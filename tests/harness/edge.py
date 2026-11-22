"""Print the left edge (px, 2560 wide) of the white focus outline on a shelf row after each key press.
usage: edge.py <key> <n> <row_y> [gap_s]   (row_y = y px inside the shelf row, 2560x1440 space)"""
import sys, time, subprocess
from PIL import ImageGrab
k, n, y = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]); gap = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
def edge():
    im = ImageGrab.grab(bbox=(0, 0, 2560, 1440)).convert("RGB")
    xs = [x for x in range(0, 2560) if min(im.getpixel((x, y))) > 235 and min(im.getpixel((x, y + 3))) > 235]
    return xs[0] if xs else None
def label():
    out = subprocess.run(["python", "tests/harness/kodi.py", "focus"], capture_output=True, text=True).stdout
    return [l.split(":")[1].strip(' ",') for l in out.splitlines() if '"ListItem.Label"' in l][0]
print("start", edge(), label())
for i in range(n):
    subprocess.run(["python", "tests/harness/kodi.py", "hold", k, "1", "0"])
    time.sleep(gap)
    print(i + 1, edge(), label())
