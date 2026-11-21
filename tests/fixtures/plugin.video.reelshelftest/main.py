import sys, time
from pathlib import Path
from urllib.parse import urlencode, parse_qsl
import xbmcgui, xbmcplugin

H = int(sys.argv[1])
BASE = sys.argv[0]

def media_root():
    # ponytail: walk up from the installed copy to find tests/media; fine for the harness layout only
    for p in Path(__file__).resolve().parents:
        if (p / "tests" / "media").is_dir():
            return p / "tests" / "media"
    return Path("tests/media")

def url(**q):
    return BASE + "?" + urlencode(q)

def folder(label, art=None, **q):
    li = xbmcgui.ListItem(label)
    li.getVideoInfoTag().setTitle(label)
    if art: li.setArt({"thumb": art, "poster": art, "fanart": art})
    xbmcplugin.addDirectoryItem(H, url(**q), li, True)

def playable(label, movie_dir, art=None, resume=None, plot="Test item."):
    li = xbmcgui.ListItem(label)
    li.setProperty("IsPlayable", "true")
    t = li.getVideoInfoTag()
    t.setTitle(label); t.setPlot(plot); t.setMediaType("movie")
    if resume: t.setResumePoint(*resume)
    if art: li.setArt({"thumb": art, "poster": art, "fanart": art})
    xbmcplugin.addDirectoryItem(H, url(play=movie_dir), li, False)

def movies():
    return sorted((media_root() / "Movies").iterdir())

def main():
    q = dict(parse_qsl(sys.argv[2][1:]))
    root = media_root()
    if "play" in q:
        d = root / "Movies" / q["play"]
        f = next(d.glob("*.mkv"))
        xbmcplugin.setResolvedUrl(H, True, xbmcgui.ListItem(path=str(f)))
        return
    xbmcplugin.setContent(H, "movies")
    m = movies()
    art = lambda d: str(d / "poster.jpg") if (d / "poster.jpg").exists() else None
    page = q.get("page")
    if page is None:
        folder("Featured", page="featured")
        folder("Browse", page="browse")
    elif page == "featured":
        for i, d in enumerate(m[:4]):
            playable(d.name, d.name, art(d), resume=(30.0, 70.0) if i == 1 else None, plot="Featured item %d." % i)
    elif page == "browse":
        folder("Deeper Level", page="deeper", art=art(m[0]))
        folder("Twenty Items", page="twenty")
        folder("Slow Folder", page="slow")
    elif page == "deeper":
        folder("Deepest", page="featured")
    elif page == "twenty":
        for i in range(20):
            d = m[i % len(m)]
            playable("Item %02d - %s" % (i + 1, d.name), d.name, art(d) if i % 3 else None)
    elif page == "slow":
        time.sleep(4)
        playable("Slow Item", m[0].name, art(m[0]))
    xbmcplugin.endOfDirectory(H)

main()
