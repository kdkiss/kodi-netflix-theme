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

1. On Home, open **Shelves** in the top menu. Select **+ Add shelf**. On an empty Home you can select **Add shelf** directly.
2. In **Choose an add-on folder**, select an installed video add-on and open the folder you want (for example Movies > Trending, TV Shows > Most Watched, My Trakt > Calendar). Press **Right** and select **Use this folder**. Repeat for each folder.
3. To change a shelf, select its name in **Shelves**: **Browse full shelf**, **Rename shelf**, **Change folder** (keeps the name) or **Remove shelf**. The manager is also reachable from an empty shelf's card and from **Settings > Interface > Skin > Configure skin > Reel Shelf**.
4. Up to eight shelves fit. When all eight are used the manager shows "All eight shelf slots are in use. Remove a shelf to add another."

Each shelf runs its add-on when Home opens, so a Fire TV Stick with many shelves, or an add-on that calls online services for every list (POV with Trakt), opens Home more slowly. Keep to the lists you use. Upgrading from 1.0 or 1.1 keeps your shelves and their names. Each shelf previews up to 12 items in the add-on's order, then a **Browse full shelf** card. A shelf that is loading shows "Loading..."; an empty one shows "Empty or unavailable" with a **Manage shelves** card.

Press **Back** on a shelf to reach the top menu, **Down** to return to the shelf and card you left. **Up** from the first shelf also reaches the menu. Local Movies and TV shows shortcuts appear under **More** only when those libraries contain titles. Local Continue Watching cards resume from the saved position. The title overview puts playback first, with the next unwatched episode beside the season and episode browser for local series.

## Go back to Estuary

Settings > Interface > Skin > Skin > **Estuary** > Yes. Sources and library are untouched. Reel Shelf stays installed and can be selected again.

## Credits and licence

Based on Kodi's Estuary skin (tag 21.3-Omega) by phil65 and Ichabod Fletchman. Licence as upstream: GPL-2.0-only for the code, CC BY-SA 4.0 for the artwork; see `skin.reelshelf/LICENSE.txt`, `skin.reelshelf/UPSTREAM.md` for the list of changes, and the font licences under `skin.reelshelf/fonts/`.
