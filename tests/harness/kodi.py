"""Reel Shelf desktop Kodi harness (stdlib only). Run: python tests/harness/kodi.py <cmd> ...
Portable Kodi lives in .kodi/app (never shipped). Data: .kodi/app/portable_data."""
import json, shutil, sqlite3, subprocess, sys, time, urllib.request, zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
APP = REPO / ".kodi" / "app"
DATA = APP / "portable_data"
USERDATA = DATA / "userdata"
LOG = DATA / "kodi.log"
MEDIA = REPO / "tests" / "media"
SCREENS = REPO / "tests" / "out" / "screens"
FIXTURE_ADDON = REPO / "tests" / "fixtures" / "plugin.video.reelshelftest"
URL = "http://127.0.0.1:8080/jsonrpc"

KEYS = {"up": "Input.Up", "down": "Input.Down", "left": "Input.Left", "right": "Input.Right",
        "select": "Input.Select", "back": "Input.Back", "home": "Input.Home",
        "contextmenu": "Input.ContextMenu", "info": "Input.Info", "showosd": "Input.ShowOSD"}
ACTIONS = {"playpause": "playpause", "stop": "stop", "pageup": "pageup", "pagedown": "pagedown",
           "next": "skipnext", "prev": "skipprevious", "fastforward": "fastforward", "rewind": "rewind"}


def rpc(method, params=None, timeout=15, kill=True):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params or {}}).encode()
    req = urllib.request.Request(URL, body, {"Content-Type": "application/json"})
    try:
        r = json.load(urllib.request.urlopen(req, timeout=timeout))
    except (TimeoutError, OSError) as e:
        if kill and ("timed out" in str(e) or isinstance(e, TimeoutError)):
            # hang detection: JSON-RPC accepted nothing within timeout -> kill Kodi and report
            subprocess.run(["taskkill", "/F", "/IM", "kodi.exe"], capture_output=True)
            raise SystemExit(f"HANG: {method} timed out after {timeout}s; Kodi killed. See portable_data/kodi.log")
        raise
    if "error" in r:
        raise RuntimeError(f"{method}: {r['error']}")
    return r["result"]


def up():
    try:
        rpc("JSONRPC.Ping", timeout=2, kill=False)
        return True
    except Exception:
        return False


# ---------- profile ----------
def reset(empty=False):
    stop()
    if DATA.exists():
        shutil.rmtree(DATA)
    USERDATA.mkdir(parents=True)
    SCREENS.mkdir(parents=True, exist_ok=True)
    vals = {
        "services.webserver": "true", "services.webserverport": "8080",
        "services.webserverauthentication": "false", "services.webserverssl": "false",
        "services.esenabled": "true", "services.esallinterfaces": "false",
        "addons.unknownsources": "true", "general.addonupdates": "2", "general.addonnotifications": "false",
        "debug.screenshotpath": str(SCREENS), "videoscreen.screen": "0", "videoscreen.fakefullscreen": "false",
        "lookandfeel.enablerssfeeds": "false", "audiooutput.audiodevice": "NULL:Null", "input.enablemouse": "false",
    }
    s = "".join(f'    <setting id="{k}">{v}</setting>\n' for k, v in vals.items())
    (USERDATA / "guisettings.xml").write_text(f'<settings version="2">\n{s}</settings>\n', encoding="utf-8")
    (USERDATA / "advancedsettings.xml").write_text(
        "<advancedsettings>\n  <loglevel>1</loglevel>\n  <splash>false</splash>\n"
        "  <video><ignoresecondsatstart>3</ignoresecondsatstart></video>\n"
        "  <network><disableipv6>true</disableipv6></network>\n</advancedsettings>\n", encoding="utf-8")
    src = "".join(f'    <source><name>{n}</name><path pathversion="1">{MEDIA / n}{chr(92)}</path>'
                  '<allowsharing>true</allowsharing></source>\n' for n in ("Movies", "TV") if not empty)
    dist = f'    <source><name>dist</name><path pathversion="1">{REPO / "dist"}{chr(92)}</path><allowsharing>true</allowsharing></source>\n'
    # "dist" file source lets the UI path (Add-ons > Install from zip file) reach the built zip
    (USERDATA / "sources.xml").write_text(
        f'<sources>\n  <video>\n    <default pathversion="1"/>\n{src}  </video>\n'
        f'  <files>\n    <default pathversion="1"/>\n{dist}  </files>\n</sources>\n', encoding="utf-8")
    install_dir(FIXTURE_ADDON)
    print("reset ok:", DATA)


