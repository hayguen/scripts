
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

```
yt-dlp https://x.com/i/spaces/1jGXggOwOMEKZ
yt-dlp https://x.com/i/spaces/1jGXggOwOMEKZ 2>&1 |grep -v "for reading$"

down_x_space https://x.com/i/spaces/1jGXggOwOMEKZ

```


# FFmpeg

## from Linux distribution

Distri package might be outdated

```
sudo apt install ffmpeg
```

## Precompiled binaries

For updating ffmpeg following packages are needed:

```
sudo apt install tar xz-utils
```

download, unpack and copy to bin/

* https://github.com/BtbN/FFmpeg-Builds
* https://api.github.com/repos/BtbN/FFmpeg-Builds/releases/latest


# CUDA

https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=Ubuntu&target_version=26.04&target_type=deb_local

```
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2604/x86_64/cuda-ubuntu2604.pin
sudo mv cuda-ubuntu2604.pin /etc/apt/preferences.d/cuda-repository-pin-600
wget https://developer.download.nvidia.com/compute/cuda/13.4.2/local_installers/cuda-repo-ubuntu2604-13-4-local_13.4.2-1_amd64.deb
sudo dpkg -i cuda-repo-ubuntu2604-13-4-local_13.4.2-1_amd64.deb
sudo cp /var/cuda-repo-ubuntu2604-13-4-local/cuda-*-keyring.gpg /usr/share/keyrings/
sudo apt-get update
sudo apt-get -y install cuda-toolkit-13-4

pip install nvidia-cuda-runtime
pip install nvidia-cublas nvidia-cuda-cccl nvidia-cuda-cupti nvidia-cuda-nvcc nvidia-cuda-nvrtc nvidia-cuda-opencl nvidia-cuda-runtime nvidia-cuda-sanitizer-api nvidia-cufft nvidia-curand nvidia-cusolver nvidia-cusparse nvidia-npp nvidia-nvfatbin nvidia-nvjitlink nvidia-nvjpeg nvidia-nvml-dev nvidia-nvtx
```

```
# terminal / profile
#   shell, custom command:  bash --init-file ~/.bashrc-voicedet_python
export PATH=${PATH}:/usr/local/cuda-13.4/bin
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/local/cuda-13.4/lib64
```

```
cd /usr/lib/x86_64-linux-gnu
sudo ln -s libavutil.so.60 libavutil.so.59
```

## monitoring - top

```
pip install gpustat
pip install nvitop

nvidia-smi
watch -n 2 nvidia-smi
gpustat --no-header
nvitop
```

## samples / device info

https://github.com/nvidia/cuda-samples

`/home/ayguen/github/cuda-samples/build/cpp/1_Utilities/deviceQuery`


```
((py314-venv) ) ayguen@lenovotc:/1_Utilities/deviceQuery (master)$ ./deviceQuery 
./deviceQuery Starting...

 CUDA Device Query (Runtime API) version (CUDART static linking)

Detected 1 CUDA Capable device(s)

Device 0: "NVIDIA GeForce RTX 3050"
  CUDA Driver Version / Runtime Version          13.2 / 13.4
  CUDA Capability Major/Minor version number:    8.6
  Total amount of global memory:                 5803 MBytes (6085214208 bytes)
  (018) Multiprocessors, (128) CUDA Cores/MP:    2304 CUDA Cores
  GPU Max Clock rate:                            1492 MHz (1.49 GHz)
  Memory Clock rate:                             7001 Mhz
  Memory Bus Width:                              96-bit
  L2 Cache Size:                                 1572864 bytes
  Maximum Texture Dimension Size (x,y,z)         1D=(131072), 2D=(131072, 65536), 3D=(16384, 16384, 16384)
  Maximum Layered 1D Texture Size, (num) layers  1D=(32768), 2048 layers
  Maximum Layered 2D Texture Size, (num) layers  2D=(32768, 32768), 2048 layers
  Total amount of constant memory:               65536 bytes
  Total amount of shared memory per block:       49152 bytes
  Total shared memory per multiprocessor:        102400 bytes
  Total number of registers available per block: 65536
  Warp size:                                     32
  Maximum number of threads per multiprocessor:  1536
  Maximum number of threads per block:           1024
  Max dimension size of a thread block (x,y,z): (1024, 1024, 64)
  Max dimension size of a grid size    (x,y,z): (2147483647, 65535, 65535)
  Maximum memory pitch:                          2147483647 bytes
  Texture alignment:                             512 bytes
  Concurrent copy and kernel execution:          Yes with 2 copy engine(s)
  Run time limit on kernels:                     Yes
  Integrated GPU sharing Host Memory:            No
  Support host page-locked memory mapping:       Yes
  Alignment requirement for Surfaces:            Yes
  Device has ECC support:                        Disabled
  Device supports Unified Addressing (UVA):      Yes
  Device supports Managed Memory:                Yes
  Device supports Compute Preemption:            Yes
  Supports Cooperative Kernel Launch:            Yes
  Device PCI Domain ID / Bus ID / location ID:   0 / 1 / 0
  Compute Mode:
     < Default (multiple host threads can use ::cudaSetDevice() with device simultaneously) >

deviceQuery, CUDA Driver = CUDART, CUDA Driver Version = 13.2, CUDA Runtime Version = 13.4, NumDevs = 1
Result = PASS
```
