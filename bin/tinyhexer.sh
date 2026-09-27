#!/bin/bash

# sudo apt install -y wine64 winetricks

if [ ! -f "$HOME/.wine/drive_c/Program Files (x86)/mirkes.de/Tiny Hexer/mpth.exe" ]; then
  echo "Error: TinyHexer isn't installed"
  echo "install from /mnt/bigdata/software/Windows/Entwicklung/TinyHexer"
  echo "  or  https://www.chip.de/downloads/Tiny-Hexer_13014623.html"
  echo "  or  https://www.limedownload.com/tiny-hexer/download"
  exit 1
fi
# echo passing cli parameters: "$@"
wine "$HOME/.wine/drive_c/Program Files (x86)/mirkes.de/Tiny Hexer/mpth.exe" "$@" &>/dev/null &
