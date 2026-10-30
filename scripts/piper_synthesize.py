"""Load a Piper voice once and synthesize each input word to a WAV file."""
import json
import pathlib
import sys
import wave

from piper import PiperVoice

model, config, output_dir = sys.argv[1:4]
words = json.load(sys.stdin)
voice = PiperVoice.load(model, config_path=config)
for index, word in enumerate(words):
    output = pathlib.Path(output_dir) / f"{index}.wav"
    with wave.open(str(output), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(voice.config.sample_rate)
        for chunk in voice.synthesize(word):
            wav.writeframes(chunk.audio_int16_bytes)
