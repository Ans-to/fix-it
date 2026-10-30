import React, {useRef} from 'react';
import {createRoot} from 'react-dom/client';
import {Player, type PlayerRef} from '@remotion/player';
import {Scene1} from './scenes/Scene1';
import {MOCK_FPS, SCENE_1_DURATION, SCENE_1_TIMINGS} from './config/mockTimings';
import './preview.css';

const App: React.FC = () => {
  const player = useRef<PlayerRef>(null);
  const cues = [
    {label: 'The question', frame: SCENE_1_TIMINGS.why},
    {label: 'Two countries', frame: SCENE_1_TIMINGS.two},
    {label: 'Trade & currency', frame: SCENE_1_TIMINGS.trade},
    {label: 'Impact · NEITHER', frame: SCENE_1_TIMINGS.neither},
    {label: 'The payoff', frame: SCENE_1_TIMINGS.issues},
  ];
  return <main className="workspace">
    <header className="masthead"><div className="brand"><span className="brand-mark">◈</span><span>DIRECTOR<span className="brand-light"> / MOTION LAB</span></span></div><span className="header-status"><span className="status-dot"/> PROTOTYPE MODE</span></header>
    <div className="layout">
      <section className="stage"><div className="stage-head"><div><div className="eyebrow">PLAYBACK / 01</div><h2>Scene preview<span className="stage-accent">.</span></h2></div><div className="stage-note">9:16 &nbsp;·&nbsp; 30 FPS</div></div>
        <div className="player-outer"><Player ref={player} component={Scene1} durationInFrames={SCENE_1_DURATION} compositionWidth={1080} compositionHeight={1920} fps={MOCK_FPS} controls loop showVolumeControls={false} style={{width: '100%', height: '100%'}} /></div>
        <div className="stage-footer"><span><span className="status-dot"/> READY TO REVIEW</span><span>4.7 SEC / 141 FRAMES</span></div>
      </section>
      <aside className="direction"><div className="chapter">SCENE 01 <span> / </span> THE QUESTION</div><h1>Why trade in<br/><em>someone else’s</em><br/>currency?</h1><p className="intro">An illustrated question, told through moving type and a shared unit travelling between two fictional participants.</p>
        <div className="notice"><span className="notice-icon">↗</span><div><strong>Silent prototype</strong><p>No audio files are loaded. All word timings are estimates for visual review only.</p></div></div>
        <div className="cue-head"><span>JUMP TO MOMENT</span><span>FRAME</span></div>
        <div className="cue-list">{cues.map((cue, index)=><button key={cue.label} type="button" onClick={()=>player.current?.seekTo(cue.frame)}><span className="cue-index">0{index+1}</span><span className="cue-label">{cue.label}</span><span className="cue-frame">{String(cue.frame).padStart(3,'0')}</span><span className="cue-arrow">↗</span></button>)}</div>
        <div className="direction-foot"><span>CREATIVE DIRECTION</span><p>3D markers A + B are illustrative. The USD object and camera move through the scene; the impact lands on a mock cue.</p></div>
      </aside>
    </div>
  </main>;
};
createRoot(document.getElementById('root')!).render(<App/>);
