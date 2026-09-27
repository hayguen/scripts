
# CUDA

see [cuda.md](cuda.md)

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

## tutorials / info

* Lokale KI: Wo lokale Modelle Claude und ChatGPT schlagen, zum Bruchteil des Preises
  * https://gerlinger.ai/blog/lokale-ki-installieren-anleitung
  * https://youtu.be/6HJki9Z4l8U
* LM Studio
  * https://lmstudio.ai/
  * https://lmstudio.ai/taderich73/filesystem-access
* GPT4ALL
  * https://linuxconfig.org/how-to-install-gpt4all-on-ubuntu-debian-linux
  * https://dev.to/vultr/installing-gpt4all-an-open-source-chatbot-application-for-running-llms-38dk


## samples / device info

models

* 6 / 8 GB: https://www.nvidia.com/de-de/geforce/graphics-cards/30-series/rtx-3050/
* 24 GB: https://www.nvidia.com/de-de/geforce/graphics-cards/30-series/rtx-3090-3090ti/
* 24 GB: RTX 4090: https://www.nvidia.com/de-de/geforce/graphics-cards/40-series/
* 16 GB: https://www.nvidia.com/de-de/geforce/graphics-cards/50-series/rtx-5060-family/
  * https://www.amazon.de/dp/B0F8BR2H6Z/?th=1
* 16 GB: https://www.nvidia.com/de-de/geforce/graphics-cards/50-series/rtx-5070-family/
  * https://www.amazon.de/dp/B0DV9GC9SR/?th=1
* 16 GB: https://www.nvidia.com/de-de/geforce/graphics-cards/50-series/rtx-5080/
* 32 GB: https://www.nvidia.com/de-de/geforce/graphics-cards/50-series/rtx-5090/


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
