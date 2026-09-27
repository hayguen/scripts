#!/usr/bin/env python3

from dotenv import dotenv_values
from typing import Final

# Load variables from the '.env' into dict
config: Final = dotenv_values()

# Access environment variables
HF_TOKEN: Final = config.get("HF_TOKEN", "")
if not HF_TOKEN:
    # 1- https://huggingface.co/join
    # 2- add / register
    #  https://huggingface.co/pyannote/speaker-diarization-community-1/resolve/main/config.yaml
    # 3- create/copy Access Token (profile)  and paste here
    print("Huggingface access token necessary")
    print("add/register at https://huggingface.co/join")
    print("  https://huggingface.co/pyannote/speaker-diarization-community-1/resolve/main/config.yaml")
    print("create/copy Access Token (profile)  and paste here")
    assert False

import sys
import time
import whisperx
import gc
from whisperx.diarize import DiarizationPipeline
from datetime import datetime
from pathlib import Path

print(10*"=" + " 1")


# vorheriges Zuschneiden:
# https://superuser.com/questions/758943/ffmpeg-cut-for-time-range
# ffmpeg -i input.aac -c:v copy -c:a aac output.mp4
# ffmpeg -ss 05:21:00 -i input.m4a -t 03:29:00 -acodec copy output.mp4
#
# ffmpeg -i input.aac -c:v copy -c:a aac output.mp4
# ffmpeg -ss 00:34:00 -i input.mp4 -t 01:38:00 -acodec copy output.mp4

# . ~/sys_venv/bin/activate
# . ~/py314-venv/bin/activate
# OMP_NUM_THREADS=4 transcribex.py <audio_file> auto|de|en
#
# https://github.com/m-bain/whisperx
#
# pip3 install whisperx
#
# pip uninstall transformers tokenizers -y
# pip install transformers==4.41.2 tokenizers==0.19.1
#
# for cuda
#   pip install gpustat
#   pip install nvitop
#   nvidia-smi
#   watch -n 2 nvidia-smi
#   gpustat --no-header
#   nvitop
#

all_lang = [ "auto", "de", "en", "fr" ]
#                 0      1
all_devices = ["cuda", "cpu"]
#                0      1        2         3        4        5         6          7           8
all_models = ["tiny", "base", "small", "medium", "turbo", "large", "large-v2", "large-v3", "large-v3-turbo"]
#                0         1                2               3             4            5         6        7
all_quants = ["int8", "int8_bfloat16", "int8_float16", "int8_float32", "bfloat16", "float16", "int16", "float32"]


# https://openwhispr.com/blog/whisper-model-sizes-explained
# https://whisper-api.com/blog/models/
# "tiny", "base", "small", "medium", "turbo", "large-v2", "large-v3", "large-v3-turbo"
dflt_device = config.get("TRANSCRIPTION_DEVICE", "cpu")
model_s = config.get("TRANSCRIPTION_MODEL", "turbo")
dflt_quant = config.get("TRANSCRIPTION_QUANTIZATION", "int16")
dflt_lang = "auto"
batch_size = 8 # reduce if low on GPU mem; 16 for cpu: ok

