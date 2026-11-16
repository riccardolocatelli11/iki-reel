#!/usr/bin/env python3
"""Colonna sonora dei promo iki (30 s), sintetizzata e sincronizzata con i tempi di template.html.

Stile: epico/cinematico con base trap a mezzo tempo (128 bpm), La minore.
  0-3 s     apertura: pad scuro, riser, BOOM sul logo (2.98)
  3-6.9     gancio: tensione, tick, colpi sulle barre rosse, riser
  6.95      DROP: 808, cassa, rullante, hi-hat a raffica, arpeggio
  12.55 / 22.65  zoom nello schermo: impatto;  17.5 giro del telefono: whoosh
  26.75     «Concentrati su ciò che conta.»: stacco, solo accordo largo
  28.45     logo finale: ultimo impatto e coda
Uso: python3 promo/music.py build/pNN.wav
"""
import sys, numpy as np
from scipy.signal import butter, lfilter
from scipy.io import wavfile

SR = 48000; TOTAL = 30.0; N = int(TOTAL * SR)
rng = np.random.default_rng(7)
L = np.zeros(N); R = np.zeros(N)

def tt(d): return np.arange(int(d * SR)) / SR
def lp(x, f): b, a = butter(2, min(f, SR / 2 - 100) / (SR / 2)); return lfilter(b, a, x)
def lpv(x, fc):
    """passa-basso a due poli con taglio che cambia nel tempo (fc: array)"""
    a = 1 - np.exp(-2 * np.pi * np.asarray(fc) / SR); y1 = np.zeros(len(x)); y2 = np.zeros(len(x)); p1 = p2 = 0.0
    for i in range(len(x)):
        p1 += a[i] * (x[i] - p1); p2 += a[i] * (p1 - p2); y2[i] = p2
    return y2
def hp(x, f): b, a = butter(2, f / (SR / 2), 'high'); return lfilter(b, a, x)
def mtof(m): return 440 * 2 ** ((m - 69) / 12)
def add(sig, t, g=1.0, pan=0.0):
    i = int(t * SR)
    if i >= N: return
    if i < 0: sig = sig[-i:]; i = 0
    sig = sig[: N - i]
    L[i:i + len(sig)] += sig * g * (1 - max(0, pan)); R[i:i + len(sig)] += sig * g * (1 + min(0, pan))

# ---------------------------------------------------------------- strumenti
def kick(d=.45):
    t = tt(d); f = 48 + 120 * np.exp(-t * 28)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7) + .3 * hp(rng.standard_normal(len(t)), 2000) * np.exp(-t * 200)
def snare(d=.32):
    t = tt(d); n = lp(hp(rng.standard_normal(len(t)), 1200), 8000) * np.exp(-t * 16)
    return n + .5 * np.sin(2 * np.pi * 190 * t) * np.exp(-t * 25) + .4 * lp(hp(rng.standard_normal(len(t)), 600), 3000) * np.exp(-t * 6)
def clap(d=.25):
    t = tt(d); e = sum(np.exp(-np.clip(t - k * .011, 0, None) * 60) * (t >= k * .011) for k in range(3)) + np.exp(-t * 14) * .6
    return lp(hp(rng.standard_normal(len(t)), 1000), 6000) * e * .7
def hat(d=.05, o=False):
    t = tt(d * (4 if o else 1)); return hp(rng.standard_normal(len(t)), 8000) * np.exp(-t * (18 if o else 90))
def sub808(m, d, glide_from=None):
    t = tt(d); f = mtof(m) * np.ones(len(t))
    if glide_from is not None: f = mtof(m) + (mtof(glide_from) - mtof(m)) * np.exp(-t * 18)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR); s = np.tanh(s * 2.2) / np.tanh(2.2)
    env = np.minimum(1, t / .005) * np.exp(-t * 1.1) * np.minimum(1, (d - t) / .03)
    return lp(s, 900) * env
def saw(f, t, det=0.0):
    out = 0
    for dd in (-det, 0, det):
        ph = (f * (1 + dd) * t) % 1; out = out + (2 * ph - 1)
    return out / 3
def pad(ms, d, cut=1600):
    t = tt(d); s = sum(saw(mtof(m), t, .006) for m in ms) / len(ms)
    env = np.minimum(1, t / .6) * np.minimum(1, (d - t) / .8)
    return lp(s, cut) * env
def pluck(m, d=.35):
    t = tt(d); f = mtof(m)
    s = saw(f, t, .004) * np.exp(-t * 9); return lpv(s, 2600 + 3000 * np.exp(-t * 12))
def brass(ms, d):
    t = tt(d); s = sum(saw(mtof(m), t, .01) for m in ms) / len(ms)
    env = np.minimum(1, t / .04) * np.exp(-t * .9) * np.minimum(1, (d - t) / .4)
    return lpv(s, 900 + 2200 * np.exp(-t * 2)) * env
def riser(d, f0=200, f1=4000):
    t = tt(d); n = rng.standard_normal(len(t)); out = np.zeros(len(t)); seg = int(.02 * SR)
    for i in range(0, len(t), seg):
        k = i / len(t); fc = f0 * (f1 / f0) ** k
        out[i:i + seg] = lp(hp(n[i:i + seg], max(60, fc * .5)), fc)[: len(out[i:i + seg])]
    tone = np.sin(2 * np.pi * np.cumsum(f0 * .5 * (f1 / f0) ** (t / d) * .25) / SR) * .3
    return (out + tone) * (t / d) ** 2
