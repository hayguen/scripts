
# Python environment for whisperx, torch, ..

small scripts and setup of python environment

```
git clone https://github.com/hayguen/scripts.git
```

copy files from bin to $HOME/bin/, copy files from rc to $HOME/rc/

the environment can be used - after setup - with

```
. ~/py313/bin/activate
```

or

```
. ~/rc/rc-voicedet_python
```

## Setup python venv

need older versions - for incompatibilities of whisperx 3.8.6 and python3.14

```
sudo apt install python3

sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install -y python3.13 python3.13-venv

cd $HOME  # to setup py313 venv in $HOME/py313
python3.13 -m venv py313
. ~/py313/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# ..

deactivate
```

# yt-dlp downloader

setup, usage: see [yt-dlp.md](yt-dlp.md)


# FFmpeg

setup, usage, applications: [ffmpeg.md](ffmpeg.md)


# CUDA

required for GPU computations, see [cuda.md](cuda.md)
