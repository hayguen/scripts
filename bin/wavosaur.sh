#!/bin/bash

# source:
# https://www.wavosaur.com/
#
# sudo apt install -y wine64 winetricks

if [ ! -f /home/ayguen/Documents/sw/audio/Wavosaur.exe ]; then
  echo "Error: wavosaur isn't installed"
  # echo "copy from /mnt/bigdata/software/Windows/Entwicklung/Wavosaur"
  echo "copy from /mnt/samba/procitec/software/Windows/Entwicklung/Wavosaur"
  echo "  or  wavosaur.com/download.php"
  exit 1
fi
# echo passing cli parameters: "$@"
wine /home/ayguen/Documents/sw/audio/Wavosaur.exe "$@" &>/dev/null &
