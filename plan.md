# Reel Shelf 1.1 plan

1. Expand the existing picker to eight independent add-on shelves. Keep the 1.0 settings as slot one and give every slot its own source folder and label. Add a remote-operated manager with add, rename, change folder, browse, and remove actions.
2. Make Home work with an empty Kodi library. Put custom shelves first, put library entry points under More only when populated, and use the top bar for Home, shelf management, video add-ons, and favourites.
3. Bring artwork and metadata into the selected card. Keep the focus outline, reuse Kodi's list navigation, and allow each shelf to open its full source folder. Use a fallback for thin metadata or missing artwork.
4. Add an artwork-led title overview with Play, Resume, or Episodes. Give local series a next-unwatched-episode shortcut alongside native season browsing. Keep Kodi's native title actions accessible from More details and make local Continue Watching cards resume directly.
5. Build a 1.1.0 upgrade ZIP and verify the empty and populated states, multiple folders from the same provider, renamed 1.0 shelf persistence, provider failures, playback, and remote focus with the portable Kodi harness.

---

# Reel Shelf • Kodi skin for Fire TV Stick

## What the first release should feel like

Open Kodi and land on something worth watching. A large backdrop fills the upper half of the TV. The title, year and a short synopsis sit over its dark left edge. Below it, a bright outline marks the selected card. Tap Right and the next title takes over the backdrop. Tap Down and another shelf scrolls into place. Open a film, choose Resume, stop playback and land back on the same card.

Build this as an installable Kodi skin named **Reel Shelf**, add-on ID `skin.reelshelf`. Netflix supplies the interaction reference. Use original branding, Kodi fonts or properly licensed alternatives, and artwork supplied by the viewer’s media sources. The deliverable is a Kodi ZIP. All interaction happens inside Kodi.

## Target and first build

The exact Fire TV Stick model and installed Kodi version are unconfirmed. Start on desktop with Kodi 21.3 Omega and the matching Estuary skin as a provisional baseline. Read the installed version in Kodi’s System information and the model in Fire TV Settings → My Fire TV → About when available. If the device runs another version, use its matching Estuary release and GUI dependency and repeat the compatibility checks. The skin should fit the viewer’s installation without requiring a Kodi upgrade.

Start from a complete, version-pinned copy of Estuary. Give the copy its own identity, including localization contexts, skin-specific paths and assets. Retain upstream credits, license notices, runtime dependencies and the windows that make the rest of Kodi usable. Prove that the renamed copy installs and can switch back to Estuary before redesigning Home. This leaves the native keyboard, settings, source browser, confirmation dialogs and playback controls available throughout development.

## Screen design

Design at 1920 × 1080 logical pixels. Suggested starting values below can be tuned at normal sofa distance on the actual TV.

