#!/usr/bin/env python3
"""Motore dei reel iki: omini su fondo carta, parole a tempo con la voce, gancio rosso,
CTA finale, loop, musica ed effetti. Ricostruito il 16/11/2026 a partire da reel.py.
Uso da uno script di reel (vedi esempi/ e README.md):  main(sys.modules[__name__], 'NN')
  python3 rNN.py            -> out/Reel iki - TITOLO.mp4
  python3 rNN.py sheet      -> build/sheet_NN.png (un fotogramma per scena, per il controllo)
  python3 rNN.py still 1.2 4.5
  python3 rNN.py times      -> stampa i tempi di scene e parole
"""
import os, json, difflib, multiprocessing
import math, subprocess, sys
import numpy as np, cairo
from scipy.ndimage import gaussian_filter

W, H, FPS = 1080, 1920, 30
INK = (0.10, 0.09, 0.08); RED = (0.84, 0.11, 0.13); BLUE = (0.16, 0.42, 0.86)
WHITE = (0.985, 0.975, 0.95); PAPERL = (0.97, 0.95, 0.905); GREEN = (0.12, 0.55, 0.30)
DARK = (0.22, 0.21, 0.20)
FONT = 'Montserrat Black'; FONTB = 'Montserrat ExtraBold'
G = 1500; U = 165

# ---------------------------------------------------------------- easing
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease(x): x = clamp(x); return x * x * (3 - 2 * x)
def eio(x):
    x = clamp(x); return 4 * x ** 3 if x < .5 else 1 - (-2 * x + 2) ** 3 / 2
def eout(x): x = clamp(x); return 1 - (1 - x) ** 3
def eback(x):
    x = clamp(x); c1 = 1.9; c3 = c1 + 1; return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2
def prog(t, a, b): return clamp((t - a) / (b - a)) if b > a else float(t >= a)
def lerp(a, b, k): return a + (b - a) * k

