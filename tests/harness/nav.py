"""Label-driven remote navigation helper. Usage: nav.py <label> [<label> ...]  (press Down until ListItem.Label contains each, then Select)."""
import sys, time
sys.path.insert(0, __file__.rsplit("tests", 1)[0] + "tests/harness")
import kodi
def st():
    r = kodi.rpc("XBMC.GetInfoLabels", {"labels": ["ListItem.Label", "System.CurrentWindow", "System.CurrentControlID", "Container.FolderPath", "Player.Playing"]})
    return r
def go(label, key="down", n=15):
    for _ in range(n):
        if label.lower() in st()["ListItem.Label"].lower(): return True
        kodi.key(key)
    return False
if __name__ == "__main__":
    for lab in sys.argv[1:]:
        ok = go(lab); print(lab, "found" if ok else "MISSING", st()["System.CurrentWindow"], st()["Container.FolderPath"])
        if not ok: break
        kodi.key("select"); time.sleep(2.5)
    print(st())
