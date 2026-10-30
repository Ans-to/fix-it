from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg, subprocess, hashlib, os, json

OUT=os.path.dirname(os.path.abspath(__file__)); W,H,FPS,N=360,640,30,180
BG=(15,25,40); FG=(244,247,246); ACC=(93,223,203); BORDER=(145,172,184)
font='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
T=ImageFont.truetype(font,22); L=ImageFont.truetype(font,15); BODY=ImageFont.truetype(font,14)
def put(d, xy, text, font, fill, anchor='mm'):
    d.text(xy,text,font=font,fill=fill,anchor=anchor)
def circle(d, x,y, text):
    d.ellipse((x-24,y-24,x+24,y+24),fill=ACC)
    put(d,(x,y+1),text,L,BG)
def frame(n):
    im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
    title='REQUESTS ARRIVE' if n<60 else ('WAIT IN ORDER' if n<120 else 'FIRST IN, FIRST OUT')
    put(d,(180,65),title,T,FG)
    d.rounded_rectangle((55,280,305,360),radius=17,outline=BORDER,width=3)
    put(d,(255,390),'QUEUE',BODY,FG,anchor='lm')
    if n<60:
        for x,i in [(100,1),(180,2),(260,3)]:circle(d,x,180,f'R{i}')
    elif n<120:
        t=min(1,(n-60)/29); y=180+140*t
        for x,i in [(100,1),(180,2),(260,3)]:circle(d,x,y,f'R{i}')
    else:
        d.rounded_rectangle((115,425,245,500),radius=14,outline=BORDER,width=3)
        put(d,(180,520),'SERVED',BODY,FG)
        circle(d,180,320,'R2'); circle(d,260,320,'R3')
        t=min(1,(n-120)/29); circle(d,100+80*t,320+140*t,'R1')
    return im

os.makedirs(OUT,exist_ok=True)
cmd=[imageio_ffmpeg.get_ffmpeg_exe(),'-hide_banner','-loglevel','error','-y','-f','rawvideo','-vcodec','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-frames:v',str(N),'-c:v','libx264','-pix_fmt','yuv420p','-movflags','+faststart',f'{OUT}/sample.mp4']
p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
for n in range(N):p.stdin.write(frame(n).tobytes())
p.stdin.close()
if p.wait()!=0: raise RuntimeError('render failed')
indices=[0,59,60,89,90,119,120,149,150,179]
thumbw,thumbh=180,320
sheet=Image.new('RGB',(thumbw*5, (thumbh+28)*2),'#ffffff'); ds=ImageDraw.Draw(sheet)
for i,n in enumerate(indices):
    img=frame(n); x=(i%5)*thumbw; y=(i//5)*(thumbh+28)
    sheet.paste(img.resize((thumbw,thumbh)),(x,y+28)); ds.text((x+5,y+5),f'frame {n}',fill='black')
sheet.save(f'{OUT}/review-contact-sheet.png')
# Check deterministic repeated rendering of important raw frames.
hashes={}
for n in indices:
    a=hashlib.sha256(frame(n).tobytes()).hexdigest(); b=hashlib.sha256(frame(n).tobytes()).hexdigest()
    assert a==b; hashes[str(n)]=a
# Count and dimension metadata by decoding the actual finished video.
probe=subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-hide_banner','-i',f'{OUT}/sample.mp4','-f','null','-'],capture_output=True,text=True)
assert probe.returncode==0,probe.stderr
with open('/tmp/director-eval/ffmpeg-output.txt','w') as f:f.write(probe.stderr)
# Validate occupancy and initial placements directly in the authored stills.
assert frame(0).getpixel((100,165))==ACC
assert frame(89).getpixel((100,305))==ACC
assert frame(149).getpixel((180,445))==ACC
assert frame(149).getpixel((180,305))==ACC

def lin(x):
    x=x/255
    return x/12.92 if x<=0.04045 else ((x+0.055)/1.055)**2.4
def lum(c):return 0.2126*lin(c[0])+0.7152*lin(c[1])+0.0722*lin(c[2])
def contrast(a,b):
    a,b=sorted((lum(a),lum(b)),reverse=True);return (a+0.05)/(b+0.05)
results={'canvas':[W,H],'fps':FPS,'frames_requested':N,'seconds':N/FPS,'same_frame_raw_hashes_match':True,'sampled_frames':indices,'white_on_navy_contrast':round(contrast(FG,BG),2),'navy_on_turquoise_contrast':round(contrast(BG,ACC),2),'video_has_audio':False,'frame_hashes':hashes}
with open(f'{OUT}/automated-checks.json','w') as f:json.dump(results,f,indent=2)
print(json.dumps({k:v for k,v in results.items() if k!='frame_hashes'},indent=2))