def install_dir(src):
    dst = DATA / "addons" / Path(src).name
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def seed_content():
    """Set source content = movies/tvshows + metadata.local. Kodi must be stopped (DB written offline)."""
    # ponytail: DB-poking because no JSON-RPC sets source content; may break if Kodi bumps MyVideos schema
    db = max((USERDATA / "Database").glob("MyVideos*.db"))
    c = sqlite3.connect(db)
    for name, content in (("Movies", "movies"), ("TV", "tvshows")):
        path = str(MEDIA / name) + "\\"  # Kodi stores native Windows paths
        rec = 2147483647 if content == "movies" else 0
        if c.execute("select 1 from path where strPath=?", (path,)).fetchone():
            c.execute("update path set strContent=?,strScraper='metadata.local',strSettings='<settings version=\"2\"/>',"
                      "scanRecursive=?,useFolderNames=?,noUpdate=0 where strPath=?", (content, rec, int(content == "movies"), path))
        else:
            c.execute("insert into path(strPath,strContent,strScraper,strSettings,scanRecursive,useFolderNames,noUpdate)"
                      " values(?,?,'metadata.local','<settings version=\"2\"/>',?,?,0)", (path, content, rec, int(content == "movies")))
    c.commit()
    c.close()


# ---------- process ----------
def start(wait_s=90):
    if up():
        print("already running")
        return
    SCREENS.mkdir(parents=True, exist_ok=True)
    # a mouse resting over the window moves list focus on start; park it on the secondary monitor
    subprocess.run(["powershell", "-NoProfile", "-c", "Add-Type -A System.Windows.Forms;"
                    "[Windows.Forms.Cursor]::Position=New-Object Drawing.Point(-100,500)"], capture_output=True)
    subprocess.Popen([str(APP / "kodi.exe"), "-p", "--windowed"], cwd=APP,
                     creationflags=getattr(subprocess, "DETACHED_PROCESS", 0))
    wait(wait_s)


def wait(timeout=90):
    t = time.time()
    while time.time() - t < timeout:
        if up():
            time.sleep(3)  # GUI still settling after JSON-RPC comes up
            print("up")
            return
        time.sleep(1)
    raise SystemExit("timeout waiting for JSON-RPC")


def stop():
    if up():
        try:
            rpc("Application.Quit")
        except Exception:
            pass
        for _ in range(30):
            if not up():
                break
            time.sleep(1)
        time.sleep(3)
    subprocess.run(["taskkill", "/F", "/IM", "kodi.exe"], capture_output=True)  # fallback; no-op if gone
    time.sleep(1)


# ---------- input / inspect ----------
def key(*names):
    for n in names:
        if n in KEYS:
            rpc(KEYS[n])
        elif n in ACTIONS:
            rpc("Input.ExecuteAction", {"action": ACTIONS[n]})
        elif n.startswith("action:"):
            rpc("Input.ExecuteAction", {"action": n[7:]})
        else:
            raise SystemExit(f"unknown key {n}")
        time.sleep(0.6)  # ponytail: fixed delay; poll `focus` if a flow needs more


def hold(name, n=10, ms=80):
    """Simulate key repeat: n quick presses, no per-key sleep."""
    for _ in range(int(n)):
        rpc(KEYS[name])
        time.sleep(int(ms) / 1000)

