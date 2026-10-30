#!/usr/bin/env python3
"""Construct a new, independent storyboard; no external visual assets are inputs."""
import json, math
from pathlib import Path

def text(id,value,x,y,size=44,color='ivory',group='world',delay=None):
 o={'id':id,'type':'text','value':value,'center':[x,y],'font_px':size,'color':color,'group':group}
 if delay is not None:o['delay']=delay
 return o

def rect(id,x,y,w,h,fill='surface',stroke='slate',delay=6):
 return {'id':id,'type':'rect','xy':[x,y],'size':[w,h],'radius':24,'fill':fill,'stroke':stroke,'stroke_px':3,'group':'world','delay':delay}

def circle(id,x,y,r,fill='surface',stroke='slate',delay=6):
 return {'id':id,'type':'circle','center':[x,y],'radius':r,'fill':fill,'stroke':stroke,'stroke_px':3,'group':'world','delay':delay}

def line(id,x1,y1,x2,y2,color='slate',delay=6):
 return {'id':id,'type':'line','from':[x1,y1],'to':[x2,y2],'color':color,'stroke_px':4,'group':'world','delay':delay}

def joined(id,a,b,delay=6):
 # Start/end two pixels inside the circular outlines. Draw line before nodes.
 dx,dy=b[0]-a[0],b[1]-a[1]; length=math.hypot(dx,dy); ux,uy=dx/length,dy/length
 return line(id,round(a[0]+ux*(a[2]-2),2),round(a[1]+uy*(a[2]-2),2),round(b[0]-ux*(b[2]-2),2),round(b[1]-uy*(b[2]-2),2),delay=delay)

def headers(title,subtitle):return [text('heading',title,540,330,68,'ivory','screen',0),text('subheading',subtitle,540,440,40,'slate','screen',0)]
S=[]
def scene(id,start,end,title,sub,vo,pages,objects,z0=1,z1=1):
 assert len(pages)==2 and ' '.join(line for page in pages for line in page)==vo
 mid=(start+end)//2
 S.append({'id':id,'interval':[start,end],'camera':{'projection':'orthographic','angle_degrees':{'yaw':0,'pitch':0,'roll':0},'zoom_anchor':[540,960],'viewport_center':[540,960],'zoom':[z0,z1]},'voiceover':vo,'caption_timing':'PROVISIONAL; realign to recorded speech','captions':[{'interval':[start,mid],'lines':pages[0]},{'interval':[mid,end],'lines':pages[1]}], 'objects':headers(title,sub)+objects})

scene('01_hook',0,180,'WHY THE DOLLAR?','A SHARED CURRENCY',
 'Why would two countries trade using a currency neither one issues?',
 [['Why would two countries trade','using a currency'],['neither one issues?']],
 [line('trade_path',320,900,760,900),circle('country_a',250,900,70),circle('country_b',830,900,70),
  circle('dollar_token',540,900,50,'gold','gold'),text('dollar_mark','$',540,900,67,'night'),
  text('country_a_label','COUNTRY A',250,1090,40,'slate'),text('country_b_label','COUNTRY B',830,1090,40,'slate')],1,1.02)
for o in S[-1]['objects']:
 if o['id'] in ('dollar_token','dollar_mark'):o['x_motion']={'from':380,'to':700,'local_start':24,'local_end':120}
scene('02_definition',180,390,'A GLOBAL TOOL','LEADING, NOT THE ONLY ONE',
 "The dollar is the leading international currency, used in trade invoicing, finance, and central bank reserves.",
 [['The dollar is the leading','international currency,'],['used in trade invoicing, finance,','and central bank reserves.']],
 [circle('euro_node',265,840,60),circle('yen_node',815,840,60),text('euro','€',265,840,60,'slate'),text('dollar','$',540,840,150,'gold'),text('yen','¥',815,840,60,'slate'),
  rect('card_a',110,1010,275,135,delay=10),rect('card_b',403,1010,275,135,delay=20),rect('card_c',695,1010,275,135,delay=30),
  text('trade','INVOICING',247,1077,38,delay=10),text('finance','FINANCE',540,1077,38,delay=20),text('reserves','RESERVES',833,1077,38,delay=30)],1,1)
