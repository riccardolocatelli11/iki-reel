#!/usr/bin/env python3
"""Motore dei caroselli iki (1080x1350, 4:5), stesso stile dei reel: fondo carta, gancio rosso, omini.
Uso da uno script cNN.py (modello: c01.py):  main_carosello(sys.modules[__name__], 'NN')
  python3 cNN.py          -> out/carosello_NN/01.jpg ... (una slide per file)
  python3 cNN.py sheet    -> build/csheet_NN.png (tutte le slide affiancate, per il controllo)

Lo script definisce TITLE, CAPTION e SLIDES, una lista di dict:
  {'kind': 'cover', 'hook': 'RIGA UNO\\nRIGA DUE', 'sub': 'frase sotto', 'art': fn(ctx)}   art in coordinate 1080x1350, zona y 640-1250
  {'kind': 'point', 'n': 1, 'title': '...', 'body': '...', 'icon': 'dumbbell'|..., 'art': fn(ctx) facoltativo}
  {'kind': 'iki', 'title': '...', 'body': '...', 'screen': content(ctx, w, h)}   schermata disegnata come nei reel
  {'kind': 'end'}   chiusura con «Mandalo a un collega» + logo
Icone disponibili: quelle di props3.icon (bulb, pose, dist, clock, sun, mug, moon, plate, pill, cross, bolt, dumbbell, target, euro).
"""
import os, sys
from props4 import *

CW, CH = 1080, 1350
HERE = os.path.dirname(os.path.abspath(__file__))

def wrap_lines(ctx, s, size, font, maxw):
    ctx.select_font_face(font); ctx.set_font_size(size)
    out = []
    for par in s.split('\n'):
        cur = ''
        for w in par.split():
            tr = (cur + ' ' + w).strip()
            if ctx.text_extents(tr).width > maxw and cur: out.append(cur); cur = w
            else: cur = tr
        out.append(cur)
    return out

def fit_block(ctx, s, size, font, maxw, maxlines):
    while size > 24:
        ls = wrap_lines(ctx, s, size, font, maxw)
        if len(ls) <= maxlines: return ls, size
        size -= 2
    return wrap_lines(ctx, s, size, font, maxw), size

def draw_lines(ctx, lines, x, y, size, font, c, lh=1.25, anchor='l'):
    for i, ln in enumerate(lines): text(ctx, ln, x, y + i * size * lh, size, font, c, anchor=anchor)
    return y + len(lines) * size * lh

def counter(ctx, i, n):
    text(ctx, f'{i}/{n}', 1010, 70, 30, FONTB, GRAY, anchor='r')
    logo(ctx, 100, 72, 90, 'rosso')

def slide_cover(ctx, d, i, n):
    lines = d['hook'].split('\n')
    ctx.select_font_face(FONT); size = 150
    for ln in lines:
        ctx.set_font_size(150); size = min(size, 150 * 940 / max(ctx.text_extents(ln).width, 1))
    ctx.save(); ctx.translate(540, 330); ctx.rotate(-.025)
    for k, ln in enumerate(lines):
        yy = (k - (len(lines) - 1) / 2) * size * 1.08
        text(ctx, ln, 0, yy + 10, size, FONT, INK, stroke=INK, sw=size * .16)
        text(ctx, ln, 0, yy, size, FONT, RED, stroke=INK, sw=size * .13)
    ctx.restore()
    if d.get('sub'):
        ls, sz = fit_block(ctx, d['sub'], 40, FONTB, 900, 2)
        draw_lines(ctx, ls, 540, 560, sz, FONTB, INK, anchor='c')
    if d.get('art'): d['art'](ctx)
    status_chip(ctx, 880, 1290, 'Scorri  →', RED, 1, 30)
    logo(ctx, 120, 1295, 100, 'rosso')

