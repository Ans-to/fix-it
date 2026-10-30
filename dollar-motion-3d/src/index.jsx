import {registerRoot,Composition} from 'remotion';
import React from 'react';
import {DollarVideo} from './video.jsx';
import plan from './plan.json';
registerRoot(()=><Composition id="Dollar3D" component={DollarVideo} durationInFrames={plan.format.duration_frames} fps={plan.format.fps} width={plan.format.width} height={plan.format.height}/>);
