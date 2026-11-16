// Registra un promo iki fotogramma per fotogramma.
//   node promo/render.mjs build/pNN.html sheet            -> build/sheet_pNN.png (12 fotogrammi chiave)
//   node promo/render.mjs build/pNN.html still 9.6 24.9   -> build/still_pNN_<t>.png
//   node promo/render.mjs build/pNN.html video "out/Promo iki - NN - TITOLO.mp4"
// Video: 1080x1920, 30 fps, 30 s, due processi in parallelo (circa 10-15 minuti).
import { createRequire } from 'module';
import { spawn, spawnSync } from 'child_process';
import fs from 'fs'; import path from 'path';
const require = createRequire(import.meta.url);
let pw; try { pw = require('playwright'); } catch { pw = require('/opt/npm-tools/node_modules/playwright'); }
const { chromium } = pw;

const [file, mode = 'sheet', ...rest] = process.argv.slice(2);
if (!file) { console.log('uso: node promo/render.mjs build/pNN.html sheet|still|video ...'); process.exit(1); }
const abs = path.resolve(file), id = path.basename(file, '.html'), BUILD = path.join(path.dirname(abs));
const CLEAN = 'body{padding:0!important;overflow:hidden}#ui{display:none!important}#page{display:block!important}#frame{border-radius:0!important;box-shadow:none!important;width:1080px!important;height:1920px!important}#stage{transform:none!important;left:0!important;top:0!important}';

async function open(scale = 1) {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: scale });
  await p.goto('file://' + abs); await p.addStyleTag({ content: CLEAN });
  await p.evaluate(() => window.ikiReady); await p.waitForTimeout(400);
  return [b, p];
}
const shot = async (p, t, o) => { await p.evaluate(v => window.ikiSeek(v), t); return p.screenshot({ ...o, clip: { x: 0, y: 0, width: 1080, height: 1920 } }); };

if (mode === 'sheet' || mode === 'still') {
  const ts = mode === 'sheet' ? [1.8, 4.6, 6.3, 8.2, 9.6, 11.9, 15.0, 20.0, 24.2, 25.6, 28.0, 29.4] : rest.map(Number);
  const [b, p] = await open();
  for (const t of ts) await shot(p, t, { path: path.join(BUILD, `still_${id}_${t}.png`) });
  await b.close();
  if (mode === 'sheet') {
    const py = `from PIL import Image\nts=${JSON.stringify(ts.map(String))}\nW,H=270,480\nc=Image.new('RGB',(W*6,H*2))\nfor i,t in enumerate(ts): c.paste(Image.open(r'${BUILD}/still_${id}_'+t+'.png').resize((W,H)),((i%6)*W,(i//6)*H))\nc.save(r'${BUILD}/sheet_${id}.png')\n`;
    spawnSync('python3', ['-c', py], { stdio: 'inherit' });
    ts.forEach(t => fs.rmSync(path.join(BUILD, `still_${id}_${t}.png`)));
    console.log(path.join(BUILD, `sheet_${id}.png`));
  }
} else if (mode === 'video') {
  const out = path.resolve(rest[0] || `out/${id}.mp4`); fs.mkdirSync(path.dirname(out), { recursive: true });
  const FPS = 30, N = 30 * FPS, parts = 2, seg = Math.ceil(N / parts);
  const work = async k => {
    const segf = path.join(BUILD, `${id}_seg${k}.mp4`);
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
      '-c:v', 'libx264', '-preset', 'medium', '-crf', '14', '-pix_fmt', 'yuv420p', segf], { stdio: ['pipe', 'inherit', 'inherit'] });
    const [b, p] = await open();
    for (let i = k * seg; i < Math.min(N, (k + 1) * seg); i++) {
      let buf; for (let tries = 0; ; tries++) { try { buf = await shot(p, i / FPS, { type: 'jpeg', quality: 95, timeout: 60000 }); break; } catch (e) { if (tries > 2) throw e; } }
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    }
    ff.stdin.end(); await new Promise(r => ff.on('close', r)); await b.close(); return segf;
  };
  const segs = await Promise.all([...Array(parts).keys()].map(work));
  const list = path.join(BUILD, `${id}_segs.txt`); fs.writeFileSync(list, segs.map(s => `file '${s}'`).join('\n'));
  // traccia audio muta: Instagram gestisce meglio i reel con una traccia audio
  const r = spawnSync('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', list, '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo',
    '-shortest', '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-profile:v', 'high', '-pix_fmt', 'yuv420p', '-r', '30', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', out], { stdio: 'inherit' });
  segs.forEach(s => fs.rmSync(s)); fs.rmSync(list);
  if (r.status !== 0) process.exit(r.status);
  console.log(out);
} else { console.log('modo sconosciuto: ' + mode); process.exit(1); }