#  benchmarks an perf-test.mp4 der Länge 00:27:27 auf Lenovo ThinkCentre, NVIDIA GeForce RTX 3050, 6 GB
#    lspci: NVIDIA Corporation GA107 [GeForce RTX 3050 6GB] (rev a1)
#    lscpu: Intel(R) Core(TM) i7-7700 CPU @ 3.60GHz
#
#  medium:
#      cuda (batch_size = 16)
#          4 -> out of memory
#      cuda (batch_size = 8)
#          7 -> 
#          5 -> OK OK OK OK: 158 sec == 00:02:43
#          4 -> OK OK OK OK: 162 sec == 00:02:48
#      cuda (batch_size = 1)
#          7 -> out of memory
#          5 -> OK OK OK OK: 182 sec == 00:03:07
#          4 -> OK OK OK OK: 190 sec == 00:03:15
#
#  turbo:
#      cuda (batch_size = 16)
#          7 -> out of memory
#          6 -> not available
#          5 -> OK OK OK OK: 150 sec == 00:02:35
#          4 -> OK OK OK OK: 155 sec == 00:02:40
#      cpu (batch_size = 8)
#          7 -> OK OK OK OK: 2261 sec == 00:37:47 (gleiches Ergebnis wie large-v3-turbo, 7)
#          6 -> OK OK OK OK: 2249 sec == 00:37:34
#      cuda (batch_size = 8)
#          7 -> out of memory
#          5 -> OK OK OK OK: 151 sec == 00:02:36
#          4 -> OK OK OK OK: 154 sec == 00:02:40
#      cuda (batch_size = 1)
#          7 -> cuFFT error: CUFFT_INTERNAL_ERROR
#
#  large-v3-turbo:
#      cpu  (batch_size = 8)
#          7 -> OK OK OK OK: 2091 sec == 00:34:56 (gleiches Ergebnis wie turbo, 7)
#
#  large-v3:
#      cpu  (batch_size = 8)
#          7 -> OK OK OK OK: 2259 sec == 00:37:47
#
#  large-v2:
#      cpu  (batch_size = 16)
#          6 -> OK OK: 3620 sec == 01:00:20 / 1h
#      cuda (batch_size = 16)
#          6 -> not available
#          7..1 -> out of memory
#      cuda (batch_size = 12)
#          6 -> backend do not support efficient int16 computation
#          7,5,4 -> out of memory
#      cuda (batch_size = 8)
#          7,5 -> out of memory
#      cuda (batch_size = 6)
#          5 -> out of memory
#      cuda (batch_size = 4)
#          5,5 -> out of memory
#      cuda (batch_size = 2)
#          5,4 -> out of memory; torch.OutOfMemoryError später
#          2 -> OK OK OK OK OK  --> 221 sec == 00:03:46
#          1 -> OK OK OK OK OK  --> 219 sec == 00:03:39
#          0 -> OK OK OK OK OK  --> 217 sec == 00:03:42  == wie 1)
#      cuda (batch_size = 1)
#          5,4 -> out of memory; torch.OutOfMemoryError später
#          2 -> OK OK OK OK OK  --> 225 sec == 00:03:50
#          1 -> OK OK OK OK OK  --> 223 sec == 00:03:48
#          0 -> OK OK OK OK OK  --> 228 sec == 00:03:53


def usage():
    # print(f"have {len(sys.argv)} args")
    print("")
    print("")
    print("missing audio file and transcript arguments!")
    print(f"usage: {sys.argv[0]} <audio input file> [[lang=]<lang>] [out=<transcript output file>|off=<sec_offset>|batch=<size>|<device>|<model>|<quantization>|help]*")
    print(f"language: 'auto', 'fr', 'de', .., 'lang=..', default: '{dflt_lang}'")
    print(f"sec_offset: add given offset (in seconds) to output times")
    print(f"batch:  sets batch size, default: {batch_size}")
    print(f"device in {all_devices} , default: '{dflt_device}'")
    print(f"model in {all_models} , default: '{model_s}'")
    print(f"quantization in {all_quants} , default: '{dflt_quant}'")
    print(f"    float32:  exponent: 8 bits, mantissa: 23 bits")
    print(f"    float16:  exponent: 5 bits, mantissa: 10 bits")
    print(f"    bfloat16: exponent: 8 bits, mantissa:  7 bits")
    sys.exit(0)

if len(sys.argv) < 2:
    usage()

narg = 1
audio_file = sys.argv[narg]
narg = narg + 1

lang_s = dflt_lang
transcript_file = str( Path(audio_file).with_suffix(".txt") )
sec_offset = 0
device_s = dflt_device
model_s = all_models[4]  # "turbo"
quant_s = dflt_quant