# ---------------------------------------------------------------- paper
def make_paper():
    rng = np.random.default_rng(7)
    base = np.array([232, 224, 206], float)
    low = gaussian_filter(rng.standard_normal((H // 8, W // 8)), 6)
    low = np.kron(low / np.abs(low).max(), np.ones((8, 8)))
    grain = rng.standard_normal((H, W)) * 3.5
    fib = gaussian_filter(rng.standard_normal((H, W)), (0.7, 5)) * 9
    spots = gaussian_filter((rng.random((H, W)) > 0.9993).astype(float), 3) * 900
    yy, xx = np.mgrid[0:H, 0:W]
    d = np.sqrt(((xx - W / 2) / (W * .6)) ** 2 + ((yy - H / 2) / (H * .6)) ** 2)
    vig = np.clip(d - .42, 0, None) ** 1.5 * 110
    lum = low * 9 + grain + fib - vig - spots
    img = base[None, None, :] + lum[..., None]
    img[..., 2] -= vig * .35
    img = np.clip(img, 0, 255).astype(np.uint8)
    arr = np.zeros((H, W, 4), np.uint8)
    arr[..., 0] = img[..., 2]; arr[..., 1] = img[..., 1]; arr[..., 2] = img[..., 0]; arr[..., 3] = 255
    surf = cairo.ImageSurface.create_for_data(arr, cairo.FORMAT_ARGB32, W, H)
    return surf, arr

# ---------------------------------------------------------------- helpers
def col(ctx, c, a=1.0): ctx.set_source_rgba(c[0], c[1], c[2], a)
def poly(ctx, pts, w, c=INK, a=1.0, close=False):
    ctx.move_to(*pts[0])
    for p in pts[1:]: ctx.line_to(*p)
    if close: ctx.close_path()
    col(ctx, c, a); ctx.set_line_width(w); ctx.stroke()
def ell(ctx, x, y, rx, ry):
    ctx.save(); ctx.translate(x, y); ctx.scale(max(rx, .01), max(ry, .01))
    ctx.arc(0, 0, 1, 0, 2 * math.pi); ctx.restore()
def rrect(ctx, x, y, w, h, r):
    r = min(r, w / 2, h / 2)
    ctx.new_sub_path()
    ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0); ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi); ctx.arc(x + r, y + r, r, math.pi, 1.5 * math.pi)
    ctx.close_path()
def fill_stroke(ctx, fillc, w, sc=INK, fa=1.0):
    col(ctx, fillc, fa); ctx.fill_preserve(); col(ctx, sc); ctx.set_line_width(w); ctx.stroke()
def text(ctx, s, x, y, size, font=FONT, c=INK, stroke=None, sw=0, anchor='c'):
    ctx.select_font_face(font); ctx.set_font_size(size)
    e = ctx.text_extents(s)
    if anchor == 'c': tx = x - e.width / 2 - e.x_bearing
    elif anchor == 'l': tx = x - e.x_bearing
    else: tx = x - e.width - e.x_bearing
    ty = y - (e.y_bearing + e.height / 2)
    ctx.move_to(tx, ty); ctx.text_path(s)
    if stroke:
        col(ctx, stroke); ctx.set_line_width(sw); ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.stroke_preserve()
    col(ctx, c); ctx.fill()
    return e.width
def cam(ctx, z, cx, cy):
    ctx.translate(W / 2, H / 2); ctx.scale(z, z); ctx.translate(-cx, -cy)
def dv(a):
    r = math.radians(a); return np.array([math.sin(r), math.cos(r)])

# ---------------------------------------------------------------- poses
ANG = ['t', 'h', 'la1', 'la2', 'ra1', 'ra2', 'll1', 'll2', 'rl1', 'rl2']
BASE = dict(t=0, h=0, la1=-14, la2=-8, ra1=14, ra2=8, ll1=-7, ll2=-3, rl1=7, rl2=3, x=0, y=0)
def P(**kw): d = dict(BASE); d.update(kw); return d
def mix(p, q, k): return {key: p[key] + (q[key] - p[key]) * k for key in p}

class Track:
    def __init__(s, keys):
        s.k = []; cur = dict(BASE)
        for item in keys:
            cur = dict(cur); cur.update(item[1])
            s.k.append((item[0], cur, item[2] if len(item) > 2 else eio))
    def __call__(s, t):
        k = s.k
        if t <= k[0][0]: return dict(k[0][1])
        for i in range(1, len(k)):
            if t <= k[i][0]:
                t0, p0, _ = k[i - 1]; t1, p1, e = k[i]
                return mix(p0, p1, e((t - t0) / (t1 - t0)))
        return dict(k[-1][1])

def walk(ph, fx=1, slump=0.0, amp=1.0):
    out = {}
    for side, off in (('l', 0), ('r', math.pi)):
        s = math.sin(ph + off); c = math.cos(ph + off)
        th = 24 * s * amp
        out[side + 'l1'] = fx * th
        out[side + 'l2'] = fx * (th - 38 * max(0, c) * amp - 4)
        a = -20 * s * amp
        out[side + 'a1'] = fx * a
        out[side + 'a2'] = fx * (a + 18)
    out['t'] = fx * (4 + 12 * slump); out['h'] = fx * 16 * slump
    out['y'] = -abs(math.cos(ph)) * 9 * amp
    return P(**out)

def joints(kind, p, U):
    tr = math.radians(p['t'])
    up = np.array([math.sin(tr), -math.cos(tr)]); perp = np.array([math.cos(tr), math.sin(tr)])
    hip = np.zeros(2); neck = up * 1.05 * U; R = .46 * U
    hr = math.radians(p['t'] + p['h'])
    head = neck + np.array([math.sin(hr), -math.cos(hr)]) * (R + .04 * U)
    if kind == 'pt':
        shL = neck - perp * .34 * U - up * .1 * U; shR = neck + perp * .34 * U - up * .1 * U
        hpL = hip - perp * .12 * U; hpR = hip + perp * .12 * U
    else:
        shL = shR = neck - up * .07 * U; hpL = hpR = hip
    eL = shL + dv(p['la1']) * .62 * U; hL = eL + dv(p['la2']) * .6 * U
    eR = shR + dv(p['ra1']) * .62 * U; hR = eR + dv(p['ra2']) * .6 * U
    kL = hpL + dv(p['ll1']) * .72 * U; fL = kL + dv(p['ll2']) * .74 * U
    kR = hpR + dv(p['rl1']) * .72 * U; fR = kR + dv(p['rl2']) * .74 * U
    return dict(hip=hip, neck=neck, head=head, shL=shL, shR=shR, hpL=hpL, hpR=hpR, eL=eL, hL=hL,
                eR=eR, hR=hR, kL=kL, fL=fL, kR=kR, fR=fR), dict(R=R, up=up, perp=perp, hr=p['t'] + p['h'])

def blinking(tt, seed):
    per = 3.1 + seed * .5; return (tt + seed * 1.37) % per < .1

# ---------------------------------------------------------------- face
def draw_face(ctx, R, f, tt, fx, LW, seed):
    sh = fx * .2 * R
    eyes = f.get('eyes', 'open'); lx, ly = f.get('look', (0, 0))
    if eyes in ('open', 'wide', 'tired') and blinking(tt, seed): eyes = 'closed'
    ew, eh, pr = .24 * R, .3 * R, .1 * R
    if eyes == 'wide': ew, eh, pr = .3 * R, .37 * R, .085 * R
    for s in (-1, 1):
        k = 1 - .3 * max(0, -s * fx)
        cx = s * .32 * R * (1 - .25 * abs(fx)) + sh; cy = -.06 * R; w = ew * k
        if eyes in ('open', 'wide', 'tired'):
            ell(ctx, cx, cy, w, eh); fill_stroke(ctx, WHITE, LW * .42)
            px, py = cx + lx * w * .42, cy + ly * eh * .4
            ctx.arc(px, py, pr, 0, 2 * math.pi); col(ctx, INK); ctx.fill()
            ctx.arc(px - pr * .35, py - pr * .4, pr * .32, 0, 2 * math.pi); col(ctx, WHITE); ctx.fill()
            if eyes == 'tired':
                ly_ = cy - eh * .05
                ctx.save(); ell(ctx, cx, cy, w, eh); ctx.clip()
                ctx.rectangle(cx - w - 5, cy - eh - 5, 2 * w + 10, ly_ - (cy - eh - 5)); col(ctx, WHITE); ctx.fill()
                ctx.restore()
                hw = w * math.sqrt(max(0, 1 - ((ly_ - cy) / eh) ** 2))
                poly(ctx, [(cx - hw, ly_), (cx + hw, ly_)], LW * .45)
        elif eyes == 'closed':
            ctx.move_to(cx - w, cy); ctx.curve_to(cx - w * .4, cy + eh * .35, cx + w * .4, cy + eh * .35, cx + w, cy)
            col(ctx, INK); ctx.set_line_width(LW * .45); ctx.stroke()
        elif eyes == 'happy':
            ctx.move_to(cx - w, cy + eh * .2); ctx.curve_to(cx - w * .4, cy - eh * .6, cx + w * .4, cy - eh * .6, cx + w, cy + eh * .2)
            col(ctx, INK); ctx.set_line_width(LW * .5); ctx.stroke()
        elif eyes == 'wince':
            d = -s
            poly(ctx, [(cx - d * w, cy - eh * .55), (cx + d * w * .7, cy), (cx - d * w, cy + eh * .55)], LW * .5)
    br = f.get('brows', 'neutral')
    if br != 'none':
        for s in (-1, 1):
            ix = s * .12 * R + sh; ox = s * .5 * R * (1 - .2 * abs(fx)) + sh
            iy, oy = {'neutral': (-.46, -.46), 'worried': (-.56, -.42), 'angry': (-.36, -.52),
                      'raised': (-.58, -.54)}[br]
            poly(ctx, [(ix, iy * R), (ox, oy * R)], LW * .45)
    m = f.get('mouth', 'smile'); mx = sh; my = .42 * R
    ctx.save(); ctx.translate(mx, 0)
    if m == 'smile':
        ctx.move_to(-.2 * R, .34 * R); ctx.curve_to(-.1 * R, .52 * R, .1 * R, .52 * R, .2 * R, .34 * R)
        col(ctx, INK); ctx.set_line_width(LW * .45); ctx.stroke()
    elif m == 'frown':
        ctx.move_to(-.17 * R, .52 * R); ctx.curve_to(-.1 * R, .38 * R, .1 * R, .38 * R, .17 * R, .52 * R)
        col(ctx, INK); ctx.set_line_width(LW * .45); ctx.stroke()
    elif m == 'flat':
        poly(ctx, [(-.13 * R, .45 * R), (.13 * R, .45 * R)], LW * .45)
    elif m == 'wavy':
        pts = [(x * R, .45 * R + .045 * R * math.sin(x * 38)) for x in np.linspace(-.2, .2, 14)]
        poly(ctx, pts, LW * .42)
    elif m == 'smirk':
        ctx.move_to(-.15 * R, .46 * R); ctx.curve_to(0, .5 * R, .12 * R, .44 * R, .2 * R, .34 * R)
        col(ctx, INK); ctx.set_line_width(LW * .45); ctx.stroke()
    elif m in ('grin', 'shout', 'o'):
        if m == 'grin':
            ctx.move_to(-.27 * R, .3 * R); ctx.line_to(.27 * R, .3 * R)
            ctx.curve_to(.25 * R, .74 * R, -.25 * R, .74 * R, -.27 * R, .3 * R); ctx.close_path()
        elif m == 'shout': ell(ctx, 0, .47 * R, .17 * R, .22 * R)
        else: ell(ctx, 0, .46 * R, .085 * R, .11 * R)
        path = ctx.copy_path()
        col(ctx, (.33, .06, .06)); ctx.fill()
        if m != 'o':
            ctx.save(); ctx.append_path(path); ctx.clip()
            ell(ctx, 0, .68 * R, .16 * R, .12 * R); col(ctx, (.93, .36, .38)); ctx.fill()
            if m == 'grin': ctx.rectangle(-.3 * R, .28 * R, .6 * R, .09 * R); col(ctx, WHITE); ctx.fill()
            ctx.restore()
        ctx.append_path(path); col(ctx, INK); ctx.set_line_width(LW * .42); ctx.stroke()
    ctx.restore()

# ---------------------------------------------------------------- figure
def bicep(ctx, a, b, U, out, LW):
    d = b - a; L = np.linalg.norm(d)
    if L < 1: return
    n = np.array([-d[1], d[0]]) / L
    if np.dot(n, out) < 0: n = -n
    p1 = a + d * .1; p2 = a + d * .88
    c1 = a + d * .22 + n * .27 * U; c2 = a + d * .72 + n * .2 * U
    ctx.move_to(*p1); ctx.curve_to(*c1, *c2, *p2); ctx.close_path()
    col(ctx, WHITE); ctx.fill_preserve(); ctx.new_path()
    ctx.move_to(*p1); ctx.curve_to(*c1, *c2, *p2); col(ctx, INK); ctx.set_line_width(LW * .7); ctx.stroke()

def draw_fig(ctx, kind, p, face, x, ground, U, tt, fx=0.0, ghost=False, seed=0, band=True):
    J, M = joints(kind, p, U)
    mf = max(J['fL'][1], J['fR'][1]) + .075 * U
    o = np.array([x + p['x'], ground - mf + p['y']])
    A = {k: v + o for k, v in J.items()}
    R, up, perp = M['R'], M['up'], M['perp']
    LW = .085 * U
    ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    if not ghost:
        lift = clamp(-p['y'] / 250)
        ell(ctx, o[0], ground + 4, .62 * U * (1 - .4 * lift), .09 * U * (1 - .4 * lift))
        col(ctx, INK, .14 * (1 - .5 * lift)); ctx.fill()
    # legs
    for hp, k, f, sd in ((A['hpL'], A['kL'], A['fL'], -1), (A['hpR'], A['kR'], A['fR'], 1)):
        poly(ctx, [hp, k, f], LW)
        fd = (1 if fx > 0 else -1) if abs(fx) > .25 else sd
        ell(ctx, f[0] + fd * .07 * U, f[1] + .01 * U, .15 * U, .07 * U); col(ctx, INK); ctx.fill()
    # torso
    if kind == 'pt':
        poly(ctx, [A['shL'], A['shR'], A['hpR'], A['hpL']], LW, close=True)
        ctx.move_to(*A['shL']); ctx.line_to(*A['shR']); ctx.line_to(*A['hpR']); ctx.line_to(*A['hpL']); ctx.close_path()
        fill_stroke(ctx, WHITE, LW)
        nk = A['neck']
        for s in (-1, 1):
            a = nk + perp * s * .03 * U - up * .42 * U; b = nk + perp * s * .29 * U - up * .24 * U
            c = nk + perp * s * .2 * U - up * .5 * U
            ctx.move_to(*a); ctx.curve_to(*c, *c, *b); col(ctx, INK); ctx.set_line_width(LW * .5); ctx.stroke()
        poly(ctx, [nk - up * .56 * U, nk - up * .78 * U], LW * .42)
        # cronometro
        c = nk - up * .66 * U + perp * .02 * U
        for s in (-1, 1):
            poly(ctx, [nk + perp * s * .1 * U - up * .02 * U, c + perp * s * .06 * U + up * .12 * U], LW * .3)
        poly(ctx, [c + up * .15 * U, c + up * .2 * U], LW * .55)
        ctx.arc(*c, .145 * U, 0, 2 * math.pi); fill_stroke(ctx, WHITE, LW * .55)
        ang = tt * math.pi
        poly(ctx, [c, c + np.array([math.sin(ang), -math.cos(ang)]) * .1 * U], LW * .35, RED)
        ctx.arc(*c, .025 * U, 0, 2 * math.pi); col(ctx, INK); ctx.fill()
    else:
        poly(ctx, [A['hip'], A['neck']], LW)
    # neck
    poly(ctx, [A['neck'], A['head']], LW)
    # arms
    for sh, e, h in ((A['shL'], A['eL'], A['hL']), (A['shR'], A['eR'], A['hR'])):
        if kind == 'pt':
            d = e - sh; d = d / (np.linalg.norm(d) + 1e-6)
            out = np.array([0, -1.0]) if abs(d[1]) < .8 else np.array([np.sign(sh[0] - A['neck'][0]) or 1.0, 0])
            bicep(ctx, sh, e, U, out, LW)
        poly(ctx, [sh, e, h], LW)
        ctx.arc(*h, .085 * U, 0, 2 * math.pi); col(ctx, INK); ctx.fill()
    # head
    hc = A['head']
    ctx.arc(*hc, R, 0, 2 * math.pi); fill_stroke(ctx, WHITE, LW)
    ctx.save(); ctx.translate(*hc); ctx.rotate(math.radians(M['hr']))
    if not ghost: draw_face(ctx, R, face, tt, fx, LW, seed)
    hair(ctx, R, LW, tt, seed)
    if kind == 'client' and band:
        ctx.save(); ctx.arc(0, 0, R - LW * .45, 0, 2 * math.pi); ctx.clip()
        ctx.move_to(-R, -.72 * R); ctx.curve_to(-.3 * R, -.62 * R, .3 * R, -.62 * R, R, -.72 * R)
        ctx.line_to(R, -.53 * R); ctx.curve_to(.3 * R, -.43 * R, -.3 * R, -.43 * R, -R, -.53 * R); ctx.close_path()
        fill_stroke(ctx, BLUE, LW * .35)
        ctx.restore()
        side = -1 if fx > .15 else 1
        b0 = np.array([side * .93 * R, -.6 * R])
        for i, (ln, ph) in enumerate(((.62, 0), (.5, 1.3))):
            pts = [b0 + np.array([side * ln * R * q, (.12 + .1 * i) * R * q + .06 * R * math.sin(tt * 7 + ph + q * 4) * q])
                   for q in np.linspace(0, 1, 8)]
            poly(ctx, pts, .17 * R, INK); poly(ctx, pts, .09 * R, BLUE)
    ctx.restore()
    return A

def draw_anim(ctx, kind, pose, face, x, ground, U, t, fx=0.0, seed=0, **kw):
    p = pose(t); p0 = pose(t - .1)
    v = sum(abs(p[k] - p0[k]) for k in ANG) + (abs(p['x'] - p0['x']) + abs(p['y'] - p0['y'])) * .35
    if v > 26:
        for dt, al in ((.05, .2), (.1, .09)):
            ctx.push_group(); draw_fig(ctx, kind, pose(t - dt), face, x, ground, U, t, fx, ghost=True, **kw)
            ctx.pop_group_to_source(); ctx.paint_with_alpha(al)
    return draw_fig(ctx, kind, p, face, x, ground, U, t, fx, seed=seed, **kw)

# ---------------------------------------------------------------- props
def floor(ctx, y, x0=40, x1=1040):
    poly(ctx, [(x0, y), (x0 + 380, y)], 5); poly(ctx, [(x0 + 405, y), (x1, y)], 5)
    for i in range(14):
        xx = x0 + 30 + i * 70
        poly(ctx, [(xx, y + 16), (xx + 34, y + 16)], 3, INK, .35)

def calendar(ctx, x, y, num, pop=1.0, w=220, h=240, head='SETTIMANA'):
    if pop <= 0: return
    ctx.save(); ctx.translate(x + w / 2, y + h / 2); ctx.scale(pop, pop); ctx.rotate(-.05); ctx.translate(-w / 2, -h / 2)
    rrect(ctx, 9, 12, w, h, 16); col(ctx, INK, .16); ctx.fill()
    rrect(ctx, 0, 0, w, h, 16); fill_stroke(ctx, PAPERL, 6)
    ctx.save(); rrect(ctx, 0, 0, w, h, 16); ctx.clip(); ctx.rectangle(0, 0, w, 66); col(ctx, RED); ctx.fill()
    for i in range(12): poly(ctx, [(i * 24 - 30, 66), (i * 24 + 6, 0)], 3, WHITE, .18)
    ctx.restore()
    poly(ctx, [(0, 66), (w, 66)], 5)
    rrect(ctx, 0, 0, w, h, 16); col(ctx, INK); ctx.set_line_width(6); ctx.stroke()
    for rx in (w * .27, w * .73):
        rrect(ctx, rx - 9, -24, 18, 44, 9); fill_stroke(ctx, WHITE, 5)
    text(ctx, head, w / 2, 38, 25, FONTB, WHITE)
    text(ctx, str(num), w / 2, 158, 128, FONT, INK)
    ctx.restore()

def dumbbell(ctx, c, ang=0, s=1.0):
    ctx.save(); ctx.translate(*c); ctx.rotate(math.radians(ang)); ctx.scale(s, s)
    poly(ctx, [(-66, 0), (66, 0)], 11)
    for sx in (-1, 1):
        for (px, pw, ph) in ((30, 20, 58), (48, 22, 76)):
            rrect(ctx, sx * px - pw / 2, -ph / 2, pw, ph, 6); fill_stroke(ctx, DARK, 5)
            poly(ctx, [(sx * px, -ph / 2 + 9), (sx * px, ph / 2 - 9)], 2.5, WHITE, .35)
    ctx.restore()

def barbell(ctx, c, ln=520, ang=0):
    ctx.save(); ctx.translate(*c); ctx.rotate(math.radians(ang))
    poly(ctx, [(-ln / 2, 0), (ln / 2, 0)], 10)
    for sx in (-1, 1):
        for (px, pw, ph) in ((ln / 2 - 95, 24, 150), (ln / 2 - 70, 24, 150), (ln / 2 - 47, 20, 110)):
            rrect(ctx, sx * px - pw / 2, -ph / 2, pw, ph, 7); fill_stroke(ctx, DARK, 5)
            poly(ctx, [(sx * px, -ph / 2 + 14), (sx * px, ph / 2 - 14)], 2.5, WHITE, .3)
        rrect(ctx, sx * (ln / 2 - 25) - 7, -14, 14, 28, 4); fill_stroke(ctx, WHITE, 4)
    ctx.restore()

def stairs(ctx, x0, g, n=4, sw=150, shh=72):
    pts = [(x0, g)]
    for i in range(n):
        pts += [(x0 + i * sw, g - (i + 1) * shh), (x0 + (i + 1) * sw, g - (i + 1) * shh)]
    pts += [(x0 + n * sw, g)]
    ctx.move_to(*pts[0])
    for p in pts[1:]: ctx.line_to(*p)
    ctx.close_path(); fill_stroke(ctx, PAPERL, 6)
    for i in range(n):
        yy = g - (i + 1) * shh
        for j in range(6):
            poly(ctx, [(x0 + i * sw + 8 + j * 12, yy + 12), (x0 + i * sw + 8 + j * 12 + 18, g - 8)], 2, INK, .12)
    posts = [(x0 + i * sw + 40, g - (i + 1) * shh) for i in range(n)]
    for (px, py) in posts: poly(ctx, [(px, py), (px, py - 240)], 7)
    rail = [(px, py - 240) for (px, py) in posts]
    rail = [(rail[0][0] - 60, rail[0][1] + 40)] + rail + [(rail[-1][0] + 90, rail[-1][1] - 60)]
    poly(ctx, rail, 18); poly(ctx, rail, 7, PAPERL)
    for i in range(n - 1):
        (ax, ay), (bx, by) = posts[i], posts[i + 1]
        for k in (.33, .66):
            xx = lerp(ax, bx, k); poly(ctx, [(xx, lerp(ay, by, k) - 230), (xx, g - (i + 1) * shh - 5 if k < .5 else g - (i + 2) * shh)], 3.5)

def mirror(ctx, mx, g, draw_ref=None):
    cy = g - 450; rx, ry = 180, 320
    for s in (-1, 1): poly(ctx, [(mx + s * 60, cy + ry - 10), (mx + s * 130, g)], 9)
    ell(ctx, mx + 12, cy + 16, rx, ry); col(ctx, INK, .15); ctx.fill()
    ell(ctx, mx, cy, rx, ry); fill_stroke(ctx, (.55, .42, .30), 8)
    for i in range(40):
        a = i / 40 * 2 * math.pi
        poly(ctx, [(mx + math.cos(a) * (rx - 4), cy + math.sin(a) * (ry - 4)),
                   (mx + math.cos(a + .05) * (rx - 20), cy + math.sin(a + .05) * (ry - 20))], 2.5, INK, .35)
    ell(ctx, mx, cy, rx - 24, ry - 24); fill_stroke(ctx, (.86, .9, .9), 5)
    if draw_ref:
        ctx.save(); ell(ctx, mx, cy, rx - 26, ry - 26); ctx.clip()
        ctx.push_group(); draw_ref(mx, cy + ry - 60); ctx.pop_group_to_source(); ctx.paint_with_alpha(.82)
        col(ctx, (.7, .85, .9), .18); ctx.paint()
        for k, (a, b) in enumerate(((-40, 60), (10, 30))):
            poly(ctx, [(mx + a - 120, cy - 120 + k * 40), (mx + a + 60, cy - 300 + k * 40)], b, WHITE, .35)
        ctx.restore()
    ell(ctx, mx, cy, rx - 24, ry - 24); col(ctx, INK); ctx.set_line_width(5); ctx.stroke()

def door(ctx, x, g, w=250, h=520, open_=1.0):
    top = g - h
    ctx.rectangle(x, top, w, h); fill_stroke(ctx, (.2, .19, .18), 8)
    for i in range(10): poly(ctx, [(x + 10, top + 30 + i * 48), (x + w - 10, top + 50 + i * 48)], 2, WHITE, .07)
    dx = -130 * open_
    ctx.move_to(x, top); ctx.line_to(x + dx, top - 26 * open_); ctx.line_to(x + dx, g + 18 * open_); ctx.line_to(x, g); ctx.close_path()
    fill_stroke(ctx, PAPERL, 6)
    for i in range(3): poly(ctx, [(x + dx * .15, top + 60 + i * 150), (x + dx * .85, top + 60 + i * 150 - 8 * open_)], 3, INK, .4)
    ctx.arc(x + dx * .8, g - h / 2, 9, 0, 2 * math.pi); col(ctx, INK); ctx.fill()
    rrect(ctx, x + w / 2 - 90, top - 90, 180, 56, 10); fill_stroke(ctx, GREEN, 5)
    text(ctx, 'USCITA', x + w / 2, top - 62, 30, FONT, WHITE)

def magnifier(ctx, c, r, content, hang=40):
    ctx.save()
    hd = dv(180 - 180 + 180 - hang)  # handle direction (down-right)
    hd = np.array([math.cos(math.radians(hang)), math.sin(math.radians(hang))])
    a = c + hd * (r + 8); b = c + hd * (r + 190)
    poly(ctx, [a, b], 40); poly(ctx, [a + hd * 40, b - hd * 12], 26, DARK)
    for k in range(5):
        q = a + hd * (60 + k * 24); n = np.array([-hd[1], hd[0]])
        poly(ctx, [q - n * 11, q + n * 11], 3, WHITE, .3)
    ctx.arc(*(c + np.array([10, 14])), r + 12, 0, 2 * math.pi); col(ctx, INK, .18); ctx.fill()
    ctx.save(); ctx.arc(*c, r, 0, 2 * math.pi); ctx.clip()
    col(ctx, (.97, .93, .9)); ctx.paint()
    content(ctx, c, r)
    ctx.arc(*c, r * .82, math.radians(200), math.radians(250)); col(ctx, WHITE, .55); ctx.set_line_width(16); ctx.stroke()
    ctx.restore()
    ctx.arc(*c, r, 0, 2 * math.pi); col(ctx, INK); ctx.set_line_width(22); ctx.stroke()
    ctx.arc(*c, r + 10, 0, 2 * math.pi); col(ctx, (.45, .45, .45)); ctx.set_line_width(4); ctx.stroke()
    ctx.restore()

def sparkle(ctx, x, y, s, a=1.0, rot=0):
    if s <= 0: return
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(s, s)
    ctx.move_to(0, -26)
    for i in range(4):
        ang = i * math.pi / 2
        ctx.curve_to(4 * math.sin(ang + .8), -4 * math.cos(ang + .8), 4 * math.sin(ang + .8), -4 * math.cos(ang + .8),
                     26 * math.sin(ang + math.pi / 2), -26 * math.cos(ang + math.pi / 2))
    ctx.close_path(); ctx.restore()
    col(ctx, WHITE, a); ctx.fill_preserve(); col(ctx, INK, a); ctx.set_line_width(4); ctx.stroke()

def burst(ctx, c, r0, r1, n=10, w=6, a=1.0, cc=INK, rot=0):
    for i in range(n):
        ang = rot + i * 2 * math.pi / n; d = np.array([math.cos(ang), math.sin(ang)])
        poly(ctx, [c + d * r0, c + d * r1], w, cc, a)

def zig(ctx, c, size, ang, a=1.0):
    ctx.save(); ctx.translate(*c); ctx.rotate(ang); ctx.scale(size, size)
    pts = [(-1, 0), (-.6, -.5), (-.2, .45), (.2, -.5), (.6, .45), (1, -.1)]
    pts = [(x * 60, y * 50) for x, y in pts]
    ctx.restore()
    ctx.save(); ctx.translate(*c); ctx.rotate(ang); ctx.scale(size, size)
    ctx.move_to(*pts[0])
    for p in pts[1:]: ctx.line_to(*p)
    ctx.restore()
    path = ctx.copy_path()
    col(ctx, INK, a); ctx.set_line_width(19 * size); ctx.stroke()
    ctx.append_path(path); col(ctx, RED, a); ctx.set_line_width(10 * size); ctx.stroke()

def drop(ctx, x, y, s=1.0, a=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.move_to(0, -24); ctx.curve_to(8, -8, 14, 0, 14, 8); ctx.arc(0, 8, 14, 0, math.pi); ctx.curve_to(-14, 0, -8, -8, 0, -24)
    ctx.restore(); col(ctx, (.72, .87, .98), a); ctx.fill_preserve(); col(ctx, INK, a); ctx.set_line_width(4); ctx.stroke()

def shake_lines(ctx, c, side, a=1.0):
    for i in range(3):
        r = 26 + i * 16
        ctx.arc(*c, r, math.radians(-40 + (0 if side > 0 else 180)), math.radians(40 + (0 if side > 0 else 180)))
        col(ctx, INK, a); ctx.set_line_width(5); ctx.stroke()

def chip(ctx, x, y, w, h, label, value, s=1.0, accent=RED):
    if s <= 0: return
    ctx.save(); ctx.translate(x + w / 2, y + h / 2); ctx.scale(s, s); ctx.translate(-w / 2, -h / 2)
    rrect(ctx, 6, 8, w, h, h / 2); col(ctx, INK, .15); ctx.fill()
    rrect(ctx, 0, 0, w, h, h / 2); fill_stroke(ctx, WHITE, 5)
    rrect(ctx, 10, 10, 190, h - 20, (h - 20) / 2); col(ctx, accent); ctx.fill()
    text(ctx, label, 105, h / 2, 28, FONT, WHITE)
    text(ctx, value, 222, h / 2, 34, FONTB, INK, anchor='l')
    ctx.restore()

DATA = [80, 80, 82.5, 85, 85, 87.5, 90, 92.5, 95]
def chart(ctx, x, y, w, h, p, lw=8, dots=True, labels=True):
    poly(ctx, [(x, y), (x, y + h), (x + w, y + h)], lw * .7)
    for k in range(1, 4): poly(ctx, [(x + 4, y + h - k * h / 4), (x + w, y + h - k * h / 4)], 2, INK, .15)
    pts = [(x + i / (len(DATA) - 1) * w, y + h - (v - 75) / 25 * h) for i, v in enumerate(DATA)]
    n = p * (len(pts) - 1)
    if n <= 0: return
    i = int(n); fr = n - i
    shown = pts[:i + 1] + ([(lerp(pts[i][0], pts[i + 1][0], fr), lerp(pts[i][1], pts[i + 1][1], fr))] if i + 1 < len(pts) else [])
    ctx.move_to(shown[0][0], y + h)
    for q in shown: ctx.line_to(*q)
    ctx.line_to(shown[-1][0], y + h); ctx.close_path(); col(ctx, RED, .12); ctx.fill()
    poly(ctx, shown, lw, RED)
    if dots:
        for q in pts[:i + 1]:
            ctx.arc(*q, lw * .95, 0, 2 * math.pi); fill_stroke(ctx, WHITE, lw * .5)
    if labels:
        text(ctx, '75', x - 16, y + h, 26, FONTB, INK, anchor='r')
        text(ctx, '100', x - 16, y, 26, FONTB, INK, anchor='r')

def phone(ctx, cx, cy, w, h, content, rot=0.0):
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(rot)
    rrect(ctx, -w / 2 + 12, -h / 2 + 16, w, h, w * .13); col(ctx, INK, .2); ctx.fill()
    rrect(ctx, -w / 2, -h / 2, w, h, w * .13); col(ctx, INK); ctx.fill()
    m = w * .045
    ctx.save(); rrect(ctx, -w / 2 + m, -h / 2 + m, w - 2 * m, h - 2 * m, w * .1); ctx.clip()
    col(ctx, (.99, .985, .975)); ctx.paint()
    ctx.translate(-w / 2 + m, -h / 2 + m); content(ctx, w - 2 * m, h - 2 * m)
    ctx.restore()
    rrect(ctx, -w * .12, -h / 2 + m + 8, w * .24, w * .05, w * .025); col(ctx, INK); ctx.fill()
    ctx.restore()


# ================================================================ aggiunte al motore
HERE = os.path.dirname(os.path.abspath(__file__))
GRAY = (0.55, 0.54, 0.52); YELLOW = (0.98, 0.80, 0.18); SKY = (0.72, 0.87, 0.98)
ORANGE = (0.96, 0.55, 0.16)

def sscale(ctx, s):
    s = max(abs(s), 1e-3); ctx.scale(s, s)

def hair(ctx, R, LW, tt, seed):
    """I due capellini dell'omino iki."""
    for i, s in enumerate((-1, 1)):
        bx = s * .12 * R; by = -R + LW * .2
        sw = .05 * R * math.sin(tt * 3 + seed + i)
        ctx.move_to(bx, by)
        ctx.curve_to(bx + s * .05 * R, by - .3 * R, bx + s * .28 * R + sw, by - .42 * R,
                     bx + s * .36 * R + sw, by - .3 * R)
        col(ctx, INK); ctx.set_line_width(LW * .55); ctx.stroke()

_LOGO = {}
def _logo_surf(kind):
    if kind not in _LOGO:
        from PIL import Image
        im = Image.open(os.path.join(HERE, 'assets', 'logo_rosso.png')).convert('RGBA')
        im = im.crop(im.getbbox()); a = np.asarray(im).astype(float)
        al = a[..., 3:4] / 255.0
        rgb = a[..., :3] if kind == 'rosso' else np.ones_like(a[..., :3]) * np.array(WHITE) * 255
        arr = np.zeros(a.shape, np.uint8)
        arr[..., 0] = (rgb[..., 2:3] * al)[..., 0]; arr[..., 1] = (rgb[..., 1:2] * al)[..., 0]
        arr[..., 2] = (rgb[..., 0:1] * al)[..., 0]; arr[..., 3] = a[..., 3]
        arr = np.ascontiguousarray(arr)
        surf = cairo.ImageSurface.create_for_data(arr, cairo.FORMAT_ARGB32, arr.shape[1], arr.shape[0])
        _LOGO[kind] = (surf, arr)
    return _LOGO[kind]

def logo(ctx, cx, cy, w, kind='rosso', a=1.0):
    """Logo iki (la scritta) centrato in (cx, cy), largo w. kind: 'rosso' o 'bianco'."""
    surf, arr = _logo_surf(kind); sw, sh = arr.shape[1], arr.shape[0]; s = w / sw
    ctx.save(); ctx.translate(cx - w / 2, cy - sh * s / 2); ctx.scale(s, s)
    ctx.set_source_surface(surf, 0, 0); ctx.get_source().set_filter(cairo.FILTER_BEST)
    ctx.paint_with_alpha(a); ctx.restore()

def check(ctx, c, s=1.0, cc=GREEN):
    if s <= 0: return
    ctx.save(); ctx.translate(*c); sscale(ctx, s)
    pts = [(-34, 2), (-10, 28), (38, -30)]
    ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    if cc != WHITE: poly(ctx, pts, 30, INK)
    poly(ctx, pts, 18, cc); ctx.restore()

def xmark(ctx, c, s=1.0, cc=RED):
    if s <= 0: return
    ctx.save(); ctx.translate(*c); sscale(ctx, s); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for a, b in (((-34, -34), (34, 34)), ((34, -34), (-34, 34))): poly(ctx, [a, b], 32, INK)
    for a, b in (((-34, -34), (34, 34)), ((34, -34), (-34, 34))): poly(ctx, [a, b], 19, cc)
    ctx.restore()

def plate_label(ctx, c, txt, k=1.0, bg=WHITE, tc=INK, size=36, rot=0.0):
    """Etichetta a pillola con testo, che entra scalando con k."""
    if k <= 0: return
    ctx.save(); ctx.translate(*c); sscale(ctx, k); ctx.rotate(rot)
    ctx.select_font_face(FONT); ctx.set_font_size(size); w = ctx.text_extents(txt).width + size * 1.5; h = size * 1.9
    rrect(ctx, -w / 2 + 6, -h / 2 + 8, w, h, h / 2); col(ctx, INK, .16); ctx.fill()
    rrect(ctx, -w / 2, -h / 2, w, h, h / 2); fill_stroke(ctx, bg, max(5, size * .14))
    text(ctx, txt, 0, 1, size, FONT, tc); ctx.restore()

def halo(ctx, c, r, cc=RED, a=.3):
    g = cairo.RadialGradient(c[0], c[1], 0, c[0], c[1], r)
    g.add_color_stop_rgba(0, cc[0], cc[1], cc[2], a); g.add_color_stop_rgba(1, cc[0], cc[1], cc[2], 0)
    ctx.save(); ctx.arc(c[0], c[1], r, 0, 2 * math.pi); ctx.set_source(g); ctx.fill(); ctx.restore()

def flip_in(ctx, c, k):
    """Trasformazione 'carta che si gira' attorno a c: usare tra ctx.save() e ctx.restore()."""
    k = clamp(k); sx = max(.02, eback(k)); sy = .85 + .15 * eout(k)
    ctx.translate(c[0], c[1]); ctx.scale(sx, sy); ctx.translate(-c[0], -c[1])

def curve_pts(a, b, bend=.3, n=24):
    a = np.array(a, float); b = np.array(b, float); d = b - a
    m = (a + b) / 2 + np.array([-d[1], d[0]]) * bend
    return [tuple((1 - q) ** 2 * a + 2 * q * (1 - q) * m + q ** 2 * b) for q in np.linspace(0, 1, n)]

def dashed_path(ctx, pts, p, w=8, cc=RED, dash=18, arrow=False):
    """Linea (tratteggiata se dash è corto) che si disegna da sola fino alla frazione p."""
    p = clamp(p)
    if p <= 0 or len(pts) < 2: return
    P_ = np.array(pts, float); seg = np.linalg.norm(np.diff(P_, axis=0), axis=1); tot = seg.sum(); goal = tot * p
    out = [tuple(P_[0])]; acc = 0
    for i, s in enumerate(seg):
        if acc + s >= goal:
            q = (goal - acc) / max(s, 1e-6); out.append(tuple(P_[i] + (P_[i + 1] - P_[i]) * q)); break
        out.append(tuple(P_[i + 1])); acc += s
    ctx.save(); ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    if dash < tot: ctx.set_dash([dash, dash * .9])
    poly(ctx, out, w, cc); ctx.restore()
    if arrow and len(out) > 1:
        a = np.array(out[-2]); b = np.array(out[-1]); d = b - a; d = d / (np.linalg.norm(d) + 1e-6); n = np.array([-d[1], d[0]])
        ctx.move_to(*(b + d * w * 2.2)); ctx.line_to(*(b - d * w + n * w * 1.8)); ctx.line_to(*(b - d * w - n * w * 1.8)); ctx.close_path()
        col(ctx, cc); ctx.fill()

def confetti(ctx, c, t, k, n=26):
    """Coriandoli che esplodono da c; k = avanzamento 0..1."""
    if k <= 0 or k >= 1: return
    rng = np.random.default_rng(11)
    for i in range(n):
        ang = rng.uniform(-math.pi, 0) + rng.uniform(-.3, .3); sp = rng.uniform(260, 620); cc = (RED, BLUE, YELLOW, GREEN)[i % 4]
        x = c[0] + math.cos(ang) * sp * k; y = c[1] + math.sin(ang) * sp * k + 620 * k * k
        ctx.save(); ctx.translate(x, y); ctx.rotate(t * 9 + i); ctx.rectangle(-11, -6, 22, 12)
        col(ctx, cc, 1 - k ** 3); ctx.fill_preserve(); col(ctx, INK, 1 - k ** 3); ctx.set_line_width(2.5); ctx.stroke(); ctx.restore()

def bubble(ctx, x, y, w, h, txt, k=1.0, tail=(-1, 1), fill=WHITE, tc=INK, size=40, font=FONT):
    """Fumetto centrato in (x, y); tail = direzione della codina, es. (-1, 1) = in basso a sinistra."""
    if k <= 0: return
    ctx.save(); ctx.translate(x, y); sscale(ctx, k)
    tx, ty = tail; bx = tx * w * .22; by = ty * h / 2
    ctx.move_to(bx - 22, by - ty * 6); ctx.line_to(bx + tx * 34, by + ty * 46); ctx.line_to(bx + 22, by - ty * 6); ctx.close_path()
    fill_stroke(ctx, fill, 7)
    rrect(ctx, -w / 2, -h / 2, w, h, min(w, h) * .32); fill_stroke(ctx, fill, 7)
    ctx.move_to(bx - 18, by - ty * 5); ctx.line_to(bx + tx * 28, by + ty * 36); ctx.line_to(bx + 18, by - ty * 5); ctx.close_path()
    col(ctx, fill); ctx.fill()
    if txt:
        for i, ln in enumerate(txt.split('\n')):
            text(ctx, ln, 0, (i - (len(txt.split('\n')) - 1) / 2) * size * 1.15, size, font, tc)
    ctx.restore()

def thought(ctx, x, y, r, content, k=1.0, src=None):
    """Nuvola di pensiero con dentro content(ctx, c, r); src = punto da cui partono le bollicine."""
    if k <= 0: return
    c = np.array([x, y], float)
    if src is not None:
        s = np.array(src, float)
        for i, q in enumerate((.2, .45, .7)):
            p = s + (c - s) * q * .8; rr = (10 + 9 * i) * clamp(k * 3 - i * .6)
            if rr > 0: ctx.arc(*p, rr, 0, 2 * math.pi); fill_stroke(ctx, WHITE, 5)
    ctx.save(); ctx.translate(*c); sscale(ctx, k); ctx.translate(-c[0], -c[1])
    for i in range(9):
        a = i / 9 * 2 * math.pi; ctx.arc(c[0] + math.cos(a) * r * .78, c[1] + math.sin(a) * r * .7, r * .38, 0, 2 * math.pi)
        col(ctx, INK); ctx.fill()
    for i in range(9):
        a = i / 9 * 2 * math.pi; ctx.arc(c[0] + math.cos(a) * r * .78, c[1] + math.sin(a) * r * .7, r * .38 - 7, 0, 2 * math.pi)
        col(ctx, WHITE); ctx.fill()
    ell(ctx, c[0], c[1], r * .86, r * .78); col(ctx, WHITE); ctx.fill()
    ctx.save(); ell(ctx, c[0], c[1], r * .9, r * .82); ctx.clip(); content(ctx, c, r * .8); ctx.restore()
    ctx.restore()

def clock(ctx, c, r, ang=0.0):
    ctx.arc(c[0] + 8, c[1] + 10, r, 0, 2 * math.pi); col(ctx, INK, .16); ctx.fill()
    ctx.arc(*c, r, 0, 2 * math.pi); fill_stroke(ctx, WHITE, r * .1)
    for i in range(12):
        a = i * math.pi / 6; d = np.array([math.sin(a), -math.cos(a)])
        poly(ctx, [np.array(c) + d * r * .8, np.array(c) + d * r * .9], r * .05 if i % 3 else r * .08)
    poly(ctx, [c, np.array(c) + np.array([math.sin(ang / 12), -math.cos(ang / 12)]) * r * .45], r * .09)
    poly(ctx, [c, np.array(c) + np.array([math.sin(ang), -math.cos(ang)]) * r * .7], r * .06, RED)
    ctx.arc(*c, r * .07, 0, 2 * math.pi); col(ctx, INK); ctx.fill()

def notebook(ctx, c, s=1.0, rot=0.0, lines=5, title=None):
    ctx.save(); ctx.translate(*c); ctx.rotate(rot); sscale(ctx, s)
    rrect(ctx, -130 + 8, -180 + 10, 260, 360, 14); col(ctx, INK, .16); ctx.fill()
    rrect(ctx, -130, -180, 260, 360, 14); fill_stroke(ctx, PAPERL, 7)
    for i in range(7): ctx.arc(-108, -150 + i * 50, 9, 0, 2 * math.pi); fill_stroke(ctx, WHITE, 4)
    y0 = -120
    if title: text(ctx, title, 10, -135, 34, FONT, RED); y0 = -80
    for i in range(lines): poly(ctx, [(-70, y0 + i * 48), (100 - (i % 3) * 30, y0 + i * 48)], 7, INK, .55)
    ctx.restore()

def stamp_x(ctx, c, k, s=1.0, rot=-.15):
    """Timbro ❌ che 'sbatte' sullo schermo (per la smentita dopo la domanda del gancio)."""
    if k <= 0: return
    z = 1 + 1.6 * (1 - eout(k))
    ctx.save(); ctx.translate(*c); ctx.rotate(rot); sscale(ctx, z * s)
    rrect(ctx, -92, -92, 184, 184, 34); col(ctx, RED, clamp(k * 2)); ctx.fill_preserve(); col(ctx, INK, clamp(k * 2)); ctx.set_line_width(10); ctx.stroke()
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for a, b in (((-46, -46), (46, 46)), ((46, -46), (-46, 46))): poly(ctx, [a, b], 30, WHITE, clamp(k * 2))
    ctx.restore()

# ================================================================ voce, tempi
SR = 44100
VO = 0.25                     # la voce parte dopo 0,25 s
def clean(w): return ''.join(ch for ch in w if ch.isalpha() or ch == "'").upper().strip("'")
def word_dur(w):
    d = min(.2 + .052 * len(clean(w)), .78)
    if w.endswith(','): d += .2
    if w.endswith(':'): d += .3
    if w.endswith('…'): d += .45
    if w[-1:] in '.?!': d += .38
    return d

def load_voice(path):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).astype(float)

def speech_segments(x, thr_db=-38, min_sil=.18):
    """Tratti parlati [(inizio, fine)] in secondi, separati da pause di almeno min_sil."""
    hop = int(.01 * SR); n = len(x) // hop
    rms = np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1) + 1e-12)
    voiced = 20 * np.log10(rms / (np.abs(x).max() + 1e-9) + 1e-9) > thr_db
    segs = []; i = 0
    while i < n:
        if voiced[i]:
            j = i
            while j < n and voiced[j]: j += 1
            if segs and i * .01 - segs[-1][1] < min_sil: segs[-1] = (segs[-1][0], j * .01)
            else: segs.append((i * .01, j * .01))
            i = j
        else: i += 1
    return [s for s in segs if s[1] - s[0] > .04], voiced

