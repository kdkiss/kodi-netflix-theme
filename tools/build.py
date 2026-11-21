#!/usr/bin/env python3
"""Build dist/skin.reelshelf-<version>.zip deterministically. Stdlib only."""
import hashlib, sys, zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIN = ROOT / "skin.reelshelf"
ADDON_ID = "skin.reelshelf"
EXCLUDE_DIRS = {"__pycache__", ".git", ".idea", ".vscode"}
EXCLUDE_NAMES = {".DS_Store", "Thumbs.db", "desktop.ini"}
EXCLUDE_SUFFIX = (".pyc", ".pyo", ".xbt", ".swp", ".swo", "~", ".bak", ".orig")
STAMP = (1980, 1, 1, 0, 0, 0)


def files():
    out = []
    for p in SKIN.rglob("*"):
        rel = p.relative_to(SKIN)
        if not p.is_file() or EXCLUDE_DIRS & set(rel.parts):
            continue
        if p.name in EXCLUDE_NAMES or p.name.endswith(EXCLUDE_SUFFIX):
            continue
        out.append(rel.as_posix())
    return sorted(out)


def check_xml(rels):
    errs = []
    for r in rels:
        if r.endswith(".xml"):
            try:
                ET.parse(SKIN / r)
            except ET.ParseError as e:
                errs.append(f"{r}: {e}")
    return errs


def check_includes(rels):
    defs, uses = set(), {}
    for r in rels:
        if not (r.startswith("xml/") and r.endswith(".xml")):
            continue
        for el in ET.parse(SKIN / r).iter():
            if el.tag == "include":
                n, c = el.get("name"), el.get("content")
                if n:
                    defs.add(n)
                if c:
                    uses.setdefault(c, r)
                if not n and not c and el.text and el.text.strip():
                    uses.setdefault(el.text.strip(), r)
    # dynamic names ($PARAM[..], $INFO[..], $EXP[..]) cannot be resolved statically
    return sorted((u, f) for u, f in uses.items() if u not in defs and "$" not in u)


def version():
    return ET.parse(SKIN / "addon.xml").getroot().get("version")


def build():
    rels = files()
    errs = check_xml(rels)
    if errs:
        sys.exit("XML parse errors:\n" + "\n".join(errs))
    missing = check_includes(rels)
    for n, f in missing:
        print(f"WARNING missing include definition: {n} (used in {f})")
    out = ROOT / "dist" / f"{ADDON_ID}-{version()}.zip"
    out.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for r in rels:
            zi = zipfile.ZipInfo(f"{ADDON_ID}/{r}", STAMP)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o100644 << 16
            zi.create_system = 3
            z.writestr(zi, (SKIN / r).read_bytes(), zipfile.ZIP_DEFLATED, 9)
    return out, len(rels), missing


def publish(out):
    """Mirror the ZIP into docs/ with a link page, so GitHub Pages works as a Kodi source."""
    docs = ROOT / "docs"
    docs.mkdir(exist_ok=True)
    for old in docs.glob(f"{ADDON_ID}-*.zip"):
        old.unlink()
    (docs / out.name).write_bytes(out.read_bytes())
    # Kodi lists an HTTP source by parsing <a href> links; plain relative names only.
    (docs / "index.html").write_text(f'<!doctype html><title>Reel Shelf</title>\n<a href="{out.name}">{out.name}</a>\n', encoding="utf-8")


if __name__ == "__main__":
    out, n, missing = build()
    publish(out)
    print(out)
    print("entries:", n, "missing includes:", len(missing))
    print("sha256:", hashlib.sha256(out.read_bytes()).hexdigest())
