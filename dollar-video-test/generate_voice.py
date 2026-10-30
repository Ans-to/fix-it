#!/usr/bin/env python3
"""Generate original Kokoro voice clips from local model and am_eric weights.
The model and voice weights are external dependencies, not part of this repo.
"""
import hashlib,json,os
from pathlib import Path
import numpy as np
import onnxruntime as ort
import wave
from kokoro_onnx.tokenizer import Tokenizer

ROOT=Path(__file__).resolve().parent
MODEL=Path(os.environ.get('KOKORO_MODEL','/tmp/kokoro-assets/kokoro-q8.onnx'))
VOICE=Path(os.environ.get('KOKORO_VOICE','/tmp/kokoro-node/node_modules/kokoro-js/voices/am_eric.bin'))
LINES=[
 'Why does so much of the world rely on dollars?',
 'Deep U.S. financial markets make dollars easy to trade and hold.',
 'As more people accept dollars, they become more useful to others.',
 "That helps the dollar lead, but it's not the only global currency.",
]

def main():
    model_hash=hashlib.sha256(MODEL.read_bytes()).hexdigest()
    if model_hash!='fbae9257e1e05ffc727e951ef9b9c98418e6d79f1c9b6b13bd59f5c9028a1478':
        raise RuntimeError('Unexpected model hash: '+model_hash)
    voice=np.fromfile(VOICE,dtype='<f4').reshape(-1,256)
    options=ort.SessionOptions(); options.intra_op_num_threads=4; options.inter_op_num_threads=1
    sess=ort.InferenceSession(str(MODEL),sess_options=options,providers=['CPUExecutionProvider'])
    tokenizer=Tokenizer(); clips=[]
    for i,text in enumerate(LINES):
        phonemes=tokenizer.phonemize(text,'en-us');tokens=tokenizer.tokenize(phonemes)
        ids=np.array([[0,*tokens,0]],dtype=np.int64)
        out=sess.run(None,{'input_ids':ids,'style':voice[min(len(tokens),509)].reshape(1,256).astype(np.float32),'speed':np.array([1.08],np.float32)})[0].reshape(-1)
        # Retain phonetic edges; trim only leading/trailing very low-level silence with padding.
        indices=np.where(np.abs(out)>0.001)[0]
        if len(indices): out=out[max(0,indices[0]-720):min(len(out),indices[-1]+1440)]
        path=ROOT/f'voice-{i+1}.wav'
        pcm=(np.clip(out,-1,1)*32767).astype('<i2')
        with wave.open(str(path),'wb') as w:
            w.setnchannels(1);w.setsampwidth(2);w.setframerate(24000);w.writeframes(pcm.tobytes())
        clips.append({'text':text,'duration_seconds':len(out)/24000,'phonemes':phonemes,'file':path.name})
    info={'engine':'Kokoro-82M-v1.0-ONNX q8, CPU','voice':'am_eric','voice_source':'kokoro-js@1.2.1','voice_sha256':hashlib.sha256(VOICE.read_bytes()).hexdigest(),'model_sha256':model_hash,'speed':1.08,'sample_rate':24000,'clips':clips}
    (ROOT/'voice-metadata.json').write_text(json.dumps(info,indent=2)+'\n')
    print(json.dumps(info,indent=2))
if __name__=='__main__':main()
