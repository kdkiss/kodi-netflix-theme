"""Perf: time from process start to first focused item, and Right x10 latency. Usage: perf.py <skin id> <runs>"""
import sys, time, subprocess
sys.path.insert(0, __file__.rsplit("tests", 1)[0] + "tests/harness")
import kodi
skin, runs = sys.argv[1], int(sys.argv[2])
def info(*l):
    return kodi.rpc("XBMC.GetInfoLabels", {"labels": list(l)})
res = []
for r in range(runs):
    kodi.stop(); time.sleep(2)
    import subprocess as sp
    t0 = time.time()
    sp.Popen([str(kodi.APP / "kodi.exe"), "-p", "--windowed"], cwd=kodi.APP, creationflags=getattr(sp, "DETACHED_PROCESS", 0))
    while not kodi.up(): time.sleep(0.05)
    up = time.time() - t0
    first = None
    while time.time() - t0 < 60:
        try: i = info("System.CurrentControlID", "ListItem.Label", "System.CurrentWindow")
        except Exception: continue
        if i["System.CurrentWindow"] == "Home" and i["System.CurrentControlID"] and i["ListItem.Label"]:
            first = time.time() - t0; break
        time.sleep(0.05)
    # right x10 warm (needs a horizontal list focused; move into content first)
    lat = []
    if skin == "skin.estuary":
        kodi.key("right"); time.sleep(0.5)
    for _ in range(10):
        b = info("ListItem.Label")["ListItem.Label"]; t = time.time(); kodi.rpc("Input.Right")
        while info("ListItem.Label")["ListItem.Label"] == b and time.time() - t < 3: pass
        d = time.time() - t
        if d < 2.9: lat.append(d)   # >=2.9 s = label never changed (end of row), not a pause
    
    print(skin, f"run{r+1}: rpc-up {up:.1f}s, first focused item {first and round(first,1)}s, right moves {len(lat)}/10 max {max(lat):.3f}s mean {sum(lat)/len(lat):.3f}s")