scene('03_history',390,600,'A POSTWAR SYSTEM','BRETTON WOODS',
 'In 1944, Bretton Woods placed the dollar at the center of the postwar monetary system.',
 [['In 1944, Bretton Woods placed','the dollar at the center'],['of the postwar','monetary system.']],
 [rect('history_card',150,760,780,330,stroke='gold'),text('year','1944',540,890,155,'gold'),
  text('history_label','POSTWAR FRAMEWORK',540,1030,40,'slate')],1,1.02)
scene('04_gold_link',600,840,'DOLLARS AND GOLD','THE BRETTON WOODS SYSTEM',
 'Participating countries tied their currencies to the dollar, while the U.S. promised gold for dollars held by foreign central banks.',
 [['Participating countries tied','their currencies to the dollar, while'],['the U.S. promised gold for dollars','held by foreign central banks.']],
 [line('left_connector',355,925,420,925),line('right_connector',660,925,725,925),
  rect('currencies_card',100,830,255,190),rect('usd_card',420,830,240,190,stroke='gold'),rect('gold_card',725,830,255,190,stroke='gold'),
  text('currency1','OTHER',227,905,40),text('currency2','MONEY',227,960,40),text('usd','$',540,925,90,'gold'),text('gold','GOLD',852,925,45,'gold'),
  text('officials','FOR CENTRAL BANKS',540,1190,40,'slate')],1,1)
scene('05_1971',840,1050,'GOLD WINDOW CLOSES','1971',
 "In 1971, the United States suspended that gold conversion. Yet the dollar's global role continued.",
 [['In 1971, the United States','suspended that gold conversion.'],["Yet the dollar's global role",'continued.']],
 [line('left_connector',390,920,490,920),line('break_link',490,920,590,920),line('right_connector',590,920,690,920),
  rect('dollar_panel',140,830,250,180,stroke='gold'),rect('gold_panel',690,830,250,180,stroke='gold'),
  text('dollar','$',265,920,90,'gold'),text('gold','GOLD',815,920,44,'gold'),text('status','CONVERSION SUSPENDED',540,1195,42,'ivory')],1,1.02)
for o in S[-1]['objects']:
 if o['id']=='break_link':o['fade_out']=[42,66]
scene('06_reasons',1050,1290,'WHY DID IT LAST?','SCALE AND MARKET DEPTH',
 'A large U.S. economy and deep Treasury markets help support the dollar. It is also widely used for trade invoicing.',
 [['A large U.S. economy','and deep Treasury markets'],['help support the dollar. It is also','widely used for trade invoicing.']],
 [rect('economy_card',145,740,790,140,delay=6),rect('treasury_card',145,930,790,140,stroke='gold',delay=18),rect('trade_card',145,1120,790,140,delay=30),
  text('economy','LARGE U.S. ECONOMY',540,810,44,delay=6),text('treasury','DEEP TREASURY MARKETS',540,1000,44,'gold',delay=18),
  text('invoicing','TRADE INVOICING',540,1190,44,delay=30)],1,1)
H=(540,830,85); L=(250,1020,55); R=(830,1020,55); B=(540,1190,55)
scene('07_network',1290,1530,'THE NETWORK EFFECT','USE CAN REINFORCE USE',
 'When banks and businesses already use dollars, others can find it easier to use them too. That reinforces the network.',
 [['When banks and businesses','already use dollars, others can'],['find it easier to use them too.','That reinforces the network.']],
 [joined('left_link',H,L,22),joined('right_link',H,R,38),joined('bottom_link',H,B,54),
  circle('hub',H[0],H[1],H[2],'gold','gold',6),text('hub_dollar','$',540,830,104,'night',delay=6),
  circle('left_node',L[0],L[1],L[2],delay=22),circle('right_node',R[0],R[1],R[2],delay=38),circle('bottom_node',B[0],B[1],B[2],delay=54),
  text('banks','BANKS',250,1135,40,'slate',delay=22),text('businesses','BUSINESSES',830,1135,40,'slate',delay=38),text('investors','INVESTORS',540,1300,40,'slate',delay=54)],1,1.02)