def _align_energy(mod, x):
    """Senza trascrizione: distribuisce le parole sul parlato, agganciando ogni frase alla pausa più vicina."""
    thr, ms = getattr(mod, 'SIL', [-38, .18]); segs, voiced = speech_segments(x, thr, ms)
    cum = np.concatenate([[0], np.cumsum(voiced)]) * .01
    def inv(v):      # tempo a cui si è accumulato v secondi di parlato
        return np.searchsorted(cum, v) * .01
    sents = [s.split() for s, *_ in mod.SENT]
    wts = [[.2 + .052 * len(clean(w)) for w in ws] for ws in sents]
    tot = sum(map(sum, wts)); V = cum[-1]
    starts = []; acc = 0
    for ws in wts: starts.append(inv(acc / tot * V)); acc += sum(ws)
    gaps = [s[0] for s in segs]
    for i in range(1, len(starts)):
        near = min(gaps, key=lambda g: abs(g - starts[i]))
        if abs(near - starts[i]) < .9 and near > starts[i - 1] + .25: starts[i] = near
    starts[0] = segs[0][0] if segs else 0
    ends = starts[1:] + [segs[-1][1] if segs else len(x) / SR]
    out = []
    for i, ws in enumerate(sents):
        a, b = int(starts[i] * 100), int(ends[i] * 100)
        c2 = np.concatenate([[0], np.cumsum(voiced[a:b])]) * .01; v = c2[-1] or 1e-6; acc = 0; tw = sum(wts[i])
        for w, wd in zip(ws, wts[i]):
            out.append(starts[i] + np.searchsorted(c2, acc / tw * v) * .01); acc += wd
    return out

