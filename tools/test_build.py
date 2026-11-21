import hashlib, re, sys, zipfile
import xml.etree.ElementTree as ET
sys.path.insert(0, __file__.rsplit("tools", 1)[0] + "tools")
import build

def run():
    out, _, _ = build.build()
    return out, hashlib.sha256(out.read_bytes()).hexdigest()

out, h1 = run()
_, h2 = run()
assert h1 == h2, "build not deterministic"
z = zipfile.ZipFile(out)
names = z.namelist()
assert "skin.reelshelf/addon.xml" in names
assert all(n.startswith("skin.reelshelf/") for n in names), "entry outside skin.reelshelf/"
assert names == sorted(names)
root = ET.fromstring(z.read("skin.reelshelf/addon.xml"))
assert root.get("id") == "skin.reelshelf"
assert any(e.get("point") == "xbmc.gui.skin" for e in root.iter("extension"))
assert "skin.estuary" not in z.read("skin.reelshelf/addon.xml").decode()
for n in names:
    if n.endswith("strings.po"):
        head = z.read(n).decode("utf-8")[:300]
        assert "skin.estuary" not in head and "Addon Name: Estuary" not in head, n
home = ET.fromstring(z.read("skin.reelshelf/xml/Home.xml"))
shelves = [
    {param.get("name"): param.get("value") for param in node.findall("param")}
    for node in home.iter("include")
    if node.get("content") in {"RS_AddonShelf", "RS_Shelf"}
]
control_ids = [node.get("id") for node in home.iter("control") if node.get("id")]
control_ids.extend(shelf[name] for shelf in shelves for name in ("id", "group"))
assert len(control_ids) == len(set(control_ids)), "Home shelf and group control IDs must not overlap"

manager = ET.fromstring(z.read("skin.reelshelf/xml/Custom_1191_RSShelves.xml"))
managed_keys = [
    node.find("param[@name='key']").get("value")
    for node in manager.iter("include")
    if node.get("content") == "RS_ManagerSlot"
]
home_keys = [shelf["key"] for shelf in shelves if "key" in shelf]
assert home_keys == managed_keys == ["rs.addon"] + [f"rs.addon{i}" for i in range(2, 9)], (
    "Home and the manager must share eight independent slots, starting with the 1.0 setting"
)

print("ok", h1)
