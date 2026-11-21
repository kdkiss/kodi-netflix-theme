"""Add a file source via File manager > Add source, keys + SendText only. Usage: add_http_source.py <url> <name>"""
import sys, time
sys.path.insert(0, __file__.rsplit("tests", 1)[0] + "tests/harness")
import kodi, nav
url, name = sys.argv[1], sys.argv[2]
kodi.rpc("GUI.ActivateWindow", {"window": "home"}); time.sleep(1)
kodi.rpc("GUI.ActivateWindow", {"window": "filemanager"}); time.sleep(2)
assert nav.go("Add source"); kodi.key("select"); time.sleep(1.5)
kodi.key("select"); time.sleep(1.5)                       # path row -> keyboard
kodi.rpc("Input.SendText", {"text": url, "done": True}); time.sleep(1)
for _ in range(6):
    if nav.st()["System.CurrentControlID"] == "12": break
    kodi.key("down")
kodi.key("select"); time.sleep(1.2)                       # name -> keyboard
kodi.rpc("Input.SendText", {"text": name, "done": True}); time.sleep(1)
kodi.key("down"); kodi.key("select"); time.sleep(2)       # OK
print(nav.st())
