
# TTS - Text to Speech

## Quellen

* https://ttsreader.com/de/
* https://quick-tts.com/de/
* https://www.narakeet.com/languages/text-vorlesen-lassen/
* https://readloudly.com/de/text-to-speech/
* https://www.canva.com/de_de/funktionen/text-to-speech/
* https://speechify.com/de/text-to-speech-online/



* https://github.com/OHF-voice/piper1-gpl
* https://github.com/mevdschee/piper-voices-tts
* https://rhasspy.github.io/piper-samples/#de_DE-kerstin-medium
* https://huggingface.co/rhasspy/piper-voices/tree/main/de/de_DE
* https://docs.sunfounder.com/projects/pidog/de/latest/ai_interaction/python_tts_piper_openai.html
* https://www.reddit.com/r/linux4noobs/comments/1pteudw/how_to_install_and_use_piper_tts_or_uhhh_software/?tl=de
* live: https://piper.ttstool.com/


* https://supertonictts.com/
* https://huggingface.co/supertone-oss-archive/supertonic-3
* https://github.com/supertone-oss-archive/supertonic
* F-Droid: https://f-droid.org/en/packages/com.brahmadeo.supertonic.tts/
* live:  https://huggingface.co/spaces/Supertone/supertonic-3


```
pip install supertonic
from supertonic import TTS

tts = TTS(auto_download=True)
style = tts.get_voice_style(voice_name="M1")
wav, duration = tts.synthesize("Hello from Supertonic.", voice_style=style, lang="en")
tts.save_audio(wav, "output.wav")
```



* https://easyspeak.dev/latest/installation/


* https://github.com/gnat/text-to-speech-ubuntu

* https://www.reddit.com/r/gnome/comments/1rpppl3/packaged_speechproviderpiper_for_debian_fedora/

* https://www.google.com/search?q=wie+ist+es+m%C3%B6glich+den+Fortschritt+bzgl.+abgespielter+Worte+des+TTS+piper+zu+verfolgen%3F&oq=wie+ist+es+m%C3%B6glich+den+Fortschritt+bzgl.+abgespielter+Worte+des+TTS+piper+zu+verfolgen%3F&gs_lcrp=EgZjaHJvbWUyBggAEEUYOdIBCjIzNDc1ajBqMTWoAgiwAgHxBQbboXgbZq4n&client=ubuntu-chr&sourceid=chrome&source=chrome.rb&ie=UTF-8