while True:  # CLI parsing
    if narg >= len(sys.argv):
        break

    # lang_s = sys.argv[narg] if narg < len(sys.argv) else dflt_lang
    if sys.argv[narg] in all_lang:
        lang_s = sys.argv[narg]
        narg = narg + 1
        continue
    elif sys.argv[narg].startswith("lang="):
        lang_s = sys.argv[narg][5:]
        narg = narg + 1
        if lang_s not in all_lang:
            print("warning: unknown language!")
        continue

    # transcript_file = sys.argv[narg] if (narg < len(sys.argv) and len(sys.argv[narg])) else audio_file + ".txt"
    if sys.argv[narg].startswith("out="):
        transcript_file = sys.argv[narg][4:]
        narg = narg + 1
        continue

    # sec_offset = int(sys.argv[narg]) if narg < len(sys.argv) else 0.0
    if narg < len(sys.argv) and sys.argv[narg].startswith("off="):
        sec_offset = int( sys.argv[narg][4:] )
        narg = narg + 1
        continue

    # device_s = sys.argv[narg] if narg < len(sys.argv) else dflt_device
    if sys.argv[narg] in all_devices:
        device_s = sys.argv[narg]
        narg = narg + 1
        if device_s == "cuda":
            batch_size = 8
            quant_s = "float16"
        elif device_s == "cpu":
            batch_size = 16
            quant_s = "int16"
        else:
            print(f"warning: unknown device!")
        print(f"{device_s} -> {batch_size=}, {quant_s=}")
        continue

    if sys.argv[narg] in all_models:
        model_s = sys.argv[narg]
        narg = narg + 1
        continue

    # quant_s = sys.argv[narg] if narg < len(sys.argv) else dflt_quant
    if sys.argv[narg] in all_quants:
        quant_s = sys.argv[narg]
        narg = narg + 1
        continue

    if sys.argv[narg].startswith("batch="):
        batch_size = int( sys.argv[narg][6:] )
        narg = narg + 1
        continue

    if sys.argv[narg] == "help":
        usage()
    break


if transcript_file == audio_file:
    transcript_file = transcript_file + ".txt"
print(f"{lang_s=}")
print(f"{audio_file=}")
print(f"{transcript_file=}")
print(f"{sec_offset=}")
print(f"{batch_size=}")
print(f"{device_s=}")
print(f"{model_s=}")
print(f"{quant_s=}")

print(10*"=" + " 2")

t_start = time.time()

model = whisperx.load_model(model_s, device=device_s, compute_type=quant_s)

dt = round(time.time() - t_start, 2)
print("%.2fs: WhisperModel() created." % dt)

if narg < len(sys.argv) and sys.argv[narg] in ["help", "-help", "-h"]:
    help(model)
    sys.exit(0)
narg = narg + 1

if lang_s == "auto":
    lang_s = None
# segments, info = model.transcribe(audio_file, language=lang_s, beam_size=5)

print(10*"=" + " 3")

audio = whisperx.load_audio(audio_file)

dt = round(time.time() - t_start, 2)
print("%.2fs: load_audio() finished." % dt)

print(10*"=" + " 4")
result = model.transcribe(audio, batch_size=batch_size, language=lang_s)

print("")
dt = round(time.time() - t_start, 2)
print("%.2fs: transcribe() finished." % dt)

print(10*"=" + " 5")

print(30*"*" + " BEFORE ALIGNMENT")
# print(result["segments"]) # before alignment
# for k, v in result.items():
#     if k in ["segments"]:
#         continue
#     print(f"result[{k}]: {v}")
# 
# print(30*"*" + " END RESULTS")


model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device_s)
dt = round(time.time() - t_start, 2)
print("%.2fs: load_align_model() finished." % dt)

# print(f"{metadata=}")
# print(f"{model_a=}")
result = whisperx.align(result["segments"], model_a, metadata, audio, device_s, return_char_alignments=False)

dt = round(time.time() - t_start, 2)
print("%.2fs: align() finished." % dt)