def slide_point(ctx, d, i, n):
    counter(ctx, i, n)
    ctx.arc(150, 250, 78, 0, 2 * math.pi); fill_stroke(ctx, RED, 8)
    text(ctx, str(d['n']), 150, 252, 86, FONT, WHITE)
    tl, ts = fit_block(ctx, d['title'], 62, FONT, 730, 3)
    draw_lines(ctx, tl, 260, 250 - (len(tl) - 1) * ts * .55, ts, FONT, INK, lh=1.1)
    bl, bs = fit_block(ctx, d['body'], 54, FONTB, 860, 7)
    ch = len(bl) * bs * 1.3 + 90
    rrect(ctx, 60 + 8, 400 + 10, 960, ch, 34); col(ctx, INK, .15); ctx.fill()
    rrect(ctx, 60, 400, 960, ch, 34); fill_stroke(ctx, WHITE, 8)
    draw_lines(ctx, bl, 110, 400 + 45 + bs * .55, bs, FONTB, INK, lh=1.3)
    if d.get('art'): d['art'](ctx)
    elif d.get('icon'):
        cy = (400 + ch + 1300) / 2
        ctx.save(); ctx.translate(540, cy); icon(ctx, d['icon'], (0, 0), 1.6); ctx.restore()

def slide_iki(ctx, d, i, n):
    counter(ctx, i, n)
    halo(ctx, (540, 900), 560, RED, .12)
    tl, ts = fit_block(ctx, d['title'], 60, FONT, 940, 2)
    draw_lines(ctx, tl, 540, 190, ts, FONT, RED, lh=1.1, anchor='c')
    bl, bs = fit_block(ctx, d['body'], 36, FONTB, 940, 3)
    y = draw_lines(ctx, bl, 540, 190 + len(tl) * ts * 1.1 + 20, bs, FONTB, INK, lh=1.25, anchor='c')
    ph = 1350 - y - 60
    pw = ph * 640 / 1120
    phone(ctx, 540, y + 30 + ph / 2, pw, ph, d['screen'])

def slide_end(ctx, d, i, n):
    counter(ctx, i, n)
    send_card(ctx, 1, 330, .5)
    text(ctx, d.get('line1', 'Ogni settimana una regola pratica'), 540, 600, 46, FONT, INK)
    text(ctx, d.get('line2', 'per il tuo lavoro da PT.'), 540, 660, 46, FONT, INK)
    fig(ctx, 'pt', lambda t: P(t=3, ra1=150, ra2=172, la1=-16, la2=-8), dict(eyes='happy', mouth='grin', brows='raised'),
        300, .4, fx=.2, seed=1, U_=U * .62, g=1180)
    fig(ctx, 'client', lambda t: P(t=0, ra1=150, ra2=170), dict(eyes='happy', mouth='smile', look=(-1, 0)), 760, .4, seed=3, U_=U * .58, g=1180)
    poly(ctx, [(120, 1182), (960, 1182)], 7)
    logo(ctx, 540, 1240, 120, 'rosso')
    text(ctx, "L'app del personal trainer · iki-app.com", 540, 1310, 28, FONTB, GRAY)

KINDS = dict(cover=slide_cover, point=slide_point, iki=slide_iki, end=slide_end)

def render_slide(d, i, n, paper):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, CW, CH); ctx = cairo.Context(s); ctx.set_antialias(cairo.ANTIALIAS_GOOD)
    ctx.set_source_surface(paper, 0, -285); ctx.paint()
    KINDS[d['kind']](ctx, d, i, n)
    s.flush()
    from PIL import Image
    a = np.frombuffer(s.get_data(), np.uint8).reshape(CH, CW, 4)[..., [2, 1, 0]]
    return Image.fromarray(a.copy())

def main_carosello(mod, cid):
    os.chdir(HERE); os.makedirs('build', exist_ok=True)
    paper, _keep = make_paper()
    n = len(mod.SLIDES)
    imgs = [render_slide(d, i + 1, n, paper) for i, d in enumerate(mod.SLIDES)]
    if sys.argv[1:2] == ['sheet']:
        from PIL import Image
        w, h = 360, 450; cols = min(n, 5); rows = (n + cols - 1) // cols
        sh = Image.new('RGB', (w * cols, h * rows), 'white')
        for i, im in enumerate(imgs): sh.paste(im.resize((w, h)), ((i % cols) * w, (i // cols) * h))
        p = f'build/csheet_{cid}.png'; sh.save(p); print('scritto', p); return
    out = f'out/carosello_{cid}'; os.makedirs(out, exist_ok=True)
    for i, im in enumerate(imgs): im.save(f'{out}/{i + 1:02d}.jpg', quality=93)
    print('scritto', out, f'({n} slide)')