def _align_words(mod, tr):
    """Con la trascrizione (parole con start/end): abbina le parole del copione a quelle sentite."""
    heard = [(clean(w.get('text', w.get('word', ''))), float(w['start'])) for w in tr
             if w.get('type', 'word') == 'word' and not str(w.get('text', w.get('word', ''))).startswith('[')
             and clean(w.get('text', w.get('word', '')))]
    script = [clean(w) for s, *_ in mod.SENT for w in s.split()]
    sm = difflib.SequenceMatcher(None, script, [h[0] for h in heard], autojunk=False)
    t = [None] * len(script)
    for a, b, n in sm.get_matching_blocks():
        for k in range(n): t[a + k] = heard[b + k][1]
    known = [(i, v) for i, v in enumerate(t) if v is not None]
    if not known: return None
    for i in range(len(t)):
        if t[i] is None:
            prev = [(j, v) for j, v in known if j < i]; nxt = [(j, v) for j, v in known if j > i]
            if prev and nxt:
                (j0, v0), (j1, v1) = prev[-1], nxt[0]; t[i] = v0 + (v1 - v0) * (i - j0) / (j1 - j0)
            elif prev: t[i] = prev[-1][1] + .28 * (i - prev[-1][0])
            else: t[i] = max(0, nxt[0][1] - .28 * (nxt[0][0] - i))
    for i in range(1, len(t)): t[i] = max(t[i], t[i - 1] + .04)
    return t

