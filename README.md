# Reel Shelf

A Kodi skin for the Fire TV Stick remote, built on Estuary. Home shows up to eight shelves from folders you choose in your video add-ons. The selected card expands to show its artwork and available title information. If Kodi has a local library, its shelves appear below your custom shelves.

## Tested

- Kodi 21.3 Omega, Windows desktop, keys only: see [TESTING.md](TESTING.md).
- Fire TV Stick: pending. The hardware checks that wait for the owner are listed in [TESTING.md](TESTING.md).

## Build and test

    python tools/build.py        # builds the ZIP and updates the GitHub Pages download in docs/
    python tools/test_build.py   # checks the ZIP (layout, XML, includes, hash)

The ZIP contains only `skin.reelshelf/`.

## Install

1. Kodi: Settings > System > Add-ons > turn on **Unknown sources**. Kodi warns that add-ons get access to personal data; accept it. If it is off, **Install from zip file** shows "For security, installation of add-ons from unknown sources is disabled." with a **Settings** button that opens this page.
2. Get the ZIP onto the device, either:
   - **From your PC over HTTP (Fire Stick):** run `python tools/serve.py 8000` on the PC (plain `python -m http.server` does not support the range requests Kodi uses on ZIPs and crashed Kodi 21.3 in testing). In Kodi: Settings > File manager > Add source > enter `http://<PC-IP>:8000/` > name it > OK.
   - **From GitHub Pages:** In Kodi's File manager, add the [Reel Shelf download page](https://kdkiss.github.io/kodi-netflix-theme/) as a source.
   - Or a local folder, an SMB share, or the Downloader app.
3. Add-ons > **Install from zip file** > pick the source > `skin.reelshelf-<version>.zip`.
4. Answer Yes to "Would you like to switch to this skin?" and **Keep** the change.

## Update an existing installation

Open **Add-ons > Install from zip file**, select your existing Reel Shelf source, and choose the newer ZIP. With the same add-on ID, Kodi installs it over the current version and keeps the saved shelf settings. Check **Settings > Interface > Skin > Configure skin > Reel Shelf** if you want to manage the shelves after updating.

## Add and manage shelves

1. On Home, open **Shelves** and select **Add shelf**. On an empty Home, you can open **Add shelf** directly.
2. Select an installed video add-on and open the folder you want. Press **Right** and select **Use this folder**. Repeat for each folder. For example, you can pin separate Movies, Most Watched TV, and Trakt Calendar folders if your add-on exposes them in its folder browser.
3. To rename a shelf, change its folder, browse the full folder, or remove it, select its name in **Shelves**. The manager is also under **Settings > Interface > Skin > Configure skin > Reel Shelf**.

Upgrading from 1.0 keeps the original shelf in the first slot. Each shelf previews up to 12 items, in the order the add-on provides, followed by a shortcut to the full folder. A temporarily empty shelf keeps its place on Home and can be managed from its card. Selecting a title or folder follows the add-on's normal Kodi behavior.

Press **Back** on a shelf to reach the top menu. Press **Down** to return to the last shelf. Local Movies and TV shows shortcuts appear under **More** when those libraries contain titles. Local Continue Watching cards resume from the saved position when selected. The title overview puts playback first, with the next unwatched episode beside the season and episode browser for local series.

## Go back to Estuary

Settings > Interface > Skin > Skin > **Estuary** > Yes. Sources and library are untouched. Reel Shelf stays installed and can be selected again.

## Credits and licence

Based on Kodi's Estuary skin (tag 21.3-Omega) by phil65 and Ichabod Fletchman. Licence as upstream: GPL-2.0-only for the code, CC BY-SA 4.0 for the artwork; see `skin.reelshelf/LICENSE.txt`, `skin.reelshelf/UPSTREAM.md` for the list of changes, and the font licences under `skin.reelshelf/fonts/`.
