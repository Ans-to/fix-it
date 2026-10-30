import React from 'react';
import {registerRoot,Composition} from 'remotion';
import {Film} from './video.jsx';
import plan from './timeline.json';
registerRoot(()=> <Composition id="DollarSync" component={Film} durationInFrames={plan.format.duration_frames} fps={plan.format.fps} width={plan.format.width} height={plan.format.height}/>);