def build(mod, rid):
    """Tempi di scene e parole. Con audio_in/NN.mp3 segue la voce (meglio se c'è anche NN.json con le parole)."""
    vpath = os.path.join(HERE, 'audio_in', f'{rid}.mp3'); jpath = os.path.join(HERE, 'audio_in', f'{rid}.json')
    voice = None; times = None
    if os.path.exists(vpath):
        voice = load_voice(vpath)
        if os.path.exists(jpath):
            tr = json.load(open(jpath)); tr = tr.get('words', tr) if isinstance(tr, dict) else tr
            times = _align_words(mod, tr)
        if times is None: times = _align_energy(mod, voice)
        times = [VO + t for t in times]; vend = VO + len(voice) / SR
    scenes = []; words = []; k = 0; t = VO
    for i, (s, fn, red, extra) in enumerate(mod.SENT):
        ws = s.split(); red = {clean(r) for r in red}
        t0 = times[k] if times else t
        start = 0.0 if i == 0 else t0 - .12
        wt = {}
        for w in ws:
            tw = times[k] if times else t
            if clean(w):
                words.append((tw, clean(w), clean(w) in red, i)); wt.setdefault(clean(w), tw - start)
            t += word_dur(w); k += 1
        t += extra
        scenes.append(dict(fn=fn, start=start, wt=wt, sent=s, i=i))
    end = (vend if times else t) + getattr(mod, 'TAIL', 1.2)
    for i, sc in enumerate(scenes):
        sc['end'] = scenes[i + 1]['start'] if i + 1 < len(scenes) else end
        sc['L'] = sc['end'] - sc['start']
    return scenes, words, end, voice

