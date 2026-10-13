#!/bin/bash

EDIDDEC="$(which edid-decode)"
if [ -z "$EDIDDEC" ]; then
  echo "missing edid-decode"
  echo "install with: sudo apt install edid-decode"
else
  for dir in $(ls -1 /sys/class/drm/); do
    if [ -d "/sys/class/drm/${dir}" ] && [ -f "/sys/class/drm/${dir}/edid" ]; then
      echo "--- Device: /sys/class/drm/${dir} ---"
      edid-decode "/sys/class/drm/${dir}/edid" | grep -E "Manufacturer:|Product|Serial Number"
    fi
  done
  echo ""
fi

DDCUTIL="$(which ddcutil)"
if [ -z "$DDCUTIL" ]; then
  echo "missing ddcutil"
  echo "install with: sudo apt install ddcutil"
else
  echo "--- ddcutil detect ---"
  ddcutil detect
fi
