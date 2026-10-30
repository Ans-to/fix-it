#!/usr/bin/env python3
"""Check explicit supplied measurements; does not collect render evidence itself."""
import argparse
import json
import math
import re
import sys


def box(b):
    if len(b)!=4 or any(not isinstance(x,(int,float)) or not math.isfinite(x) for x in b) or b[0]>b[2] or b[1]>b[3]: raise ValueError('invalid box')
    return b

def contains(outer,inner,margin=0):
    a=box(outer); b=box(inner)
    if not math.isfinite(margin) or margin<0: raise ValueError('invalid margin')
    return a[0]+margin<=b[0] and a[1]+margin<=b[1] and b[2]<=a[2]-margin and b[3]<=a[3]-margin

def color_luminance(color):
    if not re.fullmatch('#[a-fA-F0-9]{6}',color): raise ValueError('color must be #RRGGBB')
    c=[int(color[i:i+2],16)/255 for i in (1,3,5)]
    c=[v/12.92 if v<=0.04045 else ((v+0.055)/1.055)**2.4 for v in c]
    return .2126*c[0]+.7152*c[1]+.0722*c[2]

def contrast(a,b):
    x,y=sorted((color_luminance(a),color_luminance(b)))
    return (y+.05)/(x+.05)

def run(check):
    kind=check['type']; detail={}
    if kind=='bounds' or kind=='rect_containment' or kind=='caption_fit':
        passed=contains(check['outer'],check['inner'],check.get('margin',0))
    elif kind=='text_overlap':
        a=box(check['a']);b=box(check['b'])
        passed=not(a[0]<b[2] and b[0]<a[2] and a[1]<b[3] and b[1]<a[3])
    elif kind=='circle_containment':
        b=box(check['inner']);cx,cy=check['center'];radius=check['radius']-check.get('margin',0)
        if radius<0: raise ValueError('negative usable radius')
        passed=all(math.hypot(x-cx,y-cy)<=radius for x in (b[0],b[2]) for y in (b[1],b[3]))
    elif kind=='connector_endpoint':
        # Caller supplies actual transformed visible node outline radius and endpoint.
        x,y=check['endpoint'];cx,cy=check['center'];r=check['radius'];tol=check['tolerance']
        if r<=0 or tol<0: raise ValueError('invalid circle/tolerance')
        gap=math.hypot(x-cx,y-cy)-r;detail['signed_gap']=gap
        passed=abs(gap)<=tol
    elif kind=='contrast':
        ratio=contrast(check['foreground'],check['background']);target=check['target']
        if target not in (3,4.5): raise ValueError('target must be 3 or 4.5')
        detail.update(ratio=ratio,target=target);passed=ratio>=target
    else: raise ValueError('unsupported check type '+str(kind))
    return {'id':check['id'],'frame':check['frame'],'type':kind,'status':'PASS' if passed else 'FAIL','detail':detail}


def report(payload):
    # Evidence is a reported provenance string, not independently verified by this utility.
    def finite(v):
        if isinstance(v,float): return math.isfinite(v)
        if isinstance(v,list): return all(finite(x) for x in v)
        if isinstance(v,dict): return all(finite(x) for x in v.values())
        return True
    if not finite(payload): raise ValueError('non-finite measurement')
    if not isinstance(payload.get('evidence'),str) or not payload['evidence'].strip() or not payload.get('checks'): raise ValueError('evidence and at least one check required')
    if any(not isinstance(c.get('frame'),int) or isinstance(c.get('frame'),bool) or c['frame']<0 for c in payload['checks']): raise ValueError('frame must be a nonnegative integer')
    checks=[run(c) for c in payload['checks']]
    return {'measurement_evidence':payload['evidence'],'scope':'supplied measurements only; source/render coverage not independently verified',
            'results':checks,'broader_render_review':'FAIL' if any(c['status']=='FAIL' for c in checks) else 'PARTIAL'}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('measurements');a=p.parse_args()
    try:
        with open(a.measurements,encoding='utf-8') as f: payload=json.load(f,parse_constant=lambda v: (_ for _ in ()).throw(ValueError('non-finite number')))
        r=report(payload)
        print(json.dumps(r,indent=2));return 1 if r['broader_render_review']=='FAIL' else 0
    except (KeyError,TypeError,ValueError,OSError) as e:
        print(json.dumps({'status':'FAIL','error':str(e)}));return 1

if __name__=='__main__':sys.exit(main())