def impact(d=2.5):
    t = tt(d); boom = np.sin(2 * np.pi * np.cumsum(38 + 90 * np.exp(-t * 9)) / SR) * np.exp(-t * 1.6)
    crash = lp(hp(rng.standard_normal(len(t)), 3000), 12000) * np.exp(-t * 2.2) * .35
    return np.tanh((boom + crash) * 1.6)
def whoosh(d=.6):
    t = tt(d); return lp(hp(rng.standard_normal(len(t)), 500), 4000) * np.sin(np.pi * t / d) ** 2
def pop(f=900):
    t = tt(.08); return np.sin(2 * np.pi * (f + 900 * np.exp(-t * 60)) * t) * np.exp(-t * 50)
def tick():
    t = tt(.03); return hp(rng.standard_normal(len(t)), 4000) * np.exp(-t * 150)

# ---------------------------------------------------------------- arrangiamento (La minore: Am F C G)
BPM = 128; B = 60 / BPM; BAR = 4 * B; DROP = 6.95
PROG = [(57, [57, 60, 64]), (53, [53, 57, 60]), (48, [55, 60, 64]), (55, [55, 59, 62])]   # radice, accordo
roots = [45, 41, 48, 43]

# apertura e gancio
add(pad([45, 52, 57, 60], 7.4, 900), 0.0, .16)
add(riser(2.7, 150, 3000), .3, .12, .2)
add(impact(3.5), 2.96, .55)
for i in range(12): add(tick(), 3.1 + i * B, .10 if i % 2 else .16, .3 * (-1) ** i)
for i in range(6): add(kick(.3) * .6, 3.1 + i * 2 * B, .35)
for i in range(3): add(snare() * .5, 4.73 + i * .15, .35, -.2 + .2 * i); add(whoosh(.25) * .4, 4.73 + i * .15, .35, .2 - .2 * i)   # barre rosse
add(riser(1.6, 300, 6000), DROP - 1.6, .16, -.2)
add(snare(), DROP - .23, .2); add(snare(), DROP - .12, .25)

# drop: trap a mezzo tempo fino al finale
end_beat = 26.7
t0 = DROP; bar = 0
while t0 < end_beat:
    r, ch = PROG[bar % 4]
    add(sub808(roots[bar % 4] - 12, BAR * .98, glide_from=roots[(bar - 1) % 4] - 12 if bar else None), t0, .55)
    add(pad([m + 12 for m in ch], BAR, 1400 + 600 * (bar % 2)), t0, .07, -.3)
    add(pad([m + 12 for m in ch], BAR, 1400 + 600 * (bar % 2)), t0, .07, .3)
    for k in range(8):                       # arpeggio di plucks in crome
        tk = t0 + k * B / 2
        if tk >= end_beat: break
        add(pluck(ch[k % 3] + 12 + (12 if k in (3, 7) else 0)), tk, .09, .35 * (-1) ** k)
    for k, g in ((0, 1.0), (2.5, .7)): add(kick(), t0 + k * B, .55 * g)
    add(snare(), t0 + 2 * B, .42); add(clap(), t0 + 2 * B, .25)
    for k in range(16):                      # hi-hat in semicrome, raffiche a fine battuta
        th = t0 + k * B / 4
        if th >= end_beat: break
        g = .07 if k % 2 else .1
        add(hat(), th, g, .25)
        if bar % 2 == 1 and k >= 12:
            for j in range(1, 3): add(hat(.03), th + j * B / 12, .06, .25)
    add(hat(o=True), t0 + 3.5 * B, .05, -.25)
    t0 += BAR; bar += 1

# accenti sulla regia del video
add(impact(2.2), DROP, .5)
for tz in (12.55, 22.65): add(riser(.9, 500, 7000), tz - .9, .14); add(impact(1.8), tz, .42)
add(whoosh(.9), 17.1, .3, .4); add(whoosh(.9), 17.5, .25, -.4)
for t in (9.3, 9.85, 10.4, 13.9, 14.45, 15.0, 18.6, 19.15, 19.7, 23.7, 24.25, 24.8):   # card che escono
    add(pop(1100), t, .12, .3)
add(kick(.3), 8.95, .3)                      # atterraggio dell'omino

# finale
add(riser(1.0, 300, 5000), 25.75, .14)
add(impact(3.0), 26.75, .5)
add(brass([45, 52, 57, 60, 64], 3.0), 26.75, .22)
add(pad([45, 52, 57, 64, 69], 3.3), 26.75, .14)
for i, m in enumerate((69, 72, 76)): add(pluck(m, .6), 26.85 + i * .32, .14, (-.3, 0, .3)[i])
add(impact(1.6), 28.45, .45); add(sub808(33, 1.5), 28.45, .5)
add(brass([45, 52, 57, 64], 1.5), 28.45, .18)

# master
fade = np.ones(N); n = int(.05 * SR); fade[:n] = np.linspace(0, 1, n)
fo = int(29.3 * SR); fade[fo:] = np.linspace(1, 0, N - fo)
mix = np.stack([L, R], 1) * fade[:, None]
mix = np.tanh(mix * 1.35) / np.tanh(1.35)
mix = mix / (np.abs(mix).max() + 1e-9) * .89
out = sys.argv[1] if len(sys.argv) > 1 else 'build/promo_music.wav'
wavfile.write(out, SR, (mix * 32767).astype(np.int16)); print(out)
