
# FFmpeg

## setup / install FFmpeg, ffprobe, ..

### from Linux distribution

BUT: distri package might be outdated!
```
sudo apt install ffmpeg
```

### precompiled binaries

for updating ffmpeg following packages are needed:

```
sudo apt install tar xz-utils
```

download, unpack and copy to `$HOME/bin/`

* https://github.com/BtbN/FFmpeg-Builds
* https://api.github.com/repos/BtbN/FFmpeg-Builds/releases/latest


## convert / cut

[superuser: cut time range](https://superuser.com/questions/758943/ffmpeg-cut-for-time-range)

ignore errors
```
ffmpeg -err_detect ignore_err   # before -i
```

* `-t` for duration
* `-to` for end time

```
ffmpeg -i input.mp4 -c:v copy -c:a aac output.mp4
ffmpeg -i input.mp4 -ss 00:34:00 -t 01:38:00 -acodec copy output.mp4
```

recode audio with 96kbps
```
ffmpeg -i input.mp4 -vn -c:a aac -b:a 96k output-audio.mp4
```

with recoding, that video/image "appears" immediately
```
ffmpeg -i input.mp4 -ss 12:10  -t 00:20 -vf "scale=854x480,fps=25" -c:v libx264 -crf 23 -c:a copy output.mp4
ffmpeg -i input.mp4 -ss 17:16 -to 18:20 -vf "scale=854x480,fps=25" -c:v libx264 -crf 23 -c:a copy output.mp4
```

## concat media files

* create file `files.txt` with (multiple) lines `file 'xyz.m4a'`

```
ffmpeg -f concat -safe 0 -i files.txt -c copy output.m4a
```

## split media

see `ffmpeg-split` in bin of this repository

```
ffmpeg -i input.mp4 -ss 899  -t 902 -c copy output.mp4
```

## convert video to audio

simply, copy codec
```
ffmpeg -i input.mp4 -vn -acodec copy output-audio.mp4
```

recoding audio with bitrate
```
ffmpeg -i input.mp4 -vn -c:a aac -b:a 96k output-audio.mp4
```



## convert with loudness normalization

sources
* [superuser: normalize audio](https://superuser.com/questions/323119/how-can-i-normalize-audio-using-ffmpeg)
* [dynaudnorm filter guide](https://www.ffmpeg-micro.com/blog/ffmpeg-dynaudnorm-filter-guide)
* [dynaudnorm filter](https://ayosec.github.io/ffmpeg-filters-docs/8.0/Filters/Audio/dynaudnorm.html)
* [loudnorm filter](https://ayosec.github.io/ffmpeg-filters-docs/8.0/Filters/Audio/loudnorm.html)

```
ffmpeg -i input.m4a -filter:a "dynaudnorm=p=0.9:s=5"                    output.m4a
ffmpeg -i input.m4a -c:v copy -filter:a "dynaudnorm=p=0.9:s=5" -c:a aac output.mp4
```


## convert video resolution

```
ffmpeg -i input_video.mp4 \
-vf "scale=1280:720" \
-c:v libx264 -crf 23 \
-c:a copy \
output_720p.mp4
```

convert video resolution
```
ffmpeg -i input.mp4 -vf "scale=1280:720"  -c:v libx264 -crf 23 -c:a copy output-720p.mp4
```

convert frame rate
```
ffmpeg -i <input> -filter:v fps=30 <output>
```


## convert video resolution and frames in single call

* [reducing resolution](https://www.reddit.com/r/ffmpeg/comments/g318yl/reducing_resolution_and_fps_of_a_video_without/)
* [convert to common resolutions](https://www.mux.com/articles/convert-video-to-different-resolutions-with-ffmpeg#converting-to-common-resolutions)
  *  480p (854x480)
  *  720p (1280x720)
  * 1080p (1920x1080)
  * 4K    (3840x2160)

```
ffmpeg -i input.mp4 -vf "scale=1280:720,fps=25" -c:v libx264 -crf 23 -c:a copy         output-720p-25fps.mp4
ffmpeg -i input.mp4 -vf "scale=1280:720,fps=25" -c:v libx264 -crf 23 -c:a aac -b:a 64k output-720p-25fps-64kbps.mp4
ffmpeg -i input.mp4 -vf "scale=854x480,fps=25"  -c:v libx264 -crf 23 -c:a aac -b:a 64k output-480p-25fps-64kbps.mp4
```


## subtitles

* to inject an external .srt subtitle file into a video without re-encoding,
use the `-c copy` flag to copy existing streams and `-c:s` to specify the subtitle codec.
MP4 files require the `mov_text` codec for soft subtitles:

```
ffmpeg -i input.mp4 -i subtitle.srt -c copy -c:s mov_text output.mp4
```

* extract: [ffmpeg-extract-subtitles](https://nicolasbouliane.com/blog/ffmpeg-extract-subtitles)

```
ffmpeg -i input.mkv -map "0:m:language:eng" -map "-0:v" -map "-0:a" output.srt
```


```
ffmpeg -i video.mp4 -map 0:s:0 subtitles.srt
```

`-map 0:s:0` specifies the subtitle stream index.
The first 0 identifies the input file, which will always be 0 when working with a single input.
`s` selects subtitle tracks and the last 0 identifies which subtitle stream ID to select for extraction.

[SRT format](https://www.3playmedia.com/blog/create-srt-file/)


## cheat sheet

[cheat sheet](https://gist.github.com/steven2358/ba153c642fe2bb1e47485962df07c730)

* `-c copy`: Kopiert alle Streams (Video, Audio, Untertitel) ohne Neukodierung (Remuxing). Dies ist schnell und verlustfrei.
* `-c:v [Codec]`: Legt den Video-Codec fest (z. B. -c:v libx264).
* `-c:a [Codec]`: Legt den Audio-Codec fest (z. B. -c:a aac).
* `-c:s [Codec]`: Legt den Untertitel-Codec fest.
