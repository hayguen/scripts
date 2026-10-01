
# YT-DLP - downloader for media files

usable for YouTube, Twitter/X and many more

[complete tutorial for beginners](https://ostechnix.com/yt-dlp-tutorial/)

main setup with `requirements.txt` in python environment, see [README](README.md)

```
pip install -r requirements.txt
```

## JavaScript runtime for yt-dlp

see https://docs.deno.com/runtime/getting_started/installation/

```
curl -fsSL https://deno.land/install.sh | sh
```

* configure deno in ~/.yt-dlp/config

```
mkdir $HOME/.yt-dlp
cat >$HOME/.yt-dlp/config <<EOF
--write-link
--write-subs
--embed-subs
--embed-metadata
--embed-chapters

--js-runtimes deno:$HOME/.deno/bin/deno

--audio-multistreams
--merge-output-format mp4

--restrict-filenames
--mtime
-o "%(upload_date>%Y-%m-%d)s_%(title)s.%(ext)s"
EOF

```

## test / run yt-dlp

list available formats of a YouTube Video

```
yt-dlp -F https://youtu.be/5zZzjwl-m5A
```

options

* download multiple formats giving ids at `-f` video+audio separated with `+`
* special at `-f`: `best`, `worst`, `bestvideo`, `worstvideo`, `bestaudio`, `worstaudio`
* or abbreviated: `bv`, `wv`, `ba`, `wa`
* amend e.g. `[height<=480]` to limit video resolution
* amend e.g. `[ext=mp4]` or `[ext=m4a]` to specify file format
* multiple options separated by `/`
* see [formats](https://github.com/yt-dlp/yt-dlp#format-selection)

* `-k` to keep single sepearate streams, e.g. the audio
* `-x` to download only the audio
* `--write-all-thumbnails`


```
yt-dlp -f 140-1+398 -k https://youtu.be/5zZzjwl-m5A
yt-dlp -f 233-1+398 -k https://youtu.be/5zZzjwl-m5A

# Norbert Bluem
yt-dlp -f "140-1+140-0+136" -k https://youtu.be/qkREtUPnO2k

yt-dlp -f "bv[height<=720]+ba" -k https://youtu.be/qkREtUPnO2k

yt-dlp -f "bv[ext=mp4][height<=720]+ba[ext=m4a][language=de]/bv[ext=mp4][height<=720]+ba[ext=m4a][language=de-DE]" https://youtu.be/qkREtUPnO2k

yt-dlp -f "bv*+ba[language=de]+ba[language=en]" URL

```

Twitter/X Space

direct call produces lots of noise
```
yt-dlp https://x.com/i/spaces/1jGXggOwOMEKZ
```

grepping out the noise
```
yt-dlp https://x.com/i/spaces/1jGXggOwOMEKZ 2>&1 |grep -v "for reading$"
```

utilizing `down_x_space` python script and bash function filtering the noise
```
down_x_space https://x.com/i/spaces/1jGXggOwOMEKZ
```


## alternative downloader GUIs

* [Open Video Downloader](https://github.com/StefanLobbenmeier/youtube-dl-gui)
* [ClipGrab](https://github.com/hayguen/clipgrab)


## alternative download sites

* [circleboom](https://circleboom.com/social-media-scheduler/social-media-video-downloader/twitter-spaces-downloader-free)
* [spacedownloader](https://spacedownloader.io/)
* [spacesdown](https://spacesdown.com/)

* [turboscribe](https://turboscribe.ai/de/downloader/twitter/spaces)
* [twitterspacegpt](https://www.twitterspacegpt.com/downloaders)
* [flowjin](https://www.flowjin.com/tools/twitter-spaces-downloader)


* [reddit:how-do-i-download](https://www.reddit.com/r/DataHoarder/comments/1kelwxu/how_do_i_download_a_twitter_space/)
* [space-off](https://space.offmylawn.xyz/)
* [xspacedownloader](https://digitacanvas.com/xspacedownloader/)

* [Blog:Howto-transcribe](https://spacesrecorder.com/blog/how-to-transcribe-twitter-spaces)


GitHub

* [xspacedownloader](https://github.com/davidww11/xspacedownloader)
* [auto-twitter-space](https://github.com/Spicadox/auto-twitter-space)