# ================================================================ gancio e parole a schermo
LOOP_LEN = 0.4
def hook_text(ctx, t, lines, t_out):
    """Gancio: la frase intera in rosso nei primi secondi."""
    k = eback(prog(t, 0.0, .22)); out = prog(t, t_out - .18, t_out)
    if out >= 1: return
    ctx.select_font_face(FONT); size = 132
    for ln in lines:
        ctx.set_font_size(132); size = min(size, 132 * 940 / max(ctx.text_extents(ln).width, 1))
    ctx.save(); ctx.translate(540, 330); sscale(ctx, max(.6, k) * (1 - .25 * eio(out))); ctx.rotate(-.025)
    ctx.push_group()
    for i, ln in enumerate(lines):
        y = (i - (len(lines) - 1) / 2) * size * 1.12
        text(ctx, ln, 0, y + 9, size, FONT, INK, stroke=INK, sw=size * .16)
        text(ctx, ln, 0, y, size, FONT, RED, stroke=INK, sw=size * .13)
    ctx.pop_group_to_source(); ctx.paint_with_alpha(1 - out)
    ctx.restore()

def caption(ctx, t, words, scenes):
    cur = None
    for i, (wt, w, red, si) in enumerate(words):
        if wt <= t:
            nxt = words[i + 1][0] if i + 1 < len(words) else scenes[si]['end']
            if t < min(nxt, wt + 1.1): cur = (wt, w, red)
    if not cur: return
    wt, w, red = cur; age = t - wt
    s = 1 + .25 * (1 - eout(age / .13))
    ctx.select_font_face(FONT); ctx.set_font_size(124)
    e = ctx.text_extents(w); size = 124 * min(1, 880 / max(e.width, 1))
    ctx.save(); ctx.translate(540, 340); ctx.scale(s, s)
    if red: ctx.rotate(-.03)
    text(ctx, w, 0, 10, size, FONT, INK, stroke=INK, sw=16)
    text(ctx, w, 0, 0, size, FONT, RED if red else WHITE, stroke=INK, sw=15)
    ctx.restore()

