"""Drive Add-ons > Install from zip file with keys only. Usage: ui_install.py <dir-label> <zip-name> [--keep]
Source is picked by list label (a file source added in File manager, e.g. 'dist' or an HTTP source)."""
import sys, time
sys.path.insert(0, __file__.rsplit("tests", 1)[0] + "tests/harness")
import kodi

def lab():
    r = kodi.rpc("XBMC.GetInfoLabels", {"labels": ["ListItem.Label", "System.CurrentWindow", "Container.NumItems"]})
    return r["ListItem.Label"], r["System.CurrentWindow"], r["Container.NumItems"]

def goto(label, tries=60):
    for _ in range(tries):
        if lab()[0] == label:
            return True
        kodi.key("down")
    return False

src, zipname = sys.argv[1], sys.argv[2]
kodi.rpc("GUI.ActivateWindow", {"window": "home"}); time.sleep(1)
kodi.rpc("GUI.ActivateWindow", {"window": "addonbrowser"}); time.sleep(1.5)
assert goto("Install from zip file", 6), lab()
kodi.key("select"); time.sleep(1.5)
print("source list:", lab())
assert goto(src), ("source not found", lab())
kodi.key("select"); time.sleep(3)
print("in source:", lab())
assert goto(zipname), ("zip not found", lab())
print("picked", lab()); kodi.key("select")
for _ in range(20):
    time.sleep(1)
    if lab()[1] == "Yes / No dialog": break
print("dialog:", lab()); kodi.shot("m5_ui_switch")
kodi.key("left", "select")  # Yes
for _ in range(30):
    time.sleep(1)
    if lab()[1] == "Yes / No dialog":
        kodi.shot("m5_ui_keep"); kodi.key("left", "select"); break  # Keep
time.sleep(3)
print("final:", kodi.rpc("XBMC.GetInfoLabels", {"labels": ["System.CurrentWindow"]}), kodi.rpc("Settings.GetSettingValue", {"setting": "lookandfeel.skin"}))
