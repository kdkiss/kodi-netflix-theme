# Reel Shelf 1.1.1 testing

Portable Kodi 21.3 Omega on Windows, 2560x1440, remote-equivalent keys (JSON-RPC `Input.*`); JSON-RPC only for setup and reading state. Screenshots: `tests/out/screens/f11_*.png` (Kodi's own screenshot is black on this machine, so `kodi.py shot` falls back to a desktop capture).

Test add-on now imitates POV: Movies > Trending (30 playable movies, poster+fanart, no landscape, some clearlogo), TV Shows > Most Watched (25 tvshow folders > seasons > episodes), My Trakt > Calendar (episodes with show title, season, episode, aired date), a 4 s folder, an empty folder.

| Check | Desktop (Kodi 21.3) | Fire TV |
| --- | --- | --- |
| Library profile cold start, empty Continue Watching | PASS. Headings and gaps no longer appear; layout is identical at t=0, 1 and 2 s and focus is on the first Recently Added card (`f11_cold_lib_t0`-`t2`). | owner to test |
| Focused-card movement | PASS. Left edge of the focused card stays at x=118 for 13 single presses 1 s apart (`tools`: `tests/harness/edge.py`); Right x10 then Left x10 end on the expected cards, one card per press (`f11_fixed_r10`). | owner to test |
| Add-on only profile (`reset --empty`): add four shelves by keys, rename, remove, re-add, restart | PASS. Shelves persist in order; Change folder keeps the name (`f11_e_*`, `f11_j_cold_late`). | owner to test |
| Cold start focus, no library headings | PASS. First card of the first shelf focused with outline. | owner to test |
| Up/Down between shelves | PASS. Each shelf keeps its own card; focused card at the left edge in every shelf. | owner to test |
| tvshow folder card > seasons > Back | PASS. Back returns to the same Home card (`f11_j_seasons`, `f11_j_back_same`). | owner to test |
| Movie / calendar episode card > play > Stop | PASS. Same card focused after Stop. | owner to test |
| Calendar card | PASS. Show title, SxxEyy and episode title (`f11_j_cal3`). | owner to test |
| Browse full shelf card | PASS. Opens the folder in Videos; Back returns to the card. | owner to test |
| Slow (4 s) shelf | PASS. Shows "Loading..."; focus stays on the first shelf; the layout below does not move under the focus. | owner to test |
| Empty shelf | PASS. "Empty or unavailable" plus a Manage shelves card; reachable. (`f11_j_empty`) | owner to test |
| Eight shelves | PASS. Eighth reachable; manager shows the full message (`f11_l_full`, `f11_l_home8`); Back then Down returns to it. | owner to test |
| Top menu, Back | PASS. Shelves, Video add-ons, Favourites, More (Settings, Search) open; Back from a shelf goes to the menu, Down returns. | owner to test |
| Upgrade 1.1.0 > 1.1.1 over UI install | PASS. Slot 1 shelf renamed "POV Shows" on 1.1.0 kept name and path after "Install from zip file" of 1.1.1 (`f11_u_zip3`). | owner to test |
| Packaged ZIP, clean `reset --empty`, UI install | PASS. Add four shelves, restart, cold start, select/back, play/stop all as above (`f11_p_cold`). | owner to test |
| kodi.log | No skin errors, missing includes or textures. | - |

## What changed

1. Library shelves were counted as visible during the settle window, so empty headings showed until a key press. The shelf list is now faded out until the settle ends, `rs_settle_fast` and `rs_relayout` are back (and cover the add-on shelves).
2. The shelf was a `list`, so the focused card slid to the fourth slot and the row moved around it. It is a `fixedlist` with `focusposition` 0 now.
3. Episode cards show show title and SxxEyy. The manager reports when all slots are used.

## Shelf limit

Eight slots: Home.xml (two ids each), Includes_ReelShelf.xml (name, link, lists), Custom_1191_RSShelves.xml, Timers.xml `rs_relayout`, `tools/test_build.py`. See `skin.reelshelf/UPSTREAM.md` for the checklist. Cost: every added slot adds one add-on run (Python start plus any web calls) on each Home load and about 12 art textures; on a Stick this is the limiting factor, not XML.

## Not tested

Fire TV hardware, real POV with a Trakt account, overscan, Fire remote mapping. Owner to test: first usable Home with their real shelves, Right x10 on a shelf, Select on a show then Back, Select on a movie then Stop, restart persistence.

---

# Reel Shelf 1.1 testing

Verified on portable Kodi 21.3 Omega using the local test video add-on and synthetic media. The 1.0 release results follow below.

- With an empty library, Add shelf opens the picker and returns focus to the first saved shelf.
- A shelf saved with the 1.0 settings opens under its original name. Two more folders from the same add-on can be added independently, including an empty calendar with a comma in its name.
- Renaming, changing a folder, removing a shelf, and restarting Kodi preserve the other shelves. Changing the folder keeps the shelf name.
- A folder with 20 entries shows 12 on Home plus the full-folder shortcut. Back and Down restore the selected Home card, and selecting a playable add-on item starts its video.
- With all eight slots populated, remote navigation reached the eighth shelf. Back then Down returned to it, and ten Right presses followed by ten Left presses restored the first card.
- The playback overview opens the secondary details and starts a local movie. Continue Watching resumed that movie about eight seconds in with a single Select press.
- For a two-season show with episode 1 marked watched, Next episode displayed and played S01E02. Episodes opened the normal season browser.
- Fire TV and a signed-in POV/Trakt account remain to be tested.

---

# Reel Shelf testing

Release artifact: `dist/skin.reelshelf-1.0.0.zip`, 4,107,130 bytes, SHA-256 `6719cef3759aa7da2b36605711729af55613ee9aee5d0c2c16616161ef795551`.

Desktop column: Kodi 21.3 Omega portable build on Windows 11, 2560x1440, input by remote-equivalent keys (JSON-RPC `Input.*`) only; JSON-RPC used for setup and reading state. Every desktop run below used the skin installed from that exact ZIP through Add-ons > Install from zip file, on a freshly reset profile. Screenshots are in `tests/out/screens/`.

Fire TV column: nothing was run on hardware.

| Check | Desktop (Kodi 21.3) | Fire TV |
| --- | --- | --- |
| A. Empty installation | PASS. `reset --empty`: Home shows "Browse video add-ons", "Choose a shelf", "Browse video files"; focus lands on the first within 1.5 s of settle; rail reachable with Left/Down. `m5_A1_home`, `m5_70_*`, `m5_72_rail_*`. | not run — owner to test |
| B. Movie night | PASS. Home > Hollow Crown > details > Play (10 s) > Stop > resume prompt "Resume from 00:00:10" > resumed at 14 s > Stop saved 17 s; focus back on the same card. `m5_R_B_back`, `m5_R_B_resume`, earlier run `m5_B1`-`m5_B9`. | not run — owner to test |
| C. Series night | PASS. Rail TV shows > Quiet Signals (single season, Kodi opens its episode list) > 1x02 plays as S1E2 (Player.GetItem: Quiet Signals, season 1, episode 2) > Stop > Back > Back to the shows list > Back to Home. `m5_R_C3`, `m5_R_C4_eps`, `m5_R_C5_play`. | not run — owner to test |
| D. Add-ons only | PASS. `reset --empty`: Choose a shelf > Reel Shelf Test Source > Browse > Twenty Items > shelf shows after a full restart; Select "Deeper Level" > nested folders > Featured > Amber Harbor plays; Skin settings > Reel Shelf > Clear add-on shelf; restart: empty state again, Browse video add-ons reachable. `m5_D3`-`m5_D20`. | not run — owner to test |
| E. Mixed and unavailable | PASS. Library shelves plus the add-on shelf; the picker's 4 s Slow Folder showed "Loading..." and stayed usable; disabling the test add-on gives "Slow Folder / Unavailable or empty... / Choose again" while Continue Watching, TV shows and the rail still work and Settings opens. Items without art get a placeholder plus label. `m5_E1`-`m5_E8`. Known gap: after re-enabling the add-on, the shelf stays "unavailable" until Kodi restarts or Home reloads the provider (see Issues). | not run — owner to test |
| F. Navigation under load | PASS. Right x10 then Left x10 from the first card, per key (send to focus change): max 0.041 s cold, 0.060 s warm; focus ends on the same first card; 10 Rights with no spacing settle on card 11 in 0.16 s, 10 Lefts back on card 1 in 0.12 s. No pause near 1 s. Final release ZIP: max 0.060 s. `m5_F_cold`, `m5_F_warm`. | not run — owner to test |
| G. Device lifecycle | Partial analogue. Window sent behind another application and brought back, with the skin kept, same focused card, and playback continuing (20 s > 28 s > 32 s) with focus on the OSD window; full Kodi restart keeps the skin (`lookandfeel.skin`), saved add-on shelf and a valid focused card. `m5_G2`-`m5_G4`. Fire TV Home is not testable. See Issues for the minimise/restore crash. | not run — owner to test |
| H. Install and rollback | PASS. Installed the ZIP from a local file source and from an HTTP source (see below); accepted "Would you like to switch to this skin?" and "Keep this change?"; then Settings > Interface > Skin > Skin > Estuary > Yes; Estuary Home opens with the same video sources and the library intact (14 movies after a rescan; Estuary shows its empty-library text until the library is scanned in this harness profile). `m5_H*`, `m5_ui_*`. | not run — owner to test |

## Review fixes

1. **Focus alarm.** Home.xml no longer fires an unconditional `SetFocus(9400)` 4 s after load. Skin timer `rs_empty_focus` (Timers.xml) starts only when the empty-state actions are visible and `System.CurrentControlID` is empty, and focuses them after 1 s. Proof: on the empty profile, `Left` to the rail then two `Down` during the first seconds ended on "TV shows"; 8 s later focus was still on the rail (`m5_72_rail_during`/`m5_72_rail_after`). With nothing focused the actions are focused once (`m5_70_*`). A `SendClick` to a hidden button and conditional alarm builtins did not run reliably in 21.3, so a skin timer was used.
2. **Settle-window flicker.** Checked on a populated profile with an empty Continue Watching Episodes shelf and a one-item Continue Watching Movies shelf. Before the change the window showed all empty shelves as visible; after the change a screenshot at 0.4 s and at 3 s were pixel-identical in layout and focus (`m5_41_r2_t0.4`, `m5_41_r2_t3`). `rs_settle_fast` ends the window as soon as a library shelf has items; `rs_relayout` re-focuses the focused shelf when it ends. This also fixed a cold-start bug that existed in 0.4.0: an add-on-only Home was blank until a key press (`m5_D10_v040` before, `m5_D11` after).

## Performance (same desktop profile, 14 movies, 2 shows, 8 episodes)

Time from launching `kodi.exe` to a focused item on Home, and 10 Right presses from that item. Three runs each.

| Skin | JSON-RPC up | First focused item | Right x10, per-key max |
| --- | --- | --- | --- |
| Reel Shelf 1.0.0 | 1.5 / 1.5 / 2.1 s | 1.5 / 1.6 / 2.1 s | 0.050 / 0.060 / 0.060 s (10 of 10 moved) |
| Estuary (stock) | 1.5 / 1.5 / 2.1 s | 1.5 / 1.6 / 2.1 s | 0.050 / 0.062 / 0.061 s (9 of 10 moved; its widget row ends) |

On-device numbers are pending. Desktop is not a Fire Stick: expect slower cold start and art decoding. Provider delay is separate: the 4 s slow add-on folder never delayed local shelves or focus.

## Install over HTTP (the Fire Stick method), verified on desktop

1. On the PC: `python tools/serve.py 8000` (serves `dist/` with HTTP Range support).
2. In Kodi: Settings > File manager > Add source > `<None>` row: type `http://<PC-IP>:8000/` > name box: e.g. `ReelShelfHTTP` > OK.
3. Settings > System > Add-ons > Unknown sources: on.
4. Add-ons > Install from zip file > `ReelShelfHTTP` > `skin.reelshelf-1.0.0.zip` > Yes (switch skin) > Keep.

Result: Kodi 21.3 listed the Python directory page and installed the ZIP (`m5_H6b`, `m5_H12`; server log shows `GET ... 206`). Findings:

- `python -m http.server --directory dist` lists the folder fine, but it ignores HTTP Range. Kodi reads the ZIP's central directory with a range request, and Kodi 21.3 on desktop then crashed (`CCurlFile ... Requested range was not delivered by the server(33)`, dump in the profile). `tools/serve.py` is a stdlib server that answers Range with 206; with it the install succeeds. Use it instead of `python -m http.server`.
- Unknown sources off: pressing Install from zip file shows dialog "Disabled": "For security, installation of add-ons from unknown sources is disabled." with buttons "Settings" and "OK". "Settings" opens Settings / System > Add-ons > General > Unknown sources ("Allow installation of add-ons from unknown sources."). Turning it on shows "Warning!": "Add-ons will be given access to personal data stored on this device. By allowing, you agree that you are solely responsible for any loss of data, unwanted behaviour, or damage to your device. Proceed?" (Yes / No, No is the default). `m5_H13`, `m5_H14`, `m5_H15`.
- Fire TV alternatives, not tested: the Downloader app (open the ZIP URL, then Kodi: Install from zip file > Home folder / Downloads folder), or an SMB share added as a source.
- The Windows firewall must allow inbound port 8000 on the PC for the Stick to reach it.

## Issues and gaps

- **Kodi 21.3 desktop crashes when restored after being minimised** (`ShowWindow` minimise then restore), on stock Estuary too, so it is not the skin. Sending the window behind another application and back is fine. Not relevant to Fire TV.
- After re-enabling a disabled add-on that backs the shelf, the shelf stays on "Unavailable or empty" until Kodi restarts. "Choose again" replaces the source meanwhile.
- A fresh `reset` profile only reports library content after a rescan and restart (harness behaviour); the skin was checked after that.
- Not testable on desktop: overscan/safe area, Fire remote key mapping, the physical Home button, audio-track menu with multi-track media, real subtitles.
- Fire TV: owner to run A to H with the actual remote, record model, Kodi version and media source, and time first usable Home plus the warm Right x10 run against Estuary.

## Fire TV checklist (owner)

Run journeys A to H from `todo.md` section 5 with the Fire remote. Cells above stay "not run" until then.