# ================================================================ regia e render
class Timeline:
    def __init__(s, mod, rid):
        s.mod = mod; s.rid = rid
        s.scenes, s.words, s.end, s.voice = build(mod, rid)
        s.loop = bool(getattr(mod, 'LOOP', True))
        s.total = s.end + (LOOP_LEN if s.loop else 0)
        hook = getattr(mod, 'HOOK', None)
        s.hook = hook.split('\n') if hook else None
        s.hook_out = max(getattr(mod, 'HOOK_MIN', 1.8), s.scenes[0]['end'] if len(s.scenes) > 1 else 2.0) if s.hook else 0
        s.hook_out = min(s.hook_out, 3.2)
        s.reds = [w[0] for w in s.words if w[2]]

    def scene_at(s, t): return [sc for sc in s.scenes if sc['start'] <= t][-1]

    def draw_scene(s, ctx, sc, t, dx=0.0, a=1.0):
        tau = t - sc['start']; L = sc['L']
        ctx.save()
        z = 1 + .03 * clamp(tau / max(L, .1))                        # lenta spinta in avanti
        for tr in s.reds:                                            # colpo di zoom sulle parole rosse
            if 0 <= t - tr < .35: z += .035 * math.exp(-(t - tr) / .09)
        hx = 5 * math.sin(t * 1.3) + 3 * math.sin(t * 2.9 + 1); hy = 4 * math.sin(t * 1.7 + 2) + 2 * math.sin(t * 3.3)
        ctx.translate(540 + hx + dx, 960 + hy); ctx.scale(z, z); ctx.translate(-540, -960)
        if a < 1: ctx.push_group()
        ctx.save(); s.mod.SCENES[sc['fn']](ctx, tau, L, sc['wt']); ctx.restore()
        if a < 1: ctx.pop_group_to_source(); ctx.paint_with_alpha(a)
        ctx.restore()

    def frame(s, ctx, paper, t):
        ctx.identity_matrix(); ctx.set_source_surface(paper, 0, 0); ctx.paint()
        TR = .16
        if s.loop and t >= s.end:                                    # chiusura: rientra la prima scena, per il loop
            k = eio((t - s.end) / LOOP_LEN); last = s.scenes[-1]
            s.draw_scene(ctx, last, s.end - 1e-3, dx=-1080 * k)
            for g, al in ((.12, .15), (.06, .3)):
                if k < .97: s.draw_scene(ctx, s.scenes[0], 0.0, dx=1080 * (1 - max(0, k - g)), a=al * (1 - k))
            s.draw_scene(ctx, s.scenes[0], 0.0, dx=1080 * (1 - k))
            col(ctx, (1, .82, .55), .22 * math.sin(math.pi * k)); ctx.paint()
            return
            return
        sc = s.scene_at(t); dt = t - sc['start']; i = sc['i']
        if i > 0 and dt < TR:                                        # frustata d'ingresso con scia
            k = eout(dt / TR); d = 1 if i % 2 else -1
            for g, al in ((.18, .14), (.09, .28)):
                s.draw_scene(ctx, sc, t, dx=d * 620 * (1 - max(0, k - g)), a=al * (1 - k))
            s.draw_scene(ctx, sc, t, dx=d * 620 * (1 - k))
            col(ctx, (1, .82, .55), .28 * (1 - k)); ctx.paint()     # bagliore caldo sul taglio
        else:
            s.draw_scene(ctx, sc, t)
        if s.hook and t < s.hook_out: hook_text(ctx, t, s.hook, s.hook_out)
        else: caption(ctx, t, s.words, s.scenes)

def _worker(tl, a, b, path):
    paper, _keep = make_paper()
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); ctx = cairo.Context(surf); ctx.set_antialias(cairo.ANTIALIAS_GOOD)
    p = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}',
                          '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '21',
                          '-pix_fmt', 'yuv420p', path], stdin=subprocess.PIPE)
    for i in range(a, b):
        tl.frame(ctx, paper, i / FPS); surf.flush(); p.stdin.write(bytes(surf.get_data()))
    p.stdin.close(); p.wait()