H=(540,900,120); E=(250,960,62); Y=(830,960,62); O=(540,1170,46)
scene('08_payoff',1530,1800,'LEADING. NOT ONLY.','AN EVOLVING SYSTEM',
 "The dollar is not the only international currency, and its lead isn't guaranteed. Its advantage rests on history, markets, and widespread use.",
 [['The dollar is not the only','international currency,'],["and its lead isn't guaranteed.",'Its advantage rests on history, markets, and widespread use.']],
 [joined('euro_link',H,E),joined('yen_link',H,Y),joined('other_link',H,O),circle('euro_node',E[0],E[1],E[2]),circle('yen_node',Y[0],Y[1],Y[2]),circle('other_node',O[0],O[1],O[2]),
  text('euro','€',250,960,64,'slate'),text('yen','¥',830,960,64,'slate'),circle('hub',540,900,120,'surface','gold'),text('dollar','$',540,900,145,'gold'),
  text('conclusion','HISTORY + MARKETS + USE',540,1335,42,'ivory')],1,1.02)
# Scene 08 needs three short caption pages to remain readable and preserve the exact VO.
S[-1]['captions']=[
 {'interval':[1530,1605],'lines':['The dollar is not the only','international currency,']},
 {'interval':[1605,1675],'lines':["and its lead isn't guaranteed."]},
 {'interval':[1675,1800],'lines':['Its advantage rests on history,','markets, and widespread use.']},
]
plan={
 'project':'Why the dollar is a leading world currency',
 'brief':{'confirmed':['60-second script','no source images or video; code-drawn visuals only'],'assumptions':['English','general audience','9:16, 1080 x 1920','30 fps','vertical social viewing'],'unverified':['target platform and UI-safe areas','audio delivery and voice','final captions and their timing']},
 'format':{'width':1080,'height':1920,'fps':30,'frame_count':1800,'interval_convention':'zero-based, start inclusive and end exclusive'},
 'palette':{'night':'#101B2B','surface':'#1C2D40','ivory':'#F7F4EC','slate':'#C3CED7','gold':'#EAC777'},
 'font':{'face':'DejaVu Sans Bold','path_for_reference_test':'/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf','fallback':'approval and retesting required'},
 'restrictions':['No still-image, video, SVG, generated-image, photo, stock or texture input.','Only code-drawn solid rectangles, circles, lines and text; font files allowed.','No numerical or area-proportional claim; symbols are illustrative and not exhaustive.'],
 'render_rules':{
  'coordinates':'top-left origin, x right and y down; rectangles use top-left; circles and text use center',
  'scene':'Select exactly one scene with start <= frame < end. Hard cuts; background fills full frame.',
  'ease':'u=clamp(t,0,1); smooth(t)=u*u*(3-2*u)',
  'object_opacity':'local=frame-scene_start; default delay=0 for screen objects, 6 for world objects; opacity=smooth((local-delay)/18). If fade_out [a,b] is present multiply opacity by 1-smooth((local-a)/(b-a)). No entry-position shift.',
  'motion':'If x_motion exists, replace the base x of the circle center or text center with from+(to-from)*smooth((local-local_start)/(local_end-local_start)). Other coordinates remain unchanged.',
  'camera':'For local in [0,duration-1], zoom=z0+(z1-z0)*smooth(local/(duration-1)). Transform world points around the explicit zoom_anchor: (ax+(x-ax)*zoom, ay+(y-ay)*zoom); scale world sizes, line widths and world font sizes by zoom. Screen heading/subheading and captions are not camera-transformed. All camera angles remain zero.',
  'compositing':'background, world objects in listed order, screen objects in listed order, captions. Source-over compositing. Source colors and stroke widths are in the objects; round scaled font size and stroke width to nearest pixel.',
  'captions':'Draft caption timing only: at each frame choose the scene cue whose interval contains it. Draw panel x=70,y=1510,w=940,h=180,r=24, surface fill. DejaVu Sans Bold 42 px ivory centered x=540. One line center y=1600; two lines centers y=1568 and 1635. Placement safe areas NOT VERIFIED. Actual cue timing must be aligned to a recorded voice.',
 },
 'scenes':S}
Path(__file__).with_name('visual-plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n')
print('Generated',len(S),'fresh scenes')
