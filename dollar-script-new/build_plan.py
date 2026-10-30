#!/usr/bin/env python3
"""Build the new 60-second storyboard manifest; no image/video input assets."""
import json,math
from pathlib import Path
from PIL import ImageFont
ROOT=Path(__file__).resolve().parent
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
CAP=ImageFont.truetype(FONT,42)

def text(id,value,x,y,size=44,color='ivory',group='world',delay=6,bg='night',container=None):
 o={'id':id,'kind':'text','text':value,'x':x,'y':y,'size':size,'color':color,'group':group,'delay':delay,'background':bg}
 if container:o['container']=container
 return o

def circle(id,x,y,r,fill='panel',stroke='line',delay=6):return {'id':id,'kind':'circle','x':x,'y':y,'radius':r,'fill':fill,'stroke':stroke,'stroke_width':3,'group':'world','delay':delay}
def rect(id,x,y,w,h,fill='panel',stroke='line',delay=6):return {'id':id,'kind':'rect','x':x,'y':y,'w':w,'h':h,'radius':22,'fill':fill,'stroke':stroke,'stroke_width':3,'group':'world','delay':delay}
def line(id,x1,y1,x2,y2,delay=6):return {'id':id,'kind':'line','x1':x1,'y1':y1,'x2':x2,'y2':y2,'color':'line','stroke_width':4,'group':'world','delay':delay}
def connect(id,a,b,delay=6):
 dx,dy=b[0]-a[0],b[1]-a[1];length=math.hypot(dx,dy);u,v=dx/length,dy/length
 return line(id,round(a[0]+u*(a[2]-2),2),round(a[1]+v*(a[2]-2),2),round(b[0]-u*(b[2]-2),2),round(b[1]-v*(b[2]-2),2),delay)
def headings(title,sub):return [text('heading',title,540,320,66,group='screen',delay=0),text('subheading',sub,540,430,40,'muted','screen',0)]
def paginate(vo):
 words=vo.split();lines=[];line_words=[]
 for word in words:
  candidate=' '.join(line_words+[word])
  if line_words and CAP.getlength(candidate)>825:
   lines.append(' '.join(line_words));line_words=[word]
  else:line_words.append(word)
 if line_words:lines.append(' '.join(line_words))
 return [lines[i:i+2] for i in range(0,len(lines),2)]
def make_cues(vo,start,end):
 pages=paginate(vo);assert ' '.join(line for page in pages for line in page)==vo
 weights=[len(' '.join(p).split()) for p in pages];total=sum(weights);last=start;used=0;cues=[]
 for i,(page,weight) in enumerate(zip(pages,weights)):
  used+=weight;boundary=end if i==len(pages)-1 else start+round((end-start)*used/total)
  assert boundary>last;cues.append({'start':last,'end':boundary,'lines':page});last=boundary
 return cues
S=[]
def add(id,start,end,title,sub,vo,purpose,objects,z0=1,z1=1):
 S.append({'id':id,'start':start,'end':end,'camera':{'projection':'orthographic','yaw':0,'pitch':0,'roll':0,'screen_center':[540,960],'zoom_anchor':[540,960],'zoom_start':z0,'zoom_end':z1},'voiceover':vo,'purpose':purpose,'objects':headings(title,sub)+objects,'captions':make_cues(vo,start,end),'caption_status':'PROVISIONAL: approximate visual-time pages, not aligned to recorded audio'})
# Scene 1: token edges touch both country edges at the start and end of motion.
A=(245,900,70);B=(835,900,70)
add('01_question',0,180,'WHY USE DOLLARS?','TWO COUNTRIES. ONE CURRENCY.',
 'Why might two countries trade in dollars when neither one issues them?',
 'Show the opening puzzle: two symbolic countries trade using a dollar.',[
 connect('route',A,B),circle('country_a',*A),circle('country_b',*B),circle('token',540,900,50,'gold','gold'),
 text('dollar','$',540,900,66,'night',bg='gold',container='token'),text('country_a_label','COUNTRY A',245,1090,40,'muted'),text('country_b_label','COUNTRY B',835,1090,40,'muted')],1,1.01)
for o in S[-1]['objects']:
 if o['id'] in ('token','dollar'):o['move_x']={'from':365,'to':715,'local_start':18,'local_end':120}
