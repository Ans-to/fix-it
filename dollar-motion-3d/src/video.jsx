import React, {useMemo,useEffect,useState} from 'react';
import {AbsoluteFill,Audio,delayRender,continueRender,staticFile,useCurrentFrame,interpolate,spring,useVideoConfig} from 'remotion';
import {ThreeCanvas} from '@remotion/three';
import {useThree} from '@react-three/fiber';
import * as THREE from 'three';
import plan from './plan.json';

const clamp={extrapolateLeft:'clamp',extrapolateRight:'clamp'};
const lerp=(f,ins,outs)=>interpolate(f,ins,outs,clamp);
const sceneAlpha=(f,s,e)=>lerp(f,[s,s+9,e-9,e],[0,1,1,0]);
const ease=(v)=>{v=Math.max(0,Math.min(1,v));return v*v*(3-2*v)};

function markTexture(mark,fg='#100E17'){
  const el=document.createElement('canvas');el.width=512;el.height=512;const c=el.getContext('2d');
  c.clearRect(0,0,512,512);c.textAlign='center';c.textBaseline='middle';c.font='bold 290px Manrope, sans-serif';c.fillStyle=fg;c.fillText(mark,256,259);
  const tex=new THREE.CanvasTexture(el);tex.colorSpace=THREE.SRGBColorSpace;return tex;
}
function Coin({mark='$',tone='#D6A454',radius=1,rotation=[0,0,0],position=[0,0,0],opacity=1}){
  const texture=useMemo(()=>markTexture(mark, tone==='#D6A454'?'#25170D':'#10182A'),[mark,tone]);
  useEffect(()=>()=>texture.dispose(),[texture]);
  return <group rotation={rotation} position={position} scale={radius}>
    <mesh rotation={[Math.PI/2,0,0]}><cylinderGeometry args={[1,1,.18,72]}/><meshStandardMaterial color={tone} metalness={.78} roughness={.27} transparent opacity={opacity}/></mesh>
    <mesh position={[0,0,.095]}><circleGeometry args={[.915,72]}/><meshStandardMaterial color={tone} metalness={.72} roughness={.3} transparent opacity={opacity}/></mesh>
    <mesh position={[0,0,.101]}><circleGeometry args={[.73,72]}/><meshBasicMaterial map={texture} transparent opacity={opacity}/></mesh>
    <mesh position={[0,0,.103]}><ringGeometry args={[.855,.865,72]}/><meshBasicMaterial color="#F8DCA5" transparent opacity={opacity*.8}/></mesh>
    <mesh position={[0,0,-.095]} rotation={[0,Math.PI,0]}><circleGeometry args={[.915,72]}/><meshStandardMaterial color={tone} metalness={.72} roughness={.3} transparent opacity={opacity}/></mesh>
    <mesh position={[0,0,-.101]} rotation={[0,Math.PI,0]}><circleGeometry args={[.73,72]}/><meshBasicMaterial map={texture} transparent opacity={opacity}/></mesh>
    {[...Array(24)].map((_,i)=><mesh key={i} position={[.80*Math.cos(i*Math.PI/12),.80*Math.sin(i*Math.PI/12),.104]} rotation={[0,0,i*Math.PI/12]}><boxGeometry args={[.035,.01,.003]}/><meshBasicMaterial color="#F9D89B" transparent opacity={opacity*.8}/></mesh>)}
  </group>;
}
function Link({a,b,opacity=1,r=.015}){
 const mid=new THREE.Vector3(...a).add(new THREE.Vector3(...b)).multiplyScalar(.5);
 const diff=new THREE.Vector3(...b).sub(new THREE.Vector3(...a));
 const q=new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0,1,0),diff.clone().normalize());
 return <mesh position={mid} quaternion={q}><cylinderGeometry args={[r,r,diff.length(),8]}/><meshBasicMaterial color="#71D2F6" transparent opacity={opacity}/></mesh>;
}
function Node({position,label,growth,opacity}){
 const texture=useMemo(()=>markTexture(label,'#10213A'),[label]);useEffect(()=>()=>texture.dispose(),[texture]);
 return <group position={position} scale={growth}><mesh><sphereGeometry args={[.16,24,24]}/><meshStandardMaterial color={label==='D'?'#E7B778':'#A7DFF9'} emissive={label==='D'?'#9F5018':'#1A5B8D'} emissiveIntensity={.6} transparent opacity={opacity}/></mesh><mesh position={[0,0,.159]}><planeGeometry args={[.24,.24]}/><meshBasicMaterial map={texture} transparent opacity={opacity}/></mesh></group>;
}
function Sparks({frame}){
 const points=useMemo(()=>Array.from({length:54},(_,i)=>({x:Math.sin(i*41.7)*2.4,y:Math.cos(i*7.53)*4.6,z:-2.5+Math.sin(i*3.13)*1.2,r:i%7===0?.035:.015})),[]);
 return <group>{points.map((p,i)=><mesh key={i} position={[p.x+Math.sin(frame*.012+i)*.06,p.y+Math.cos(frame*.01+i)*.05,p.z]}><sphereGeometry args={[p.r,6,6]}/><meshBasicMaterial color={i%4?'#C8DEEA':'#EAC480'} transparent opacity={.35+.22*Math.sin(frame*.02+i)**2}/></mesh>)}</group>;
}
function CameraMotion({frame}){
 const {camera}=useThree();
 camera.position.set(.18*Math.sin(frame*.015), .12*Math.cos(frame*.013), 10.2-.25*Math.sin(frame*.011));camera.lookAt(0,0,0);camera.updateProjectionMatrix();return null;
}
function Scene({frame}){
 const q=lerp(frame,[75,105],[0,1]);const n=lerp(frame,[185,215],[0,1]);const end=lerp(frame,[290,320],[0,1]);
 const scale=1.03-.34*n+.08*end;const x= -.30*q+.30*n-.72*end;const y=-.42+.12*Math.sin(frame*.028)+1.5*end;
 const spin=2*Math.PI*(ease((frame-70)/26)+ease((frame-185)/26)+ease((frame-290)/26));
 const rr=.28+.15*Math.sin(frame*.025)+.22*q+.17*end+spin;
 const market=sceneAlpha(frame,83,200); const network=sceneAlpha(frame,188,315); const final=lerp(frame,[300,323,443,450],[0,1,1,0]);
 const pos=[[-1.35,.70,.1],[1.35,.7,.1],[-1.35,-1.15,.1],[1.35,-1.15,.1]];
 const growth=pos.map((_,i)=>ease((frame-(203+i*13))/18));
 const mid=[0,-.18,0];
 let transfer=Math.max(0,Math.min(1,(frame-270)/29));const from=pos[3],to=pos[0];let dot=transfer<.5?from.map((v,j)=>v+(mid[j]-v)*transfer*2):mid.map((v,j)=>v+(to[j]-v)*(transfer-.5)*2);
 return <>
  <CameraMotion frame={frame}/><ambientLight intensity={1.2}/><directionalLight position={[4,6,8]} intensity={3.2} color="#D8E9FF"/><pointLight position={[-3,-2,3]} intensity={28} color="#478DFF"/><pointLight position={[3,1,4]} intensity={22} color="#E8B676"/>
  <Sparks frame={frame}/>
  <group position={[x,y,0]} rotation={[.13,rr,.08*Math.sin(frame*.02)]}><Coin radius={scale}/></group>
  {[0,1,2].map(i=><mesh key={i} position={[x,y,-.4-i*.12]} rotation={[.45+i*.17,frame*.013+i*.4,frame*.012+i*.9]}>
    <torusGeometry args={[1.35+i*.2,.012,8,96]}/><meshBasicMaterial color={i===1?'#DDAE70':'#507FCF'} transparent opacity={.18+.24*(1-network)}/>
  </mesh>)}
  {market>0 && <group position={[0,-.4,-.65]} rotation={[.16,-.35,.03]}>{[0,1,2,3,4].map(i=><group key={i} position={[-1.1+i*.55,-1.4+i*.10,-.06*i]}>
    <mesh rotation={[.24,0,0]}><boxGeometry args={[.34,1.0+.18*Math.sin(frame*.055+i),.12]}/><meshStandardMaterial color={i%2?'#215C95':'#A47C45'} metalness={.6} roughness={.35} transparent opacity={market*.66}/></mesh>
  </group>)}</group>}
  {network>0 && <group position={[0,-.42,0]}>
    {pos.map((p,i)=>growth[i]>.01?<React.Fragment key={i}><Link a={mid} b={p} opacity={network*growth[i]}/><Node position={p} label={['A','B','C','D'][i]} growth={growth[i]} opacity={network}/></React.Fragment>:null)}
    {frame>=270 && frame<300 && <mesh position={dot}><sphereGeometry args={[.085,16,16]}/><meshBasicMaterial color="#FFE0A4"/></mesh>}
  </group>}
  {final>0 && <>
    <Coin mark="€" tone="#C9D3E1" radius={.58*final} position={[1.03,1.15,-.3]} rotation={[.2,-.35+.22*Math.sin(frame*.027),.17]} opacity={final}/>
    <Coin mark="¥" tone="#C9D3E1" radius={.43*final} position={[1.20,.05,-.8]} rotation={[-.1,.35+.24*Math.sin(frame*.022),-.15]} opacity={final}/>
  </>}
 </>;
}
function Words({scene,frame}){
 const {fps}=useVideoConfig();const alpha=sceneAlpha(frame,scene.start,scene.end);
 const top=scene.id==='payoff'?1060:scene.id==='markets'?225:255;
 return <div style={{position:'absolute',left:80,right:80,top,opacity:alpha}}>
  <div style={{display:'flex',alignItems:'center',gap:14,marginBottom:24,fontFamily:'Mono',fontSize:22,letterSpacing:4,color:'#A9C7D8'}}><span style={{width:36,height:2,background:'#D6A454'}}/>{scene.id==='question'?'THE GLOBAL MONEY QUESTION':scene.id==='markets'?'THE FINANCIAL FOUNDATION':scene.id==='network'?'HOW A NETWORK GROWS':'THE SHORT ANSWER'}</div>
  {scene.lines.map((line,i)=>{
   const sz=line.length>13?118:151;
   return <div key={line} style={{fontFamily:'Anton',fontSize:sz,lineHeight:1.02,letterSpacing:0,whiteSpace:'nowrap',color:i===1?'#E8BA77':'#F4F5ED',textShadow:'0 4px 32px rgba(10,17,35,.5)'}}>{line.split(' ').map((word,j)=>{
    const progress=spring({frame:frame-scene.start-i*5-j*3+4,fps,config:{damping:16,stiffness:130,mass:.7}});
    const drift=scene.id==='question'?Math.sin((frame-scene.start)*.07+j)*2:0;
    return <span key={j} style={{display:'inline-block',marginRight:'.18em',transform:`translate3d(0px,${(1-progress)*40+drift}px,0) scale(${.87+.13*progress})`,transformOrigin:'left center',opacity:progress}}>{word}</span>
   })}</div>
  })}
 </div>;
}
function Tag({children,style={}}){return <div style={{padding:'11px 21px',border:'1px solid rgba(164,211,235,.45)',borderRadius:8,background:'rgba(9,19,38,.65)',font:'bold 24px Manrope',letterSpacing:2,color:'#DBECF3',...style}}>{children}</div>}
function Overlays({frame}){
 const market=sceneAlpha(frame,85,195),net=sceneAlpha(frame,195,302),fin=sceneAlpha(frame,302,450);
 return <>
  <div style={{position:'absolute',top:125,left:80,right:80,display:'flex',justifyContent:'space-between',font:'23px Mono',letterSpacing:3,color:'#ABC6D5'}}><span>GLOBAL FINANCE / 01</span><span>15 SEC</span></div>
  <div style={{position:'absolute',top:153,left:80,right:80,height:1,background:'linear-gradient(90deg,#D2A466,transparent)'}}/>
  {plan.scenes.map(s=><Words scene={s} frame={frame} key={s.id}/>)}
  <div style={{position:'absolute',left:86,right:86,top:1285,display:'flex',justifyContent:'center',gap:13,opacity:market,transform:`translateY(${lerp(frame,[85,105],[30,0])}px)`}}><Tag>BUY</Tag><Tag>SELL</Tag><Tag>HOLD</Tag></div>
  <div style={{position:'absolute',left:0,right:0,top:1310,textAlign:'center',opacity:net,font:'23px Mono',letterSpacing:3,color:'#B9D7E6'}}>ILLUSTRATIVE NETWORK MODEL</div>
  <div style={{position:'absolute',left:0,right:0,top:1370,textAlign:'center',opacity:net*lerp(frame,[270,280],[0,1]),font:'bold 26px Manrope',letterSpacing:2,color:'#F4D8AC'}}>A NEW USER OPENS A NEW CONNECTION</div>
  <div style={{position:'absolute',left:0,right:0,top:1410,textAlign:'center',opacity:fin,font:'23px Mono',letterSpacing:3,color:'#B9D7E6'}}>USD LEADS  /  OTHER CURRENCIES EXIST</div>
  {plan.scenes.map(s=>{
   const start=s.voice_start,end=start+Math.ceil(s.voice_duration*30); if(frame<start||frame>=end)return null;
   return <div key={s.id} style={{position:'absolute',left:76,right:76,top:1520,minHeight:144,display:'flex',flexDirection:'column',justifyContent:'center',alignItems:'center',borderRadius:18,background:'rgba(5,11,23,.9)',border:'1px solid rgba(139,189,218,.26)',boxShadow:'0 12px 40px rgba(0,0,0,.25)',padding:'12px 16px',boxSizing:'border-box'}}>{s.caption.map(line=><div key={line} style={{font:'bold 37px Manrope',lineHeight:1.35,color:'#F7FAFB',whiteSpace:'nowrap'}}>{line}</div>)}</div>
  })}
 </>;
}
export function DollarVideo(){
 const frame=useCurrentFrame(); const [handle]=useState(()=>delayRender('loading the local fonts'));
 useEffect(()=>{Promise.all([document.fonts.load('900 100px Manrope'),document.fonts.load('100px Anton'),document.fonts.load('20px Mono')]).then(()=>continueRender(handle)).catch(e=>{console.error(e);continueRender(handle)});},[handle]);
 return <AbsoluteFill style={{background:'#070E1B',overflow:'hidden'}}>
  <style>{`@font-face{font-family:Anton;src:url('${staticFile('fonts/Anton-Regular.ttf')}')} @font-face{font-family:Manrope;src:url('${staticFile('fonts/Manrope-Variable.ttf')}');font-weight:200 800} @font-face{font-family:Mono;src:url('${staticFile('fonts/IBMPlexMono-Regular.ttf')}')}`}</style>
  <AbsoluteFill style={{background:'radial-gradient(ellipse at 54% 54%,#173D56 0%,#0A1930 42%,#050914 85%)'}}/>
  <AbsoluteFill style={{opacity:.16,backgroundImage:'linear-gradient(rgba(123,172,206,.20) 1px,transparent 1px),linear-gradient(90deg,rgba(123,172,206,.13) 1px,transparent 1px)',backgroundSize:'120px 120px',transform:`perspective(800px) rotateX(58deg) scale(2) translateY(${frame*.55}px)`,transformOrigin:'50% 80%'}}/>
  {[85,195,302].map((cut,i)=>{const p=lerp(frame,[cut-6,cut+9],[0,1]);const a=frame>=cut-6&&frame<=cut+9?Math.sin(p*Math.PI)*.4:0;return <div key={cut} style={{position:'absolute',left:`${-120+p*220}%`,top:0,width:'23%',height:'100%',transform:'skewX(-18deg)',background:'linear-gradient(90deg,transparent,#E8BA77,transparent)',opacity:a,filter:'blur(15px)'}}/>})}
  <ThreeCanvas width={1080} height={1920} camera={{position:[0,0,10.2],fov:38,near:.1,far:80}} gl={{antialias:true,alpha:true}}><Scene frame={frame}/></ThreeCanvas>
  <AbsoluteFill style={{background:'linear-gradient(180deg,rgba(3,7,16,.40) 0%,transparent 36%,transparent 68%,rgba(3,7,16,.55) 100%)',pointerEvents:'none'}}/>
  <Overlays frame={frame}/><Audio src={staticFile('audio/audio-mix.wav')}/>
 </AbsoluteFill>;
}
