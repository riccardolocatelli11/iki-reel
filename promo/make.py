#!/usr/bin/env python3
"""Promo iki in stile «Il tuo lavoro è allenare» — costruisce l'HTML del video.

Uso:
  python3 promo/make.py promo/pNN.json            -> build/pNN.html
  python3 promo/make.py grid NOME_SCHERMATA        -> build/grid_NOME.png (griglia per scegliere i ritagli)

Le schermate sono quelle vere dell'app: gestionale-pt/public/pt-vetrina-<NOME>.png
(clone di riccardolocatelli11/gestionale-pt, percorso in IKI_APP, default ../gestionale-pt).
Coordinate dei ritagli: nello schermo del telefono, larghezza 832 px (come la griglia).
"""
import base64, io, json, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
APP = os.environ.get('IKI_APP', os.path.join(os.path.dirname(ROOT), 'gestionale-pt'))
BUILD = os.path.join(ROOT, 'build')
SCREEN_BOX = (124, 124, 956, 1866)   # schermo dentro i mockup pt-vetrina-*.png (1080x1920)


def b64(data, mime):
    return f'data:{mime};base64,' + base64.b64encode(data).decode()


def screen(name):
    p = os.path.join(APP, 'public', f'pt-vetrina-{name}.png')
    if not os.path.exists(p):
        sys.exit(f'Schermata mancante: {p}. Schermate disponibili: ' + ', '.join(sorted(
            f[11:-4] for f in os.listdir(os.path.join(APP, 'public')) if f.startswith('pt-vetrina-'))))
    return Image.open(p).convert('RGB').crop(SCREEN_BOX)


def jpg(im, q=86):
    b = io.BytesIO(); im.save(b, 'JPEG', quality=q, optimize=True); return b.getvalue()


def video(name):
    src = os.path.join(APP, 'public', 'video', f'{name}.mp4')
    if not os.path.exists(src): sys.exit(f'Video esercizio mancante: {src}')
    with tempfile.TemporaryDirectory() as d:
        out = os.path.join(d, 'v.mp4')
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', src, '-an', '-vf', 'scale=960:-2',
                        '-c:v', 'libx264', '-crf', '28', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], check=True)
        return open(out, 'rb').read()


def grid(name):
    im = screen(name); g = im.resize((416, int(416 * im.height / im.width))); d = ImageDraw.Draw(g)
    for y in range(0, im.height, 100):
        d.line([(0, y / 2), (416, y / 2)], fill=(0, 200, 255)); d.text((2, y / 2 + 1), str(y), fill=(0, 160, 255))
    for x in range(0, im.width, 100):
        d.line([(x / 2, 0), (x / 2, g.height)], fill=(0, 200, 255)); d.text((x / 2 + 1, 2), str(x), fill=(0, 160, 255))
    os.makedirs(BUILD, exist_ok=True); out = os.path.join(BUILD, f'grid_{name}.png'); g.save(out); print(out)


def fontcss():
    F = os.path.join(HERE, 'fonts'); rd = lambda f: b64(open(os.path.join(F, f), 'rb').read(), 'font/woff2')
    return (f'@font-face{{font-family:"Unbounded";font-weight:200 900;src:url({rd("unbounded-latin-wght-normal.woff2")}) format("woff2")}}\n'
            f'@font-face{{font-family:"Geist";font-weight:100 900;src:url({rd("geist-latin-wght-normal.woff2")}) format("woff2")}}\n'
            f'@font-face{{font-family:"Geist Mono";font-weight:500;src:url({rd("geist-mono-latin-500-normal.woff2")}) format("woff2")}}\n'
            f'@font-face{{font-family:"Geist Mono";font-weight:600;src:url({rd("geist-mono-latin-600-normal.woff2")}) format("woff2")}}')


def build(cfg_path):
    cfg = json.load(open(cfg_path)); pid = os.path.splitext(os.path.basename(cfg_path))[0]
    assert len(cfg['scenes']) == 4, 'servono esattamente 4 scene'
    assert len(cfg['hook']['lines']) == 3, 'il gancio ha 3 righe'
    L = os.path.join(HERE, 'logo'); png = lambda f: b64(open(os.path.join(L, f), 'rb').read(), 'image/png')
    shots = {s['screen'] for s in cfg['scenes']}
    crops = cfg.get('crops', {})
    used = {c['src'] for s in cfg['scenes'] for c in s['cards'] if c['type'] == 'img'}
    for u in used: assert u in crops, f'ritaglio "{u}" non definito in crops'
    vids = {c['src'] for s in cfg['scenes'] for c in s['cards'] if c['type'] == 'vid'}
    assets = dict(sym=png('simbolo.png'), wm=png('scritta.png'),
                  letters=[png(f'scritta_{n}.png') for n in ('i1', 'k', 'i2')],
                  scr={k: b64(jpg(screen(k)), 'image/jpeg') for k in shots},
                  crop={k: b64(jpg(screen(crops[k][0]).crop(tuple(crops[k][1:])), 90), 'image/jpeg') for k in used},
                  vid={k: b64(video(k), 'video/mp4') for k in vids})
    conf = {k: v for k, v in cfg.items() if k not in ('title', 'crops', 'caption')}
    html = (open(os.path.join(HERE, 'template.html')).read()
            .replace('__TITLE__', cfg.get('title', 'iki Promo'))
            .replace('__FONTCSS__', fontcss())
            .replace('__OMINO__', open(os.path.join(HERE, 'omino.js')).read())
            .replace('__ASSETS__', json.dumps(assets))
            .replace('__CONFIG__', json.dumps(conf, ensure_ascii=False)))
    os.makedirs(BUILD, exist_ok=True); out = os.path.join(BUILD, f'{pid}.html'); open(out, 'w').write(html)
    print(out, len(html) // 1024, 'KB')


if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == 'grid': grid(sys.argv[2])
    elif len(sys.argv) == 2: build(sys.argv[1])
    else: sys.exit(__doc__)
