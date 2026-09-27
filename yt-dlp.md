
# YT-DLP - downloader for media files

usable for YouTube, Twitter/X and many more

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

download giving formats audio+video with `+`

`-k` to keep single sepearate streams, e.g. the audio

option: `--write-all-thumbnails`

```
yt-dlp -f 140-1+398       -k https://youtu.be/5zZzjwl-m5A
yt-dlp -f 233-1+234-1+398 -k https://youtu.be/5zZzjwl-m5A
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