print(30*"*" + " AFTER ALIGNMENT")
# print(result["segments"]) # after alignment

print(30*"*" + " DIARIZE ..")
# 3. Assign speaker labels
diarize_model = DiarizationPipeline(token=HF_TOKEN, device=device_s)

dt = round(time.time() - t_start, 2)
print("%.2fs: DiarizationPipeline() created." % dt)

print(30*"*" + " DIARIZE .. 2")

diarize_segments = diarize_model(audio)
# diarize_model(audio, min_speakers=min_speakers, max_speakers=max_speakers)

dt = round(time.time() - t_start, 2)
print("%.2fs: diarize_model() finished." % dt)

print(30*"*" + " DIARIZE .. 3")

result = whisperx.assign_word_speakers(diarize_segments, result)

dt = round(time.time() - t_start, 2)
print("%.2fs: assign_word_speakers() finished." % dt)

print(30*"*" + " DIARIZE .. 4")
print(diarize_segments)
print(30*"*" + " DIARIZE .. 5")

# sys.exit(0)

with open(transcript_file, "w") as f:
    print(f"# {audio_file=}", file=f)
    print(f"# {device_s=}", file=f)
    print(f"# {model_s=}", file=f)
    print(f"# {batch_size=}", file=f)
    print(f"# {quant_s=}", file=f)
    print(f"# {lang_s=}", file=f)
    print("#", file=f)
    f.flush()

    if False:
        # print(diarize_segments, file=f)
        # print(f"# type(diarize_segments) = {type(diarize_segments)}")
        for idx, row in enumerate(diarize_segments.iterrows()):
            ds = row[1]
            if idx == 0:
                # for idx, col in enumerate(row):
                #     print(f"col {idx}: type {type(col)}")
                # row_label_types = [ str(type(col)) for col in ds.index ]
                # row_s = "\t".join(row_label_types)
                # print(f"label_types: {row_s}")
                row_labels = [ str(col) for col in ds.index ]
                row_labels.insert(0, "")
                row_s = "\t".join(row_labels)
                print(f"# labels: {row_s}", file=f)
            # row_value_types = [ str(type(col)) for col in ds.values ]
            # row_s = "\t".join(row_value_types)
            # print(f"label_types: {row_s}")
            row_tuples = [ str(col) for col in ds.values ]
            row_tuples.insert(0, str(row[0]))
            row_s = "\t".join(row_tuples)
            print(f"# {row_s}", file=f)
        print("#", file=f)
        f.flush()

    dt = round(time.time() - t_start, 2)
    print("# %.2fs: WhisperModel() initialized with audio file." % dt)
    print("# %.2fs: WhisperModel() initialized with audio file." % dt, file=f)
    print("# Detected language '%s'" % (metadata["language"],))
    print("# Detected language '%s'" % (metadata["language"],), file=f)
    print("#", file=f)
    print("#[SPEAKER_NN] SHOWNAME		URL", file=f)
    print("#[SPEAKER_NN] SHOWNAME", file=f)
    print("#", file=f)
    print("#[h1] title .. h1 .. h3 between the lines", file=f)
    print("#", file=f)
    f.flush()

    for segment in result["segments"]:  # segments are now assigned speaker IDs
        start, stop, text, speaker = segment["start"], segment["end"], segment["text"], segment.get("speaker", "SPEAKER_UK")
        # dt = round(time.time() - t_start, 2)
        # print(segment)
        start_off = start + sec_offset
        stop_off = stop + sec_offset
        print("[%.2fs -> %.2fs] %s : %s" % (start_off, stop_off, speaker, text))
        print("[%.2fs -> %.2fs] %s : %s" % (start_off, stop_off, speaker, text), file=f)
        f.flush()

    t_end = time.time()
    print(f"transcription took {round(t_end - t_start, 1)} secs")
    print(f"# transcription took {round(t_end - t_start, 1)} secs", file=f)
    f.flush()