| Surface | Design and interaction |
| --- | --- |
| Home | Use roughly the upper 50% for the backdrop, with a left-to-right dark gradient behind the title. Show the first shelf in full and a glimpse of the next when available. The hero follows the focused item and has no focusable controls of its own. |
| Navigation | A narrow left rail expands to show labels on focus. Include Home, Movies, TV Shows, Video add-ons, Favourites and Settings. Keep access to Kodi’s other installed media sections through a secondary menu that preserves the upstream routes. |
| Cards | Start around 280 × 158 px for landscape shelves with 16 px gutters. Use a bright 4 px focus outline and a small lift. Keep the outline visible on white as well as dark artwork. For poster-only titles, letterbox the poster over a dark fill and show the title below. |
| Type and colour | Charcoal background (#111214), white text (#F5F5F5), muted text (#C3C5C8), warm red accent (#E44747) for progress. Start with a 64 px hero title, 32 px shelf headings and 27 px body. Clamp the synopsis to three lines. |
| Movie and TV browsing | Open the native Videos window in a styled poster grid. Give seasons and episodes a legible list with episode number and thumbnail. Keep a text-rich list for add-on folders and items with sparse metadata. |
| Title details | Restyle the video information dialog. Show title, available year/runtime, synopsis, Play or Resume and the native actions the item supports. A show opens its seasons and episodes. Keep the player’s subtitle and audio controls reachable. |

Use this art order for landscape cards: landscape → fanart → contained poster → original placeholder with item label. On the hero use fanart → landscape → dark background. Never stretch a poster to fill the hero. Focus changes the title immediately. A brief artwork delay of around 150 ms is a tuning target to avoid flashing past every backdrop during a held key. Late-arriving art must still belong to the selected item.

## What fills the shelves

Use Kodi’s own library and installed video add-ons. Keep the two sources’ playback and history semantics intact.

| Home shelf or destination | Source and rules |
| --- | --- |
| Continue Watching · Movies | A skin-owned movie smart playlist with an in-progress rule, most recently played first. A finished or unstarted movie does not qualify. |
| Continue Watching · Episodes | A separate episode smart playlist using the same rule. Show series title and season/episode where present. Opening a series that has an unfinished season is a different action from resuming an episode. |
| Recently Added Movies | Bind a native horizontal container to `videodb://recentlyaddedmovies/`. |
| Recently Added Episodes | Use `videodb://recentlyaddedepisodes/` and episode thumbnails where available. |
| Movies and TV Shows | Open `videodb://movies/titles/` and `videodb://tvshows/titles/`. Keep full catalogs accessible beyond the Home shelf limit. |
| Add-on shelf | Support one user-selected directory from an installed video add-on. Open its folders normally and delegate playable items to that add-on. Show its own labels, artwork and progress when supplied. Let the user change or clear the source. |
| Video add-ons and Favourites | Open the native Kodi destinations. These must work with an empty scanned library and while an add-on shelf is loading or unavailable. |

For the add-on shelf, first prove a real directory listing in a dynamic container with `target="videos"` and a verified `plugin://` path. Prefer a remote-operable folder picker on the target Kodi build. If the stock picker cannot browse nested add-on directories, implement a small on-demand chooser for installed video add-ons and their browsable folders. Store the selected directory and display label in this skin’s settings. Validate it against the installed provider. Never store credentials or include the viewer’s private paths in the release. Bind the stored directory as list content. Keep a source’s own playback, information and navigation actions intact, including add-on-specific menus.

Hide empty shelves after loading settles. With no scanned titles, Home should still offer **Browse video add-ons**, **Choose a shelf** and **Browse video files**. With a slow or offline source, keep the rail usable and provide a route to reopen or replace that source. Fill the hero from the first available item on entry. A focused folder without artwork gets its own label and the neutral background.

## Remote behaviour

| Starting point | Expected result |
| --- | --- |
| Enter Home | Focus the first card of the first populated shelf. With zero cards, focus the first available browse action. |
| Left / Right within a shelf | Move one card per press. Left on the first card opens the rail. Right on the last card stays there, or focuses a visible “See all” card when provided. |
| Up / Down between shelves | Skip hidden shelves. Preserve the column where possible and clamp it on shorter shelves. At the top or bottom keep a visible selection. |
| Rail | Up/Down changes destination. Right restores the previous Home card or first valid fallback. Select opens the highlighted destination. |
| Select a card | Library movies and episodes open details. Series, seasons and add-on folders open their contents. For add-on playables use their native action when useful details are unavailable. |
| Back | Close the top dialog, then return through folder or screen history. On Home content, Back opens the rail. On the root rail, use Kodi’s normal root behaviour. The physical Home button remains assigned to Fire TV. |
| After playback | Restore the originating shelf and item if present. When a completed title disappears from Continue Watching, move to its nearest neighbour or the next populated shelf. |

## Build sequence and release

1. **Bootable skin.** Pin the base, rename it, package it and prove install, activation, settings access and rollback in desktop Kodi.
2. **One complete viewing path.** Build the hero, rail and one real shelf. Prove Right → Select → Play/Resume → Stop → Back using only remote-equivalent input. Also prove one add-on folder and one playable item before investing in the remaining layouts.
3. **Complete the browse experience.** Connect remaining shelves, settings and empty states. Style the library grid, episode list and details. Keep playback history in Kodi or the source add-on.
4. **Fire Stick pass.** Test the ZIP with the actual remote. Start at 12 items per shelf, with a single hero image, short fades and static placeholders. Keep autoplay previews and background polling off. Compare warm navigation with stock Estuary on the same library. Reduce shelf counts, animations or artwork cost if focus falls behind.
5. **Hand off the build.** Deliver the versioned ZIP, editable source, one repeatable packaging command and a short README covering compatibility, choosing a shelf, installation and switching back. Record which tests ran on desktop and which ran on Fire TV.

Keep the first release focused on browsing and playback. Personalized recommendations, autoplay trailers, profile switching and cross-provider search can follow once the on-device viewing path passes. The ordered implementation and acceptance checks are in `todo.md`.

## Technical references

- [Kodi skinning manual](https://kodi.wiki/view/Skinning_Manual) and [Kodi source releases](https://github.com/xbmc/xbmc/tags)
- [Dynamic list content and folder targets](https://kodi.wiki/view/Dynamic_List_Content) and [opening native Kodi windows](https://kodi.wiki/view/Opening_Windows_and_Dialogs)
- [Kodi smart playlist rules and media types](https://kodi.wiki/view/Smart_playlists) and [video plug-in sources](https://kodi.wiki/view/Plugin_sources)
- [Amazon Fire TV remote input](https://developer.amazon.com/docs/fire-tv/remote-input.html) and [Kodi ZIP installation](https://kodi.wiki/view/Add-on_manager)
