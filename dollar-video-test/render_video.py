#!/usr/bin/env python3
"""Original screen-space Pillow renderer, deterministic at each frame.
Profile: dollar-pillow-profile-1.0.0; see visual-plan.json and production-plan.md.
"""
import argparse,json,math,os,subprocess,sys
from functools import lru_cache
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont

P=Path(__file__).resolve().parent
PLAN=json.loads((P/'visual-plan.json').read_text())
W,H=PLAN['format']['width'],PLAN['format']['height'];FPS=PLAN['format']['fps']
C=PLAN['colors']; bg=C['paper']; ink=C['ink'];blue=C['blue'];cream=C['cream'];muted=C['muted'];gold=C['gold']

@lru_cache(None)
def font(which,size,weight='Regular'):
    files={'display':'Anton-Regular.ttf','body':'Manrope-Variable.ttf','mono':'IBMPlexMono-Regular.ttf'}
    f=ImageFont.truetype(str(P/'fonts'/files[which]),size)
    if which=='body': f.set_variation_by_name(weight)
    return f

def rgb(hexstr):return tuple(int(hexstr[i:i+2],16) for i in (1,3,5))
def blend(a,b,t):
    a,b=rgb(a),rgb(b);return tuple(round(x*(1-t)+y*t) for x,y in zip(a,b))
def clamp(x):return max(0.,min(1.,x))
def smooth(x):
    x=clamp(x);return x*x*(3-2*x)
def ease_out(x):
    x=clamp(x);return 1-(1-x)**3

def background():
    im=Image.new('RGB',(W,H),bg);d=ImageDraw.Draw(im)
    # A restrained editorial grid, deliberately non-data-bearing.
    for x in range(90,1000,90):d.line((x,215,x,1425),fill='#E9E8E1',width=1)
    for y in range(245,1430,90):d.line((90,y,990,y),fill='#E9E8E1',width=1)
    for y in range(245,1430,180):
        for x in range(90,1000,180): d.ellipse((x-2,y-2,x+2,y+2),fill='#D6D9D2')
    return im
BASE=background()

class Canvas:
    def __init__(self,img):self.image=img;self.d=ImageDraw.Draw(img);self.boxes=[]
    def text(self,xy,text,which,size,fill,weight='Regular',anchor='lt',track=True):
        f=font(which,size,weight);box=self.d.textbbox(xy,text,font=f,anchor=anchor)
        if track:
            if box[0]<0 or box[1]<0 or box[2]>W or box[3]>H: raise ValueError(f'text outside canvas {text!r}: {box}')
            self.boxes.append((text,box))
        self.d.text(xy,text,font=f,fill=fill,anchor=anchor)
        return box
    def rrect(self,box,r,fill,outline=None,width=1):self.d.rounded_rectangle(box,radius=r,fill=fill,outline=outline,width=width)
    def line(self,xy,fill,width=1):self.d.line(xy,fill=fill,width=width)
    def ellipse(self,box,fill=None,outline=None,width=1):self.d.ellipse(box,fill=fill,outline=outline,width=width)

def header(c,s):
    c.text((94,135),'FIELD NOTES  /  GLOBAL FINANCE','mono',25,ink)
    c.text((985,135),s['number']+' / 04','mono',25,ink,anchor='rt')
    c.line((94,186,986,186),ink,2)
    c.text((94,233),s['eyebrow'],'mono',25,blue)
    c.rrect((890,226,985,265),19,ink)
    c.text((937,234),'15 SEC','mono',17,cream,anchor='mt')

def title(c,s,local):
    p=.7+.3*ease_out(local/17)
    for i,line in enumerate(s['headline']):
        yy=320+i*169
        ff=font('display',152)
        # Retain consistent visual hierarchy while fitting each actual string.
        size=152
        while c.d.textlength(line,font=font('display',size))>895:size-=2
        c.text((94-round(25*(1-p)),yy),line,'display',size,blend(bg,ink,p))
    c.rrect((96,677,164,686),4,blue)
    c.line((180,681,986,681),'#C5CBC7',2)

def question(c,local):
    p=smooth((local-4)/22); cx,cy=540,1055; r=round(225*p)
    if r>0:
        c.ellipse((cx-r,cy-r,cx+r,cy+r),fill=ink)
        if r>18:c.ellipse((cx-r+18,cy-r+18,cx+r-18,cy+r-18),outline='#385269',width=2)
        for j in range(3):
            rr=250+j*37
            c.d.arc((cx-rr,cy-rr*.73,cx+rr,cy+rr*.73),start=195+j*13,end=345+j*13,fill=blend(bg,blue,p*.7),width=3)
            c.d.arc((cx-rr,cy-rr*.73,cx+rr,cy+rr*.73),start=15+j*13,end=165+j*13,fill=blend(bg,blue,p*.7),width=3)
        if p>.72:c.text((cx,cy-129),'$','display',248,cream,anchor='mt')
        theta=local*.036
        for i in range(3):
            a=theta+i*math.tau/3;x=cx+math.cos(a)*295;y=cy+math.sin(a)*210
            c.ellipse((x-9,y-9,x+9,y+9),fill=blue if i!=1 else gold)
    c.text((540,1367),'ONE CURRENCY. MANY CONNECTIONS.','mono',24,muted,anchor='mt')

