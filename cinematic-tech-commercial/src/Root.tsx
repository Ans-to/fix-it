import React from 'react';
import {Composition} from 'remotion';
import {Scene1} from './scenes/Scene1';
import {MOCK_FPS, SCENE_1_DURATION} from './config/mockTimings';

export const RemotionRoot: React.FC = () => (
  <Composition id="Scene1Prototype" component={Scene1} durationInFrames={SCENE_1_DURATION} fps={MOCK_FPS} width={1080} height={1920} />
);
