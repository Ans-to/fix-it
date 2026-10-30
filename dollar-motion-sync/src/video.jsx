import React,{useEffect,useMemo,useState} from 'react';
import {AbsoluteFill,Audio,delayRender,continueRender,staticFile,useCurrentFrame,interpolate,spring,useVideoConfig} from 'remotion';
import {ThreeCanvas} from '@remotion/three';import {useThree} from '@react-three/fiber';import * as THREE from 'three';
import plan from './timeline.json';import alignment from './word-cues.json';
const opt={extrapolateLeft:'clamp',extrapolateRight:'clamp'};
const l=(f,a,b)=>interpolate(f,a,b,opt);const smooth=x=>{x=Math.max(0,Math.min(1,x));return x*x*(3-2*x)};
const alpha=(f,s,e)=>l(f,[s,s+8,e-8,e],[0,1,1,0]);
function tex(text,color='#05202A',size=230){const canvas=document.createElement('canvas');canvas.width=512;canvas.height=512;const c=canvas.getContext('2d');c.clearRect(0,0,512,512);c.fillStyle=color;c.font=`800 ${size}px Manrope,sans-serif`;c.textAlign='center';c.textBaseline='middle';c.fillText(text,256,258);const t=new THREE.CanvasTexture(canvas);t.colorSpace=THREE.SRGBColorSpace;return t;}
function Medallion({mark='$',position=[0,0,0],scale=1,rotation=[0,0,0],color='#D7BC76'}){
 const t=useMemo(()=>tex(mark),[mark]);useEffect(()=>()=>t.dispose(),[t]);
 return <group position={position} scale={scale} rotation={rotation}>
  <mesh rotation={[Math.PI/2,0,0]}><cylinderGeometry args={[.78,.78,.20,64]}/><meshStandardMaterial color={color} metalness={.72} roughness={.27}/></mesh>
  <mesh position={[0,0,.105]}><circleGeometry args={[.72,64]}/><meshStandardMaterial color={color} metalness={.62} roughness={.3}/></mesh>
  <mesh position={[0,0,.112]}><planeGeometry args={[1.18,1.18]}/><meshBasicMaterial map={t} transparent/></mesh>
  <mesh position={[0,0,-.105]} rotation={[0,Math.PI,0]}><circleGeometry args={[.72,64]}/><meshStandardMaterial color={color} metalness={.62} roughness={.3}/></mesh>
  <mesh position={[0,0,-.112]} rotation={[0,Math.PI,0]}><planeGeometry args={[1.18,1.18]}/><meshBasicMaterial map={t} transparent/></mesh>
  <mesh position={[0,0,.115]}><ringGeometry args={[.665,.673,64]}/><meshBasicMaterial color="#F7E8B6"/></mesh>
 </group>
}
function Link({a,b,grow=1,color='#7EE6DB'}){const aa=new THREE.Vector3(...a),bb=new THREE.Vector3(...b);const v=bb.clone().sub(aa).multiplyScalar(grow),mid=aa.clone().add(v.clone().multiplyScalar(.5));const q=new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0,1,0),v.clone().normalize());return <mesh position={mid} quaternion={q}><cylinderGeometry args={[.014,.014,Math.max(.001,v.length()),8]}/><meshBasicMaterial color={color}/></mesh>}
function Node({p,name,scale=1}){const t=useMemo(()=>tex(name,'#071F29',250),[name]);useEffect(()=>()=>t.dispose(),[t]);return <group position={p} scale={scale}><mesh><sphereGeometry args={[.18,20,20]}/><meshStandardMaterial color={name==='D'?'#F7C675':'#A6FFF1'} emissive={name==='D'?'#DB6B2A':'#188B86'} emissiveIntensity={.5}/></mesh><mesh position={[0,0,.178]}><planeGeometry args={[.26,.26]}/><meshBasicMaterial map={t} transparent/></mesh></group>}
function Camera({f}){const {camera}=useThree();camera.position.set(.26*Math.sin(f*.022),.20*Math.cos(f*.019),9.4-.5*Math.sin(f*.014));camera.lookAt(0,-.15,0);camera.updateProjectionMatrix();return null}
function Stage({f}){
 const hook=f<114;const market=f>=96&&f<220;const network=f>=200&&f<340;const finale=f>=320;
 const marketGrow=smooth((f-96)/18);const networkGrow=smooth((f-200)/20);const endGrow=smooth((f-320)/20);
 const pts=[[-1.36,.78,.15],[1.36,.75,.15],[-1.35,-.9,.15],[1.34,-.92,.15]],middle=[0,-.1,.1];
 const enter=pts.map((_,i)=>smooth((f-(217+i*13))/12));
 const transit=Math.max(0,Math.min(1,(f-263)/30));const dot=transit<.5?pts[3].map((v,i)=>v+(middle[i]-v)*transit*2):middle.map((v,i)=>v+(pts[0][i]-v)*(transit-.5)*2);
 const marketOpacity=alpha(f,96,220), networkOpacity=alpha(f,200,340);
 return <>
  <Camera f={f}/><ambientLight intensity={1.1}/><directionalLight position={[3,4,7]} intensity={3.4} color="#DBFAFF"/><pointLight position={[-3,1,3]} intensity={24} color="#1EEED4"/><pointLight position={[3,-2,4]} intensity={21} color="#E5A950"/>
  {hook&&<group position={[.12,-.15,-.1]} scale={1-.75*marketGrow} rotation={[.2+f*.005,.45+f*.014,-.12]}>
   <mesh><sphereGeometry args={[1.28,18,12]}/><meshBasicMaterial color="#4BF5E1" wireframe transparent opacity={.25}/></mesh>
   {[0,1,2].map(i=><mesh key={i} rotation={[i*.7,.3+i*.4,f*.009+i]}><torusGeometry args={[1.48+i*.12,.012,8,80]}/><meshBasicMaterial color={i===1?'#F2CE7B':'#47DDD4'} transparent opacity={.56}/></mesh>)}
   <Medallion scale={.85} rotation={[-.2,-.45-f*.014,.12]}/>
  </group>}
  {market&&<group position={[.18,-.28,-.55]} rotation={[.08,-.3+.08*Math.sin(f*.02),.08]} scale={marketGrow}>
   {[0,1,2,3,4,5,6].map(i=>{const v=.55+i*.12+.17*Math.sin(f*.09+i*1.5);return <mesh key={i} position={[-1.42+i*.47,-.7+v*.5,-i*.05]}><boxGeometry args={[.30,v,.33]}/><meshStandardMaterial color={i%2?'#249F9F':'#C5A45C'} metalness={.55} roughness={.27} transparent opacity={marketOpacity}/></mesh>})}
   <group position={[.1,.25,.4]} rotation={[.22,f*.03,.1]}><Medallion scale={.68}/></group>
   {[0,1,2].map(i=><mesh key={'rail'+i} position={[0,-1.18+i*.32,-.3]} rotation={[Math.PI/2,0,0]}><torusGeometry args={[1.65,.012,8,64]}/><meshBasicMaterial color="#7CE1DD" transparent opacity={marketOpacity*.44}/></mesh>)}
  </group>}
  {network&&<group position={[0,-.20,0]} scale={networkGrow*(1-smooth((f-318)/11))}>
   <Medallion scale={.55} rotation={[.12,.3+.1*Math.sin(f*.04),0]}/>
   {pts.map((p,i)=>enter[i]>.001?<React.Fragment key={i}><Link a={middle} b={p} grow={enter[i]}/><Node p={p} name={['A','B','C','D'][i]} scale={enter[i]}/></React.Fragment>:null)}
   {f>=263&&f<295&&<mesh position={dot}><sphereGeometry args={[.07,16,16]}/><meshBasicMaterial color="#FFF5BF"/></mesh>}
   <mesh position={[0,-.1,-.7]} rotation={[.48,0,f*.013]}><torusGeometry args={[1.64,.012,8,80]}/><meshBasicMaterial color="#5DCCCA" transparent opacity={networkOpacity*.5}/></mesh>
  </group>}
  {finale&&<group position={[0,.95,0]} scale={endGrow}>
    <Medallion position={[-.8,.25,0]} scale={1.05} rotation={[.14,.4+f*.006,.08]}/>
    <Medallion mark="€" position={[.96,1.00,-.45]} scale={.55} rotation={[.1,-.3+.22*Math.sin(f*.025),-.1]} color="#BDD9DF"/>
    <Medallion mark="¥" position={[1.12,.00,-.5]} scale={.43} rotation={[.18,.3+.22*Math.sin(f*.028),.12]} color="#BDD9DF"/>
  </group>}
  <group>{Array.from({length:42},(_,i)=>{const x=Math.sin(i*81.1)*2.2,y=Math.cos(i*22.4)*4.2,z=-2.4+Math.sin(i*10.3);return <mesh key={i} position={[x+.06*Math.sin(f*.02+i),y+.1*Math.cos(f*.018+i),z]}><sphereGeometry args={[i%6?.018:.035,6,6]}/><meshBasicMaterial color={i%3?'#88DEDE':'#F9D596'} transparent opacity={.4}/></mesh>})}</group>
 </>
}
function TypeMoment({item,f}){
 const {fps}=useVideoConfig();if(f<item.start||f>=item.end)return null;
 const p=spring({frame:f-item.start,fps,config:{damping:18,stiffness:190,mass:.65}});const exit=l(f,[item.end-5,item.end],[1,0]);
 const direction=item.style==='right'?1:-1;const burst=item.style==='burst';const top=burst?330:item.id==='connections'?250:item.id==='leads'?1000:item.style==='right'?1000:250;
 const shortest=item.end-item.start<20;const size=burst?(item.lines[0].length>7?192:245):item.lines.some(x=>x.length>11)?112:170;
 return <div style={{position:'absolute',left:76,right:76,top,opacity:exit,transform:`translate3d(0px,${(1-p)*40}px,0) scale(${burst?1.16-.16*p:.94+.06*p})`,transformOrigin:item.style==='right'?'right center':'left center',textAlign:item.style==='right'?'right':'left',pointerEvents:'none'}}>
  {item.lines.map((line,i)=><div key={line} style={{fontFamily:'Anton',fontSize:size,lineHeight:.96,whiteSpace:'nowrap',color:i?'#F1C56D':'#F1FFF7',letterSpacing:-1,textShadow:'0 7px 30px rgba(2,9,20,.8)'}}>{line}</div>)}
 </div>
}
function Captions({f}){
 let index=plan.scenes.findIndex(s=>f>=s.voice_start&&f<s.voice_start+Math.ceil(s.voice_duration*30));if(index<0)return null;
 const scene=plan.scenes[index],words=alignment.clips[index].words;let n=0;
 return <div style={{position:'absolute',top:1510,left:60,right:60,minHeight:155,padding:'16px 12px',boxSizing:'border-box',borderRadius:12,background:'rgba(3,11,19,.89)',border:'1px solid rgba(121,222,213,.35)',display:'flex',flexDirection:'column',alignItems:'center',justifyContent:'center'}}>
  {scene.caption_lines.map((line,j)=><div key={j} style={{font:'700 35px Manrope',lineHeight:1.5,whiteSpace:'nowrap'}}>{line.map((w,k)=>{const item=words[n++],active=f>=item.start_frame&&f<item.end_frame;return <span key={k} style={{color:active?'#FFE493':'#EFFCF7',background:active?'rgba(218,166,75,.15)':'transparent',borderRadius:3}}>{w}{k<line.length-1?' ':''}</span>})}</div>)}
 </div>
}
function Graphics({f}){
 return <>
  <div style={{position:'absolute',top:104,left:76,right:76,display:'flex',justifyContent:'space-between',font:'21px Mono',letterSpacing:3,color:'#BDE6DC'}}><span>THE MONEY NETWORK</span><span>01 / 15</span></div>
  <div style={{position:'absolute',top:150,left:76,right:76,height:2,background:'rgba(180,232,222,.18)'}}><div style={{width:`${f/449*100}%`,height:2,background:'#F0C977'}}/></div>
  {plan.titles.map(t=><TypeMoment key={t.id} item={t} f={f}/>)}
  {f>=233&&f<318&&<div style={{position:'absolute',top:1370,left:0,right:0,textAlign:'center',font:'22px Mono',color:'#C0EBE2',letterSpacing:2}}>ILLUSTRATIVE NETWORK</div>}
  {f>=365&&<div style={{position:'absolute',top:1390,left:76,right:76,textAlign:'right',font:'22px Mono',color:'#C0EBE2',letterSpacing:2}}>OTHER CURRENCIES EXIST</div>}
  <Captions f={f}/>
 </>
}
export function Film(){const f=useCurrentFrame();const [h]=useState(()=>delayRender('Load local fonts'));useEffect(()=>{Promise.all([document.fonts.load('800 100px Manrope'),document.fonts.load('100px Anton'),document.fonts.load('20px Mono')]).then(()=>continueRender(h)).catch(()=>continueRender(h))},[h]);
 const pulse=plan.sound_cues.map(c=>Math.exp(-Math.max(0,f-c.frame)*.48)*(f>=c.frame?1:0)).reduce((a,b)=>Math.max(a,b),0);
 return <AbsoluteFill style={{background:'#041219',overflow:'hidden'}}>
  <style>{`@font-face{font-family:Anton;src:url('${staticFile('fonts/Anton-Regular.ttf')}')} @font-face{font-family:Manrope;src:url('${staticFile('fonts/Manrope-Variable.ttf')}');font-weight:200 800} @font-face{font-family:Mono;src:url('${staticFile('fonts/IBMPlexMono-Regular.ttf')}')}`}</style>
  <AbsoluteFill style={{background:'radial-gradient(ellipse at 60% 48%,#124D4F 0%,#0A2933 42%,#030C14 90%)'}}/>
  <AbsoluteFill style={{opacity:.18,backgroundImage:'linear-gradient(#4FBCB5 1px,transparent 1px),linear-gradient(90deg,#4FBCB5 1px,transparent 1px)',backgroundSize:'100px 100px',transform:`perspective(700px) rotateX(57deg) scale(2) translateY(${f*.8}px)`,transformOrigin:'50% 65%'}}/>
  <ThreeCanvas width={1080} height={1920} camera={{position:[0,0,9.4],fov:40,near:.1,far:80}} gl={{antialias:true,alpha:true}}><Stage f={f}/></ThreeCanvas>
  <AbsoluteFill style={{pointerEvents:'none',background:'linear-gradient(180deg,rgba(2,9,14,.3),transparent 35%,transparent 65%,rgba(2,9,14,.55))'}}/>
  <AbsoluteFill style={{pointerEvents:'none',background:'#DAFFF2',opacity:Math.min(.12,pulse*.09)}}/>
  <Graphics f={f}/><Audio src={staticFile('audio/mix.wav')}/>
 </AbsoluteFill>
}
