"""Forced-align a scene's known transcript against its 16 kHz PCM waveform.

PocketSphinx alignment estimates acoustic boundaries; it is not a substitute
for manual review, especially for unusual words or noisy speech.
"""
import json
import re
import sys
import wave

from pocketsphinx import Decoder

wav_path, text = sys.argv[1:3]
words = text.lower().split()
decoder = Decoder(loglevel="ERROR", samprate=16000)
missing = [word for word in words if not decoder.lookup_word(word)]
if missing:
    raise SystemExit("Words not in PocketSphinx's dictionary: " + ", ".join(missing))
decoder.set_align_text(" ".join(words))
with wave.open(wav_path, "rb") as audio:
    if audio.getframerate() != 16000 or audio.getnchannels() != 1 or audio.getsampwidth() != 2:
        raise SystemExit("Expected mono 16-bit PCM at 16 kHz")
    pcm = audio.readframes(audio.getnframes())
decoder.start_utt()
decoder.process_raw(pcm, full_utt=True)
decoder.end_utt()
segments = []
for item in decoder.seg():
    word = re.sub(r"\(\d+\)$", "", item.word)
    if word not in ("<s>", "</s>", "<sil>"):
        segments.append({"word": word, "startSeconds": item.start_frame / 100, "endSeconds": (item.end_frame + 1) / 100})
if [segment["word"] for segment in segments] != words:
    raise SystemExit(f"Alignment word mismatch: {segments}")
print(json.dumps(segments))
