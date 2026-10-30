// Extract the NSS/NSPR libraries bundled by @sparticuz/chromium for Linux
// environments lacking those system libraries. No system directories touched.
import {fileURLToPath} from 'node:url';import path from 'node:path';import fs from 'node:fs';import zlib from 'node:zlib';import {spawnSync} from 'node:child_process';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');const dest=process.argv[2]||'/tmp/dollar-chromium-libs';
fs.mkdirSync(dest,{recursive:true});const tar=path.join(dest,'al2023.tar');
fs.writeFileSync(tar,zlib.brotliDecompressSync(fs.readFileSync(path.join(root,'node_modules/@sparticuz/chromium/bin/al2023.tar.br'))));
const r=spawnSync('tar',['xf',tar,'-C',dest],{stdio:'inherit'});if(r.status!==0)process.exit(r.status||1);
console.log(`Extracted to ${dest}; run with LD_LIBRARY_PATH=${dest}/lib:/tmp:$LD_LIBRARY_PATH`);
