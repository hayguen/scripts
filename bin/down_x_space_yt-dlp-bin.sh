#!/bin/bash

yt-dlp "$@" 2>&1 |grep -v "for reading$"
