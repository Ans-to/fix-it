import {bundle} from '@remotion/bundler';
import {selectComposition,renderStill,openBrowser} from '@remotion/renderer';
import chromium from '@sparticuz/chromium';import path from 'node:path';import fs from 'node:fs';
const root=path.resolve('dollar-motion-3d');const serveUrl=await bundle({entryPoint:path.join(root,'src/index.jsx'),publicDir:path.join(root,'public')});
const browserExecutable=await chromium.executablePath();const chromiumOptions={gl:'swangle'}; const browser=await openBrowser('chrome',{browserExecutable,chromiumOptions});
const opts={browserExecutable,chromiumOptions,logLevel:'error',puppeteerInstance:browser};
try{const composition=await selectComposition({serveUrl,id:'Dollar3D',...opts});fs.mkdirSync('/tmp/dollar-3d-samples',{recursive:true});
for(const f of [0,25,45,80,85,110,150,194,195,230,260,285,301,302,330,370,420,449]) {await renderStill({serveUrl,composition,frame:f,output:`/tmp/dollar-3d-samples/${String(f).padStart(3,'0')}.png`,imageFormat:'png',scale:.32,...opts});console.log('frame',f)}}finally{await browser.close({silent:true})}
