import sys, time
from pathlib import Path
from urllib.parse import urlencode, parse_qsl
import xbmcgui, xbmcplugin

H = int(sys.argv[1])
BASE = sys.argv[0]
HERE = Path(__file__).absolute().parent

def media_root():
    # ponytail: walk up from the installed copy to find tests/media; fine for the harness layout only
    for p in HERE.parents:
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

def pic(d, name):
    p = d / name
    return str(p) if p.exists() else ""

def pov_art(d, logo=False):
    # POV style: poster + fanart (+ sometimes clearlogo), never landscape
    a = {}
    poster, fan = pic(d, "poster.jpg"), pic(d, "fanart.jpg")
    if poster: a["poster"] = a["thumb"] = poster
    if fan: a["fanart"] = fan
    if logo: a["clearlogo"] = str(HERE / "resources" / "logo1.png")
    return a

def trending():
    m = movies()
    for i in range(30):
        d = m[i % len(m)]
        li = xbmcgui.ListItem("Trending %02d %s" % (i + 1, d.name.split(" (")[0][:28]))
        li.setProperty("IsPlayable", "true")
        t = li.getVideoInfoTag()
        t.setTitle(li.getLabel()); t.setMediaType("movie"); t.setYear(2000 + i % 25)
        t.setPlot("Trending movie %d. A plot long enough to test the inline info text on the expanded card." % (i + 1))
        t.setDuration(5400 + i * 60); t.setRating(5.0 + (i % 50) / 10.0, 1000 + i, "imdb", True)
        t.setGenres(["Drama", "Thriller"]); t.setMpaa("PG-13")
        li.setArt(pov_art(d, logo=(i % 3 == 0)))
        xbmcplugin.addDirectoryItem(H, url(play=d.name), li, False)

def tv_list():
    for i in range(25):
        n = "Most Watched Show %02d" % (i + 1)
        li = xbmcgui.ListItem(n)
        t = li.getVideoInfoTag()
        t.setTitle(n); t.setTvShowTitle(n); t.setMediaType("tvshow"); t.setYear(2010 + i % 14)
        t.setPlot("Show %d, a popular series with several seasons." % (i + 1))
        t.setGenres(["Drama"]); t.setRating(6.0 + (i % 30) / 10.0, 500 + i, "tmdb", True)
        li.setArt(pov_art(media_root() / "TV" / ("Paper Lanterns" if i % 2 else "Quiet Signals"), logo=(i % 4 == 0)))
        xbmcplugin.addDirectoryItem(H, url(page="seasons", show=n), li, True)

def seasons(show):
    for s in (1, 2):
        li = xbmcgui.ListItem("Season %d" % s)
        t = li.getVideoInfoTag()
        t.setTitle(li.getLabel()); t.setTvShowTitle(show); t.setSeason(s); t.setMediaType("season")
        li.setArt(pov_art(media_root() / "TV" / "Paper Lanterns"))
        xbmcplugin.addDirectoryItem(H, url(page="episodes", show=show, season=s), li, True)

def tv_file(i):
    fs = sorted((media_root() / "TV" / "Paper Lanterns" / "Season 01").glob("*.mkv"))
    return str(fs[i % len(fs)])

def episodes(show, season):
    for e in range(1, 4):
        li = xbmcgui.ListItem("%s - S%02dE%02d" % (show, season, e))
        li.setProperty("IsPlayable", "true")
        t = li.getVideoInfoTag()
        t.setTitle("Episode %d" % e); t.setTvShowTitle(show); t.setSeason(season); t.setEpisode(e)
        t.setMediaType("episode"); t.setPlot("Episode %d of season %d." % (e, season)); t.setDuration(2700)
        t.setFirstAired("2024-0%d-1%d" % (season, e))
        li.setArt({"thumb": pic(media_root() / "TV" / "Paper Lanterns", "fanart.jpg")})
        xbmcplugin.addDirectoryItem(H, url(play="tv", n=e), li, False)

def calendar():
    qs = media_root() / "TV" / "Quiet Signals"
    for i in range(12):
        show = "Trakt Show %d" % (i + 1)
        li = xbmcgui.ListItem("%s - S02E%02d - Aired Episode" % (show, i + 1))
        li.setProperty("IsPlayable", "true")
        t = li.getVideoInfoTag()
        t.setTitle("Aired Episode %d" % (i + 1)); t.setTvShowTitle(show); t.setSeason(2); t.setEpisode(i + 1)
        t.setMediaType("episode"); t.setPremiered("2026-11-%02d" % (10 + i)); t.setFirstAired("2026-11-%02d" % (10 + i))
        t.setPlot("Calendar episode %d." % (i + 1)); t.setDuration(2400)
        li.setArt({"thumb": pic(qs, "fanart.jpg"), "poster": pic(qs, "poster.jpg"), "fanart": pic(qs, "fanart.jpg")})
        xbmcplugin.addDirectoryItem(H, url(play="tv", n=i), li, False)

def main():
    q = dict(parse_qsl(sys.argv[2][1:]))
    root = media_root()
    if "play" in q:
        if q["play"] == "tv":
            f = tv_file(int(q.get("n", 0)))
        else:
            f = str(next((root / "Movies" / q["play"]).glob("*.mkv")))
        xbmcplugin.setResolvedUrl(H, True, xbmcgui.ListItem(path=f))
        return
    xbmcplugin.setContent(H, "movies")
    m = movies()
    art = lambda d: str(d / "poster.jpg") if (d / "poster.jpg").exists() else None
    page = q.get("page")
    if page is None:
        folder("Featured", page="featured")
        folder("Browse", page="browse")
        folder("Calendar (Today, 0)", page="calendar")
        folder("Movies", page="movies")
        folder("TV Shows", page="tv")
        folder("My Trakt", page="trakt")
        folder("Empty", page="empty")
    elif page == "movies":
        folder("Trending", page="trending")
    elif page == "trending":
        trending()
    elif page == "tv":
        folder("Most Watched", page="mostwatched")
    elif page == "mostwatched":
        xbmcplugin.setContent(H, "tvshows"); tv_list()
    elif page == "seasons":
        xbmcplugin.setContent(H, "seasons"); seasons(q["show"])
    elif page == "episodes":
        xbmcplugin.setContent(H, "episodes"); episodes(q["show"], int(q["season"]))
    elif page == "trakt":
        folder("Calendar", page="traktcal")
    elif page == "traktcal":
        xbmcplugin.setContent(H, "episodes"); calendar()
    elif page == "empty":
        pass
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