def shot(name):
    SCREENS.mkdir(parents=True, exist_ok=True)
    before = set(SCREENS.glob("screenshot*"))
    rpc("Input.ExecuteAction", {"action": "screenshot"})
    for _ in range(20):
        time.sleep(0.5)
        new = set(SCREENS.glob("screenshot*")) - before
        if new:
            time.sleep(0.5)
            dst = SCREENS / f"{name}.png"
            dst.unlink(missing_ok=True)
            max(new, key=lambda p: p.stat().st_mtime).rename(dst)
            print(dst)
            return dst
    raise SystemExit("no screenshot appeared (check debug.screenshotpath)")


LABELS = ["System.CurrentWindow", "System.CurrentControl", "System.CurrentControlID", "Container.FolderPath",
          "ListItem.Label", "ListItem.Title", "Player.Title", "Player.Time", "Player.Duration"]


def focus():
    r = rpc("XBMC.GetInfoLabels", {"labels": LABELS})
    r.update(rpc("XBMC.GetInfoBooleans", {"booleans": ["Player.Playing", "Player.Paused"]}))
    r["skin"] = rpc("Settings.GetSettingValue", {"setting": "lookandfeel.skin"})["value"]
    print(json.dumps(r, indent=1))
    return r


def log(grep=None, n=80):
    lines = LOG.read_text(encoding="utf-8", errors="replace").splitlines()
    if grep:
        lines = [x for x in lines if grep in x]
    print("\n".join(lines[-n:]))


def scan(timeout=180):
    rpc("VideoLibrary.Scan", {"showdialogs": False})
    time.sleep(3)
    t = time.time()
    while time.time() - t < timeout:
        if not rpc("XBMC.GetInfoBooleans", {"booleans": ["Library.IsScanningVideo"]})["Library.IsScanningVideo"]:
            break
        time.sleep(2)
    c = {k: len(rpc(f"VideoLibrary.Get{k}").get(k.lower(), [])) for k in ("Movies", "TVShows", "Episodes")}
    print(c)
    return c


def install_zip(path):
    """Best effort: unzip into portable_data/addons; restart Kodi to load (users use UI 'Install from zip')."""
    with zipfile.ZipFile(path) as z:
        top = z.namelist()[0].split("/")[0]
        z.extractall(DATA / "addons")
    print("extracted", top, "- restart Kodi; then Addons.SetAddonEnabled {addonid, enabled:true} if disabled")


def set_skin(skin_id):
    """Set skin, then accept the 'Keep this change?' dialog (No is focused by default; 10 s timeout reverts)."""
    rpc("Settings.SetSettingValue", {"setting": "lookandfeel.skin", "value": skin_id})
    for _ in range(30):
        time.sleep(1)
        if rpc("XBMC.GetInfoLabels", {"labels": ["System.CurrentWindow"]})["System.CurrentWindow"] == "Yes / No dialog":
            key("left", "select")
            break
    time.sleep(2)
    focus()

def main(argv):
    if not argv:
        raise SystemExit(__doc__)
    c, a = argv[0], argv[1:]
    if c == "reset":
        empty = "--empty" in a  # no video sources: empty library for empty-state tests
        reset(empty)
        start()  # first run creates DBs; enable dropped-in addon, stop, seed source content, leave stopped
        rpc("Addons.SetAddonEnabled", {"addonid": "plugin.video.reelshelftest", "enabled": True})
        stop()
        if not empty:
            seed_content()
        print("content seeded; Kodi stopped" if not empty else "empty profile; Kodi stopped")
    elif c == "start":
        start()
    elif c == "stop":
        stop()
    elif c == "wait":
        wait()
    elif c == "rpc":
        print(json.dumps(rpc(a[0], json.loads(a[1]) if len(a) > 1 else None), indent=1))
    elif c == "key":
        key(*a)
    elif c == "hold":
        hold(*a)
    elif c == "shot":
        shot(a[0])
    elif c == "log":
        log(a[a.index("--grep") + 1] if "--grep" in a else None)
    elif c == "focus":
        focus()
    elif c == "install-zip":
        install_zip(a[0])
    elif c == "set-skin":
        set_skin(a[0])
    elif c == "scan":
        scan()
    else:
        raise SystemExit(f"unknown command {c}")


if __name__ == "__main__":
    main(sys.argv[1:])
