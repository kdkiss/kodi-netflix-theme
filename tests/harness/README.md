# Reel Shelf Kodi harness

Portable Kodi 21.3 Omega at `.kodi/app` (extracted from the official installer with 7z; never shipped, never installed).
Data: `.kodi/app/portable_data` (disposable). Log: `portable_data/kodi.log` (not `temp/`).
Web server/JSON-RPC: `http://127.0.0.1:8080/jsonrpc`, no auth. Screenshots: `tests/out/screens/<name>.png` (2560x1440 on this machine).

    python tests/fixtures/make_media.py          # once; 14 movies, 2 shows, 8 episodes -> tests/media
    python tests/harness/kodi.py reset           # wipe + seed profile, run Kodi once, seed sources, leave Kodi STOPPED
    python tests/harness/kodi.py reset --empty   # same, but no video sources (empty library)
    python tests/harness/kodi.py start|stop|wait
    python tests/harness/kodi.py scan            # prints counts
    python tests/harness/kodi.py key home down select back contextmenu info playpause stop action:<name>
    python tests/harness/kodi.py shot <name>
    python tests/harness/kodi.py focus           # window, control, folder, listitem, player, skin
    python tests/harness/kodi.py log [--grep X]
    python tests/harness/kodi.py rpc Method '{"json":"params"}'
    python tests/harness/kodi.py set-skin skin.reelshelf
    python tests/harness/kodi.py install-zip path.zip   # best effort: unzips to portable_data/addons, restart Kodi

## Quirks
- `reset` seeds source content (movies/tvshows + metadata.local) by editing MyVideos DB while Kodi is stopped; no JSON-RPC exists for it. Hence the start/stop inside reset.
- Test add-on is copied into portable_data/addons before first start; it is enabled via Addons.SetAddonEnabled during reset (otherwise "Unable to find plugin").
- First start showed no blocking dialogs (unknown-sources seeded true). Kodi opens a real window on the desktop.
- Screenshot action writes `screenshot00000.png`-style files; `shot` renames the new one.
- Source paths in DB/sources.xml must use native backslashes with trailing `\`.
- `<ignorepercentatend>` must not be set low; resume points then vanish. Resume is saved only on stop via Player.Stop/stop key after >3 s (verified: 15 s -> 15/70).
- `key` sleeps 0.6 s per key; `wait` adds 3 s after RPC is up. Slow add-on folder sleeps 4 s (Files.GetDirectory needs a longer timeout than default only if >15 s).
- Audio device forced to NULL:Null is overridden by Kodi to DirectSound; harmless.
- Keyboard-free: only JSON-RPC Input.* used. Stock Estuary: `key home` lands on Home menu; Down/Select drives it.
- install-zip is not the user path. UI path (proven in 0.2.0): `reset` seeds a `dist` file source; `rpc GUI.ActivateWindow {"window":"addonbrowser"}`, keys down down select (Install from zip file), pick `dist`, down, select the zip, then Yes (left select) and Keep (left select). Users: Settings > Add-ons > Install from zip file.
- `set-skin` waits for the "Keep this change?" dialog and answers Yes (No is the default focus).
- `start` parks the mouse off-window; a mouse over the window changes list focus.
- `sh tests/harness/sync.sh` copies skin.reelshelf into portable_data/addons for a quick dev loop (restart Kodi).
- `kodi.py hold <right|left|...> [n] [ms]` sends n presses with no extra sleep (key-repeat simulation). `rpc()` kills Kodi and exits with `HANG:` when a call times out (15 s default).
- Profile has `input.enablemouse` false; a stray real mouse no longer moves focus.
- A screenshot taken while Kodi is on a black frame (just after start) is all 0; retry after a few seconds.