def markets(c,local):
    c.text((109,755),'A LIQUID MARKET, SIMPLIFIED','mono',23,muted)
    rows=[('01','BUY','ACCESS'),('02','SELL','EXCHANGE'),('03','HOLD','RESERVES')]
    for i,(num,label,right) in enumerate(rows):
        p=ease_out((local-5-i*8)/19)
        if p<=0:continue
        x=115+round((1-p)*32);y=817+i*160
        fill=blend(bg,cream,p); edge=blend(bg,'#CBD2CF',p)
        c.rrect((x,y,x+850,y+130),22,fill,edge,2)
        c.text((x+28,y+24),num,'mono',20,blend(bg,muted,p))
        c.text((x+94,y+20),label,'body',52,blend(bg,ink,p),'ExtraBold')
        c.text((x+96,y+83),right,'mono',20,blend(bg,muted,p))
        c.rrect((x+620,y+25,x+805,y+105),40,blend(bg,ink,p))
        c.text((x+712,y+40),'USD','body',31,blend(bg,cream,p),'Bold',anchor='mt')
    c.text((540,1367),'ILLUSTRATIVE MARKET ACTIVITY','mono',24,muted,anchor='mt')

def network(c,local):
    cx,cy=540,1063
    positions=[(290,900),(790,900),(290,1220),(790,1220)]
    activ=[smooth((local-6)/14),smooth((local-18)/14),smooth((local-39)/14),smooth((local-57)/14)]
    for (x,y),p in zip(positions,activ):
        if p<=0:continue
        c.line((cx,cy,x,y),blend(bg,blue,p*.75),5)
    c.ellipse((cx-84,cy-84,cx+84,cy+84),fill=ink)
    c.text((cx,cy-34),'USD','body',42,cream,'ExtraBold',anchor='mt')
    for idx,((x,y),p) in enumerate(zip(positions,activ)):
        r=round(58*p)
        if r<3:continue
        c.ellipse((x-r,y-r,x+r,y+r),fill=cream,outline=blend(bg,blue,p),width=4)
        if p>.8:c.text((x,y-23),chr(65+idx),'body',32,ink,'Bold',anchor='mt')
    # A traveling marker makes the added connection observable, not evidence of actual transactions.
    if local>60:
        # A new participant D opens a route back to A, illustrating the benefit.
        a=min(1,(local-60)/38)
        start=positions[3];end=positions[0]
        if a<.5:
            t=a*2;x=start[0]+(cx-start[0])*t;y=start[1]+(cy-start[1])*t
        else:
            t=(a-.5)*2;x=cx+(end[0]-cx)*t;y=cy+(end[1]-cy)*t
        c.ellipse((x-8,y-8,x+8,y+8),fill=gold)
    if local>=75:c.text((540,1330),'A CAN CONNECT WITH D','mono',24,ink,anchor='mt')
    c.text((540,1370),'ILLUSTRATIVE NETWORK MODEL','mono',22,muted,anchor='mt')

def payoff(c,local):
    p=ease_out((local-3)/19); dx=round((1-p)*20)
    c.rrect((115+dx,803,965+dx,1085),30,blend(bg,ink,p))
    if p>.68:
        c.text((160,844),'USD','display',112,cream)
        c.text((163,1008),'LEADING GLOBAL CURRENCY','mono',23,'#C5D5DF')
        c.ellipse((811,872,911,972),fill=blue)
        c.text((861,886),'$','display',58,cream,anchor='mt')
    p2=ease_out((local-27)/18)
    if p2>0:
        c.rrect((115,1133,965,1275),24,blend(bg,cream,p2),blend(bg,'#C8CFCC',p2),2)
        c.text((151,1155),'OTHER CURRENCIES','mono',22,blend(bg,muted,p2))
        c.text((151,1190),'EUR  /  JPY  /  OTHERS','body',34,blend(bg,ink,p2),'Bold')
    c.text((540,1367),'LEADING DOES NOT MEAN ONLY','mono',24,muted,anchor='mt')

def captions(c,s,frame):
    if not s['caption_start']<=frame<s['caption_end']: return
    # Caption panel is a project placement proposal, not a verified platform safe zone.
    x0,y0,x1,y1=84,1510,996,1674
    c.rrect((x0,y0,x1,y1),22,ink)
    for i,line in enumerate(s['caption']):
        b=c.text((540,1536+i*53),line,'body',38,cream,'Bold',anchor='mt')
        if b[0]<x0+24 or b[2]>x1-24 or b[1]<y0+14 or b[3]>y1-14:
            raise ValueError(f'caption overflows panel: {line}: {b}')

def frame_image(frame):
    if not 0<=frame<PLAN['format']['total_frames']:raise ValueError('frame out of range')
    s=next(s for s in PLAN['scenes'] if s['start']<=frame<s['end']);local=frame-s['start']
    image=BASE.copy();c=Canvas(image);header(c,s);title(c,s,local)
    {'question':question,'markets':markets,'network':network,'payoff':payoff}[s['id']](c,local)
    captions(c,s,frame)
    return image

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--frame',type=int);ap.add_argument('--output',type=Path);ap.add_argument('--render',action='store_true');a=ap.parse_args()
    if a.frame is not None:
        if not a.output:ap.error('--frame needs --output')
        frame_image(a.frame).save(a.output);return
    if not a.render:ap.error('choose --render or --frame')
    ff=os.environ.get('FFMPEG','/tmp/director-eval-deps/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2')
    output=P/'dollar-test.mp4'
    cmd=[ff,'-hide_banner','-loglevel','warning','-y','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','pipe:0','-i',str(P/'audio-mix.wav'),'-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-threads','3','-c:a','aac','-b:a','192k','-ar','48000','-t','15','-movflags','+faststart',str(output)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    try:
        for n in range(PLAN['format']['total_frames']):
            proc.stdin.write(frame_image(n).tobytes())
            if n%60==0: print(f'rendered {n}/{PLAN["format"]["total_frames"]}',flush=True)
    except BaseException:
        proc.stdin.close();proc.terminate();proc.wait();raise
    proc.stdin.close();code=proc.wait()
    if code:raise RuntimeError(f'ffmpeg returned {code}')
    print(f'Wrote {output}',flush=True)
if __name__=='__main__':main()
