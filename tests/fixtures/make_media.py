"""Generate tiny test media + NFO + art under tests/media. Needs ffmpeg on PATH. Idempotent."""
import subprocess, sys
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1] / "media"
FONT = "C\:/Windows/Fonts/arial.ttf"  # ponytail: Windows-only font path; drawtext skipped if absent
HAS_FONT = Path("C:/Windows/Fonts/arial.ttf").exists()

def ff(*a):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *a], check=True)

def esc(t):  # drawtext text escape
    return t.replace("\\", "").replace(":", "\:").replace("'", "").replace("%", "")

def video(path, title, secs=90, hue=0):
    if path.exists(): return
    path.parent.mkdir(parents=True, exist_ok=True)
    vf = f"hue=h={hue}"
    if HAS_FONT:
        vf += f",drawtext=fontfile='{FONT}':text='{esc(title)}':fontsize=18:fontcolor=white:box=1:boxcolor=black@0.6:x=10:y=10"
    ff("-f", "lavfi", "-i", "testsrc=size=320x180:rate=15", "-f", "lavfi", "-i", "sine=frequency=440:sample_rate=22050",
       "-t", str(secs), "-vf", vf, "-c:v", "libx264", "-preset", "veryfast", "-b:v", "60k", "-pix_fmt", "yuv420p",
       "-c:a", "aac", "-b:a", "32k", "-ac", "1", str(path))

def art(path, w, h, color, text=""):
    if path.exists(): return
    path.parent.mkdir(parents=True, exist_ok=True)
    vf = "null"
    if text and HAS_FONT:
        vf = f"drawtext=fontfile='{FONT}':text='{esc(text)}':fontsize={h//12}:fontcolor=gray:x=(w-tw)/2:y=(h-th)/2"
    ff("-f", "lavfi", "-i", f"color=c={color}:s={w}x{h}", "-vf", vf, "-frames:v", "1", "-update", "1", str(path))

def w(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

# (title, year, fanart, poster, plot)
MOVIES = [
    ("Amber Harbor", 2011, "orange", "orange", "A lighthouse keeper finds a map in a bottle. The tide brings stranger things each night."),
    ("Bright Meadow", 2014, "white", "yellow", "A picnic goes on far too long. Everything is very white and very sunny."),
    ("Dark Hollow", 2016, "0x050505", "0x111111", "A night-shift nurse walks an empty corridor. The lights go out one by one."),
    ("Poster Only", 2012, None, "teal", "This film has a poster but no fanart. It tests the fallback backdrop."),
    ("No Art At All", 2013, None, None, "No poster, no fanart. The skin must still show something sensible."),
    ("The Extraordinarily Long Title of a Film That Keeps Going and Going Until the Layout Gives Up", 2019, "purple", "purple",
     "A title that refuses to end. Truncation and marquee behaviour are the point."),
    ("Crimson Tide Pool", 2015, "crimson", "crimson", "Two siblings explore a tide pool. One of them is not who they claim."),
    ("Dusty Rails", 2010, "sienna", "sienna", "A freight train stops in the desert. Nobody remembers calling it."),
    ("Echo Valley", 2017, "navy", "navy", "A sound engineer records a canyon. The canyon answers back."),
    ("Frozen Orchard", 2018, "skyblue", "steelblue", "An orchard blooms in midwinter. The farmer suspects the neighbours."),
    ("Glass Garden", 2020, "seagreen", "seagreen", "A greenhouse holds a secret. It is not the plants."),
    ("Hollow Crown", 2021, "gold", "goldenrod", "A minor king loses his crown on a ferry. The ferry keeps going."),
    ("Iron Lullaby", 2009, "slategray", "slategray", "A factory plays music at dawn. The workers hum along unwillingly."),
    ("Jade Compass", 2022, "darkgreen", "darkgreen", "A compass points to the same shop every time. The shop has no door."),
]
SHOWS = {
    "Paper Lanterns": {"year": 2018, "seasons": {1: 3, 2: 2}, "plot": "A town floats lanterns every autumn. Each season uncovers who sends them."},
    "Quiet Signals": {"year": 2020, "seasons": {1: 3}, "plot": "A radio operator hears numbers at night. The numbers start to know his name."},
}

def main():
    for i, (t, y, fan, pos, plot) in enumerate(MOVIES):
        d = ROOT / "Movies" / f"{t} ({y})"
        video(d / f"{t} ({y}).mkv", t, 90 if i % 2 else 70, hue=i * 25)
        if fan: art(d / "fanart.jpg", 1280, 720, fan, t[:30])
        if pos: art(d / "poster.jpg", 500, 750, pos, t[:20])
        w(d / f"{t} ({y}).nfo", f"<movie><title>{escape(t)}</title><year>{y}</year><runtime>{2 if i % 2 else 1}</runtime>"
          f"<plot>{escape(plot)}</plot><genre>Test</genre></movie>")
    for s, info in SHOWS.items():
        d = ROOT / "TV" / s
        w(d / "tvshow.nfo", f"<tvshow><title>{s}</title><year>{info['year']}</year><plot>{escape(info['plot'])}</plot><genre>Test</genre></tvshow>")
        art(d / "fanart.jpg", 1280, 720, "indigo", s)
        art(d / "poster.jpg", 500, 750, "indigo", s)
        for sn, n in info["seasons"].items():
            for e in range(1, n + 1):
                base = f"{s} S{sn:02d}E{e:02d}"
                sd = d / f"Season {sn:02d}"
                ep = f"Episode {e}"
                video(sd / f"{base}.mkv", f"{s} {sn}x{e}", 60, hue=sn * 40 + e * 20)
                if e == 1: art(sd / f"{base}-thumb.jpg", 640, 360, "darkcyan", base)
                w(sd / f"{base}.nfo", f"<episodedetails><title>{ep} of {s}</title><season>{sn}</season><episode>{e}</episode>"
                  f"<plot>Plot of {s} season {sn} episode {e}. Something happens. Then something else.</plot><runtime>1</runtime></episodedetails>")
    print("media ok:", ROOT)

if __name__ == "__main__":
    main()