add('02_definition',180,405,'LEADING. NOT ONLY.','CURRENCIES COEXIST',
 "The dollar is the leading international currency, not the only one. It's widely used for trade invoicing, finance, and reserves.",
 'Give the spoken and visible qualification; the euro and yen are illustrative examples, not an exhaustive list or scaled data.',[
 circle('euro_node',260,810,62),circle('dollar_node',540,810,78,'panel','gold'),circle('yen_node',820,810,62),
 text('euro','€',260,810,72,'ivory',bg='panel',container='euro_node'),text('dollar','$',540,810,90,'gold',bg='panel',container='dollar_node'),text('yen','¥',820,810,72,'ivory',bg='panel',container='yen_node'),
 rect('trade_card',105,1030,270,145,delay=12),rect('finance_card',405,1030,270,145,delay=22),rect('reserve_card',705,1030,270,145,delay=32),
 text('trade','INVOICING',240,1102,39,delay=12,bg='panel',container='trade_card'),text('finance','FINANCE',540,1102,39,delay=22,bg='panel',container='finance_card'),text('reserves','RESERVES',840,1102,38,delay=32,bg='panel',container='reserve_card')],1,1)
add('03_history',405,600,'THE POSTWAR PLAN','BRETTON WOODS',
 'In 1944, Bretton Woods placed the dollar at the center of a new postwar monetary system.',
 'Place the 1944 conference within a postwar framework; the dollar also had an earlier international role.',[
 rect('history_card',150,760,780,310,stroke='gold'),text('year','1944',540,885,150,'gold',bg='panel',container='history_card'),
 text('history_note','POSTWAR FRAMEWORK',540,1010,42,'muted',bg='panel',container='history_card')],1,1.01)
add('04_gold',600,840,'THE GOLD LINK','FOREIGN CENTRAL BANKS',
 'Participating countries tied their currencies to the dollar. The United States offered gold for dollars held by foreign central banks.',
 'Show currency links while preserving the essential foreign-central-bank qualifier.',[
 line('left_link',355,920,415,920),line('right_link',665,920,725,920),
 rect('other_box',100,830,255,180),rect('dollar_box',415,830,250,180,stroke='gold'),rect('gold_box',725,830,255,180,stroke='gold'),
 text('other_first','OTHER',227,895,40,bg='panel',container='other_box'),text('other_second','MONEY',227,950,40,bg='panel',container='other_box'),
 text('usd','$',540,920,85,'gold',bg='panel',container='dollar_box'),text('gold','GOLD',852,920,43,'gold',bg='panel',container='gold_box'),
 text('qualifier','FOREIGN CENTRAL BANKS',540,1190,42,'muted')],1,1)
add('05_suspension',840,1050,'CONVERSION','SUSPENDED IN 1971',
 "In 1971, the United States suspended gold conversion. The dollar's international role continued after the system changed.",
 'Fade the gold-conversion link without claiming the entire Bretton Woods system ended in one day.',[
 line('left_link',390,910,490,910),line('middle_link',490,910,590,910),line('right_link',590,910,690,910),
 rect('dollar_box',140,820,250,180,stroke='gold'),rect('gold_box',690,820,250,180,stroke='gold'),
 text('dollar','$',265,910,85,'gold',bg='panel',container='dollar_box'),text('gold','GOLD',815,910,43,'gold',bg='panel',container='gold_box'),
 text('status','OFFICIAL CONVERSION SUSPENDED',540,1185,40,'muted')],1,1.01)
for o in S[-1]['objects']:
 if o['id']=='middle_link':o['fade_out']=[40,64]
add('06_economy',1050,1290,'WHY IT CONTINUED','SCALE + LIQUID MARKETS',
 'A large U.S. economy and deep Treasury markets support the dollar, while widespread trade invoicing gives people reasons to use it.',
 'State the supporting factors without numerical or causal overclaim.',[
 rect('economy_card',140,735,800,140,delay=6),rect('market_card',140,920,800,140,stroke='gold',delay=20),rect('trade_card',140,1105,800,140,delay=34),
 text('economy','LARGE U.S. ECONOMY',540,805,43,delay=6,bg='panel',container='economy_card'),text('market','DEEP TREASURY MARKETS',540,990,43,'gold',delay=20,bg='panel',container='market_card'),text('trade','TRADE INVOICING',540,1175,43,delay=34,bg='panel',container='trade_card')],1,1)
