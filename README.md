# Reel Shelf

A Kodi skin for the Fire TV Stick remote: a large backdrop on top, horizontal shelves below (Continue Watching, Recently Added, Movies, TV shows, plus one add-on folder you choose), a narrow left rail, and a bright outline on the selected card. Interaction is inspired by streaming apps. It is built on Kodi's Estuary skin and works with Kodi's own library and installed video add-ons.

## Tested

- Kodi 21.3 Omega, Windows desktop, keys only: see [TESTING.md](TESTING.md).
- Fire TV Stick: pending. The hardware checks that wait for the owner are listed in [TESTING.md](TESTING.md).

## Build and test

    python tools/build.py        # writes dist/skin.reelshelf-<version>.zip
    python tools/test_build.py   # checks the ZIP (layout, XML, includes, hash)

The ZIP contains only `skin.reelshelf/`.

## Install

1. Kodi: Settings > System > Add-ons > turn on **Unknown sources**. Kodi warns that add-ons get access to personal data; accept it. If it is off, **Install from zip file** shows "For security, installation of add-ons from unknown sources is disabled." with a **Settings** button that opens this page.
2. Get the ZIP onto the device, either:
   - **From your PC over HTTP (Fire Stick):** run `python tools/serve.py 8000` on the PC (plain `python -m http.server` does not support the range requests Kodi uses on ZIPs and crashed Kodi 21.3 in testing). In Kodi: Settings > File manager > Add source > enter `http://<PC-IP>:8000/` > name it > OK.
   - **From GitHub Pages:** `tools/build.py` also copies the ZIP and a link page into `docs/`. With Pages serving `main` / `docs`, add `https://<user>.github.io/<repo>/` as the source instead.
   - Or a local folder, an SMB share, or the Downloader app.
3. Add-ons > **Install from zip file** > pick the source > `skin.reelshelf-<version>.zip`.
4. Answer Yes to "Would you like to switch to this skin?" and **Keep** the change.

## Choose, rename and clear the add-on shelf

Home > Choose a shelf (shown on an empty Home), or Settings > Interface > Skin > Configure skin... > **Reel Shelf**:

- **Choose add-on shelf**: pick a video add-on, open its folders with Select, press **Use this folder**.
- **Rename shelf**: edit the heading.
- **Clear add-on shelf**: remove it.

The shelf shows up to 12 items. If the add-on is missing or the folder is empty the shelf says "Unavailable or empty" and offers "Choose again".

## Go back to Estuary

Settings > Interface > Skin > Skin > **Estuary** > Yes. Sources and library are untouched. Reel Shelf stays installed and can be selected again.

## Credits and licence

Based on Kodi's Estuary skin (tag 21.3-Omega) by phil65 and Ichabod Fletchman. Licence as upstream: GPL-2.0-only for the code, CC BY-SA 4.0 for the artwork; see `skin.reelshelf/LICENSE.txt`, `skin.reelshelf/UPSTREAM.md` for the list of changes, and the font licences under `skin.reelshelf/fonts/`.
