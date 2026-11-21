#!/bin/sh
# dev loop: copy the skin source into the portable profile and reload it
cd "$(dirname "$0")/../.." && rm -rf .kodi/app/portable_data/addons/skin.reelshelf && cp -r skin.reelshelf .kodi/app/portable_data/addons/
