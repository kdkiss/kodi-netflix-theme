# Upstream

Based on Kodi's Estuary skin (`addons/skin.estuary`) from https://github.com/xbmc/xbmc
Tag `21.3-Omega`, commit `a3a448d26b8d560a65655dab2cd122994dc4e146`.
Licenses and credits kept: `LICENSE.txt`, `fonts/*license*`, `extras/home-images/LICENSE`.

## Changes from upstream (milestone 1)
- `addon.xml`: id `skin.reelshelf`, name "Reel Shelf", version 0.1.0, own provider-name, en_GB summary/description/disclaimer only (translated Estuary texts dropped), empty `<source>`, screenshots removed. Extension point, `xbmc.gui` 5.17.0 dependency and res folders unchanged.
- `language/*/strings.po`: header comments `Addon Name` / `Addon id` renamed (77 files).
- `resources/icon.png`, `resources/fanart.jpg`: original Reel Shelf art; Estuary screenshots deleted.
- No skin XML changed.

## Changes from upstream (milestone 2, 0.2.0)
- `xml/Home.xml` replaced with the Reel Shelf Home (upstream copy not kept; other windows do not depend on its control ids, upstream Home includes in `Includes_Home.xml` left in place).
- New `xml/Includes_ReelShelf.xml`, registered in `Includes.xml`; `media/reelshelf/*.png`; `rs_*` colours in `colors/defaults.xml`; `font64` in `Font.xml`; strings 31700-31705.

## Changes from upstream (milestone 3, 0.3.0)
- Home: shelves in a grouplist, Continue Watching/Episodes/Movies/TV Shows shelves, add-on shelf, empty-state actions.
- New `playlists/rs_inprogress_{movies,episodes}.xsp`, `xml/Custom_1190_RSPicker.xml`; `SkinSettings.xml` gets a Reel Shelf category; strings 31706-31725.

## Changes from upstream (milestone 4, 0.4.0)
- Colours: `primary_background`, `secondary_background`, `dialog_tint`, `button_focus` re-pointed to the Reel Shelf palette; `ColoredBackgroundImages` is a flat `rs_bg` fill; `lists/panel.png` tint; fanart backdrops dimmed.
- Views: `InfoWallMovieLayout` (54/500/51), View_51 poster, View_55 season/episode rows (`RS_EpRow`), View_50 seasons use View_55 rows; view ids and `<viewtype>` labels unchanged.
- `DialogVideoInfo.xml`: poster kept whole on a dark card; `Variables.xml` sub label gets runtime/rating and episode code.
- Home: settle alarm, hero art delay, episode hero title/meta; `tests/harness/kodi.py`: `hold`, hang detection, mouse disabled.

## Changes from upstream (1.0.0)
- `xml/Timers.xml` (upstream timers kept, three added): `rs_empty_focus` focuses the empty-state actions only when nothing has focus; `rs_settle_fast` ends the Home settle window as soon as a library shelf has items (3 s alarm in Home.xml stays as fallback); `rs_relayout` re-focuses the focused shelf when the settle window ends (a cold start on an add-on-only Home was blank until a key press).
- `xml/Home.xml`: the unconditional `SetFocus(9400)` alarm is removed.
- `addon.xml` 1.0.0.

## Changes from upstream (1.1.0)

- Home lists up to eight video add-on folders ahead of local-library shelves. The first slot keeps the 1.0 settings. Custom_1191_RSShelves.xml manages the slots and Custom_1190_RSPicker.xml browses the selected source.
- Includes_ReelShelf.xml provides the wide focused card and the title overview. DialogVideoInfo.xml keeps Kodi's playback, episode browsing, and maintenance actions and adds a first-unwatched-episode link for local series.
- Timers.xml recovers focus after an empty picker result or a first-shelf setup.

## Changes from upstream (1.1.1)

- `Home.xml`: the shelf list is faded out while the settle window is open and a library exists, so empty library shelves never show headings or gaps; settle alarm is 4 s.
- `Timers.xml`: `rs_settle_fast` (ends the settle window once no library shelf is updating and one has items) and `rs_relayout` (re-focuses the focused shelf when the window ends) restored, now covering the eight add-on shelves too.
- `Includes_ReelShelf.xml`: shelves are `fixedlist` with `focusposition` 0, so the focused card stays at the left edge; episode cards show show title plus SxxEyy.
- `Custom_1191_RSShelves.xml`, strings 31740: message when all slots are used.
- To raise the shelf limit: add a slot N to Home.xml (ids 52xx/56xx), the manager (`RS_ManagerSlot`), `RS_ShelfNameN`, `RS_ShelfLink52xx`, and the lists `rs_has_shelves`, `rs_has_free_slot`, `rs_managing_shelf`, `RS_NextShelf`, `RS_ManagedPath`, `RS_ManagedLabel`, plus the `rs_relayout` timer; update `tools/test_build.py`.

