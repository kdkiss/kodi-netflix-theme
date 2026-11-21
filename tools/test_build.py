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
print("ok", h1)