H=(540,775,80);L=(250,970,54);R=(830,970,54);N=(540,1180,54)
add('07_network',1290,1530,'USE REINFORCES USE','AN ILLUSTRATIVE MODEL',
 "As more people use dollars, others may find them easier to use. That network effect can reinforce the dollar's role.",
 'First show two connected participants; then reveal a new user and two new links. The animation illustrates a mechanism, not data or causal proof.',[
 connect('hub_left',H,L,16),connect('hub_right',H,R,16),connect('existing_peers',L,R,26),
 connect('new_to_left',N,L,96),connect('new_to_right',N,R,96),connect('new_to_hub',H,N,96),
 circle('hub',*H,fill='gold',stroke='gold'),text('hub_dollar','$',540,775,92,'night',bg='gold',container='hub'),
 circle('left_node',*L,delay=16),circle('right_node',*R,delay=16),circle('new_node',*N,delay=96),
 text('bank_label','BANKS',250,1080,40,'muted',delay=16),text('business_label','BUSINESSES',830,1080,40,'muted',delay=16),text('new_label','NEW USER',540,1290,40,'muted',delay=96),
 text('model_note','USE CAN GET EASIER',540,1380,44,'ivory',delay=110)],1,1.01)
add('08_answer',1530,1800,'WHY THEY CHOOSE $','COMMON ACCESS, NOT A RULE',
 'So those two countries can choose dollars because they already have access to a widely used system. Other currencies can work too.',
 'Return to the same two parties and directly answer the opening; retain non-exclusivity.',[
 connect('route',A,B),circle('country_a',*A),circle('country_b',*B),circle('token',715,900,50,'gold','gold'),text('dollar','$',715,900,66,'night',bg='gold',container='token'),
 text('country_a_label','COUNTRY A',245,1090,40,'muted'),text('country_b_label','COUNTRY B',835,1090,40,'muted'),
 text('answer','BOTH CAN USE ONE SYSTEM',540,1240,43,'ivory'),text('other','OTHER CURRENCIES CAN WORK TOO',540,1330,40,'muted')],1,1)
plan={'title':'Why is the dollar a world currency?','format':{'width':1080,'height':1920,'fps':30,'frames':1800,'status':'PROPOSED; duration is confirmed, platform and format are not','frame_range':'0-based [start,end)'},
'colors':{'night':'#101B2B','panel':'#1C2D40','ivory':'#F7F4EC','muted':'#C3CED7','gold':'#EAC777','line':'#96AABB'},
'font':{'name':'DejaVu Sans Bold','tested_path':FONT,'substitution':'requires re-testing'},
'restrictions':['No photos, footage, images, screenshots, textures, external SVGs, or video inputs.','Draw only solid rectangles, circles, lines and text; licensed font files allowed.','All currency symbols, countries and network nodes are illustrative, not exhaustive or data-scaled.'],
'contract':{'coordinates':'top-left origin; text and circles use centers, rectangles top-left','scene_selection':'0-based start inclusive, end exclusive; hard cuts','entry':'local=frame-scene.start; alpha=smooth((local-delay)/18), smooth(x)=u*u*(3-2*u), u=clamp(x,0,1). No entry translation. If fade_out=[a,b], multiply alpha by 1-smooth((local-a)/(b-a)).','camera':'All cameras orthographic with yaw/pitch/roll 0. Screen center and zoom anchor (540,960). World points (x,y) map to (540+(x-540)*z,960+(y-960)*z); z=z0+(z1-z0)*smooth(local/(scene_duration-1)). Scale world shapes, text and strokes by z. Heading, subheading and captions are screen-fixed.','motion':'When move_x is present, x=from+(to-from)*smooth((local-local_start)/(local_end-local_start)) before camera transform. Otherwise the object geometry holds. Token circles and glyphs use the same move_x.','z_order':'Background, then world objects in listed order, then screen objects in listed order, then captions. Source-over alpha. Network lines are drawn behind nodes.','captions':'Draft cue ranges are provisional, not synced to speech. Fixed panel (70,1510) size 940×180 radius 22; fill panel. Bold 42 px ivory: one line at (540,1600); two lines at (540,1568) and (540,1635). PLATFORM SAFE AREA NOT VERIFIED. Re-align to final voice, review and add meaningful non-speech captions if needed.','reproducibility':'Font metrics depend on installed font version; replacement requires review. Round scaled font size and stroke width to nearest pixel.'},'scenes':S}
(ROOT/'visual-plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Plan:',len(S),'scenes,',plan['format']['frames'],'frames')