def stills(tl, times, name):
    from PIL import Image
    paper, _keep = make_paper()
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); ctx = cairo.Context(surf); ctx.set_antialias(cairo.ANTIALIAS_GOOD)
    ims = []
    for t in times:
        tl.frame(ctx, paper, t); surf.flush()
        a = np.frombuffer(surf.get_data(), np.uint8).reshape(H, W, 4)[..., [2, 1, 0]]
        ims.append(Image.fromarray(a).resize((360, 640)))
    cols = min(6, len(ims)); rows = (len(ims) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * 360, rows * 640), 'white')
    for i, im in enumerate(ims): sheet.paste(im, ((i % cols) * 360, (i // cols) * 640))
    out = os.path.join(HERE, 'build', name); sheet.save(out); print('scritto', out, [round(t, 2) for t in times])

# ================================================================ audio
def _tt(d): return np.arange(int(d * SR)) / SR
def _lp(x, f):
    from scipy.signal import butter, lfilter
    b, a = butter(2, f / (SR / 2)); return lfilter(b, a, x)
def _hp(x, f):
    from scipy.signal import butter, lfilter
    b, a = butter(2, f / (SR / 2), 'high'); return lfilter(b, a, x)
_rng = np.random.default_rng(1)
def _ding(f=1320):
    t = _tt(1.2); return (np.sin(2 * np.pi * f * t) + .4 * np.sin(2 * np.pi * f * 2.76 * t)) * np.exp(-t * 3.5)
def _chime(f=1500):
    out = np.zeros(int(1.2 * SR))
    for i, m in enumerate((0, 4, 7, 12)):
        s = _ding(f * 2 ** (m / 12))[: len(out) - int(i * .07 * SR)]; out[int(i * .07 * SR):int(i * .07 * SR) + len(s)] += s * .6
    return out
def _sweep(f0, f1, d, shape=1.0):
    t = _tt(d); f = f0 + (f1 - f0) * t / d; return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / d) ** shape * .4
SYNTH = {
    'whoosh': lambda f=None, d=.35: _lp(_hp(_rng.standard_normal(int(d * SR)), 400), 3000) * np.sin(np.pi * _tt(d) / d) ** 2,
    'pop': lambda f=None: (lambda t: np.sin(2 * np.pi * ((f or 900) + 1400 * np.exp(-t * 60)) * t) * np.exp(-t * 45))(_tt(.09)),
    'tick': lambda f=None: _hp(_rng.standard_normal(int(.03 * SR)), 3000) * np.exp(-_tt(.03) * 160),
    'ding': lambda f=None: _ding(f or 1320),
    'chime': lambda f=None: _chime(f or 1500),
    'boing': lambda f=None: (lambda t: np.sin(2 * np.pi * np.cumsum(180 + 120 * np.sin(2 * np.pi * 7 * t) * np.exp(-t * 5)) / SR) * np.exp(-t * 6))(_tt(.45)),
    'clap': lambda f=None: _lp(_hp(_rng.standard_normal(int(.18 * SR)), 900), 5000) * np.exp(-_tt(.18) * 30) * (1 + (_tt(.18) < .012) * 2),
    'zing': lambda f=None: (lambda t: np.sin(2 * np.pi * np.cumsum(1800 * np.exp(-t * 3) + 300) / SR) * np.exp(-t * 5))(_tt(.5)),
    'swoosh_up': lambda f=None: _sweep(300, 1800, .4),
    'swoosh_down': lambda f=None: _sweep(1600, 250, .4),
    'thud': lambda f=None: (lambda t: np.sin(2 * np.pi * np.cumsum(110 * np.exp(-t * 18) + 45) / SR) * np.exp(-t * 9))(_tt(.35)),
    'buzz': lambda f=None: (lambda t: np.sign(np.sin(2 * np.pi * (f or 140) * t)) * .5 * np.minimum(1, (.4 - t) * 20) * np.minimum(1, t * 80))(_tt(.4)),
    'msg': lambda f=None: np.concatenate([np.sin(2 * np.pi * fq * _tt(.07)) * np.exp(-_tt(.07) * 25) for fq in ((f or 880), (f or 880) * 1.5)]),
    'beep': lambda f=None: (lambda t: np.sin(2 * np.pi * (f or 1000) * t) * np.minimum(1, t * 200) * np.minimum(1, (.18 - t) * 200))(_tt(.18)),
    'sad': lambda f=None: _lp(np.concatenate([(np.sin(2 * np.pi * 440 * 2 ** ((m - 69) / 12) * _tt(.33)) * np.exp(-_tt(.33) * 3)) for m in (55, 54, 53, 52)]), 2500),
    'shimmer': lambda f=None: sum(np.pad(_ding(2000 + 300 * i)[: int(.5 * SR)] * .3, (int(i * .1 * SR), int((10 - i) * .1 * SR))) for i in range(10)),
}

def _music(N, total):
    """Base lo-fi sintetizzata (96 bpm, Do - La min - Fa - Sol)."""
    L = np.zeros(N); R = np.zeros(N)
    def add(sig, t, g=1.0, pan=0.0):
        i = int(t * SR); sig = sig[: max(0, N - i)]
        L[i:i + len(sig)] += sig * g * (1 - max(0, pan)); R[i:i + len(sig)] += sig * g * (1 + min(0, pan))
    mtof = lambda m: 440 * 2 ** ((m - 69) / 12)
    def env(d, a, r): t = _tt(d); return np.minimum(1, t / a) * np.exp(-t / r)
    def keys(m, d):
        t = _tt(d); f = mtof(m)
        return (np.sin(2 * np.pi * f * t) + .35 * np.sin(4 * np.pi * f * t) * np.exp(-t * 6) + .12 * np.sin(6 * np.pi * f * t)) * env(d, .004, .9)
    def bass(m, d): t = _tt(d); f = mtof(m); return (np.sin(2 * np.pi * f * t) + .2 * np.sin(4 * np.pi * f * t)) * env(d, .01, .6)
    beat = 60 / 96; bar = 4 * beat
    chords = [[60, 64, 67, 71], [57, 60, 64, 67], [53, 57, 60, 64], [55, 59, 62, 65]]; roots = [36, 33, 29, 31]
    for b in range(int(total / bar) + 1):
        t0 = b * bar; ch = chords[b % 4]
        for off, d in ((0, 1.2), (1.5 * beat, .8), (3 * beat, .9)):
            for m in ch: add(keys(m, d), t0 + off, .05, -.2)
        add(bass(roots[b % 4], 1.4), t0, .22); add(bass(roots[b % 4] + 7, .9), t0 + 2.5 * beat, .16)
        for k in range(4):
            add(SYNTH['thud'](), t0 + k * beat, .32 if k % 2 == 0 else .18)
            if k % 2 == 1: add(_lp(_hp(_rng.standard_normal(int(.2 * SR)), 1500), 6000) * np.exp(-_tt(.2) * 22), t0 + k * beat, .08, .1)
            for h in (0, .5): add(_hp(_rng.standard_normal(int(.05 * SR)), 7000) * np.exp(-_tt(.05) * 70), t0 + (k + h) * beat, .035 if h else .05, .3)
    fade = np.ones(N); n1 = int(.3 * SR); fade[:n1] = np.linspace(0, 1, n1)
    fo = int((total - .5) * SR); fe = int(total * SR); fade[fo:fe] = np.linspace(1, 0, fe - fo); fade[fe:] = 0
    return L * fade, R * fade

def build_audio(tl, path):
    mod = tl.mod; total = tl.total; N = int(total * SR) + SR
    ML, MR = _music(N, total); ML *= .15; MR *= .15
    L = np.zeros(N); R = np.zeros(N)
    def add(sig, t, g=1.0, pan=0.0):
        i = max(0, int(t * SR)); sig = sig[: max(0, N - i)]
        L[i:i + len(sig)] += sig * g * (1 - max(0, pan)); R[i:i + len(sig)] += sig * g * (1 + min(0, pan))
    def fx(name, t, gain=.3, f=None, max=None, pan=0.0):
        if name.startswith('file:'):
            p = os.path.join(HERE, 'audio_in', name[5:] + '.mp3')
            if not os.path.exists(p): return
            sig = load_voice(p)
        else: sig = SYNTH.get(name, SYNTH['pop'])(f)
        if max: sig = sig[: int(max * SR)]; n = min(len(sig), int(.15 * SR)); sig[-n:] *= np.linspace(1, 0, n)
        add(sig, t, gain, pan)
    S = {s['fn']: s for s in tl.scenes}
    def at(fn, word=None, off=0.0):
        sc = S[fn]; return sc['start'] + (sc['wt'].get(clean(word), 0.0) if word else 0.0) + off
    for sc in tl.scenes[1:]: add(SYNTH['whoosh'](), sc['start'] - .12, .3, .2)
    if tl.hook: add(SYNTH['thud'](), 0.02, .5); add(SYNTH['pop'](), .05, .3)
    if hasattr(mod, 'SFX'): mod.SFX(fx, at)
    else:
        for t in tl.reds: add(SYNTH['pop'](1000), t - .03, .16)
    if tl.loop: add(SYNTH['whoosh'](), tl.end - .08, .3, -.2)
    amb = getattr(mod, 'AMB', None)
    if amb:
        p = os.path.join(HERE, 'audio_in', amb[0] + '.mp3')
        if os.path.exists(p):
            a = load_voice(p); a = np.tile(a, int(N / max(len(a), 1)) + 1)[:N]; ML += a * amb[1] * .5; MR += a * amb[1] * .5
    if tl.voice is not None:
        vo = np.zeros(N); v = tl.voice[: N - int(VO * SR)]; vo[int(VO * SR):int(VO * SR) + len(v)] = v
        vo = vo / (np.abs(vo).max() + 1e-9) * .85
        from scipy.ndimage import uniform_filter1d, maximum_filter1d    # la musica si abbassa sotto la voce
        env = uniform_filter1d(maximum_filter1d(np.abs(vo), int(.05 * SR)), int(.25 * SR))
        env = np.clip(env / (np.percentile(env[env > 0], 90) + 1e-9), 0, 1); g = 1 - .6 * env
        ML *= g; MR *= g; L *= (1 - .25 * env); R *= (1 - .25 * env)
        L += vo; R += vo
    L += ML; R += MR
    mix = np.stack([L, R], 1)[: int(total * SR)]
    mix = np.tanh(mix * 1.1) / np.tanh(1.1); mix = mix / np.abs(mix).max() * .9
    from scipy.io import wavfile
    wavfile.write(path, SR, (mix * 32767).astype(np.int16))

# ================================================================ main
def main(mod, rid):
    os.chdir(HERE); os.makedirs('build', exist_ok=True); os.makedirs('out', exist_ok=True)
    tl = Timeline(mod, rid); args = sys.argv[1:]
    if args and args[0] == 'times':
        for s in tl.scenes: print(f"{s['start']:6.2f}-{s['end']:6.2f} {s['fn']}  {s['sent']}\n         {({k: round(v, 2) for k, v in s['wt'].items()})}")
        print('gancio fino a', round(tl.hook_out, 2), '| fine voce+coda', round(tl.end, 2), '| totale', round(tl.total, 2), '| voce:', 'sì' if tl.voice is not None else 'NO (tempi stimati)')
        return
    if args and args[0] == 'still':
        return stills(tl, [float(a) for a in args[1:]], f'still_{rid}.png')
    if args and args[0] == 'sheet':
        ts = [.15, min(1.0, tl.hook_out * .6)]
        for s in tl.scenes: ts += [s['start'] + s['L'] * .35, s['start'] + s['L'] * .85]
        return stills(tl, sorted(set(round(t, 2) for t in ts if t < tl.end)), f'sheet_{rid}.png')
    n = int(round(tl.total * FPS)); nw = max(1, min(os.cpu_count() or 1, 4)); parts = []; procs = []
    for k in range(nw):
        a = n * k // nw; b = n * (k + 1) // nw; p = f'build/part_{rid}_{k}.mp4'; parts.append(p)
        pr = multiprocessing.Process(target=_worker, args=(tl, a, b, p))
        pr.start(); procs.append(pr)
    build_audio(tl, f'build/audio_{rid}.wav')
    for pr in procs: pr.join()
    if any(pr.exitcode for pr in procs): raise SystemExit('render fallito')
    open(f'build/list_{rid}.txt', 'w').write(''.join(f"file '{os.path.basename(p)}'\n" for p in parts))
    title = getattr(mod, 'TITLE', rid); out = f'out/Reel iki - {rid} - {title}.mp4'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', f'build/list_{rid}.txt',
                    '-i', f'build/audio_{rid}.wav', '-c:v', 'copy', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11',
                    '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-movflags', '+faststart', '-shortest', out], check=True)
    print('scritto', out, f'({tl.total:.1f} s)')
