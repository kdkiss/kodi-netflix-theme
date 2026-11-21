"""Journey F: Right x10 then Left x10 from the first card; per-key focus latency (key sent -> ListItem.Label changes) and a rapid 'hold' run."""
import sys, time
sys.path.insert(0, __file__.rsplit("tests", 1)[0] + "tests/harness")
import kodi
def lab():
    r = kodi.rpc("XBMC.GetInfoLabels", {"labels": ["ListItem.Label", "System.CurrentControlID", "Container(5100).CurrentItem"]})
    return r["ListItem.Label"], r["System.CurrentControlID"], r["Container(5100).CurrentItem"]
def seq(action, n):
    lat = []; trace = []
    for _ in range(n):
        before = lab()[2]
        t = time.time(); kodi.rpc("Input." + action)
        while True:
            cur = lab()
            if cur[2] != before or time.time() - t > 3: break
        lat.append(time.time() - t); trace.append(cur[2])
    return lat, trace
tag = sys.argv[1]
print("start", lab())
lr, tr = seq("Right", 10); ll, tl = seq("Left", 10)
print(tag, "SEQ right", [round(x, 3) for x in lr], tr)
print(tag, "SEQ left ", [round(x, 3) for x in ll], tl)
print(tag, "SEQ max", round(max(lr + ll), 3), "end", lab())
t = time.time()
for _ in range(10): kodi.rpc("Input.Right")
end_r = lab(); print(tag, "HOLD right x10 ->", end_r, "settle", round(time.time() - t, 2))
t = time.time()
for _ in range(10): kodi.rpc("Input.Left")
print(tag, "HOLD left x10 ->", lab(), "settle", round(time.time() - t, 2))
kodi.shot(f"m5_F_{tag}")
