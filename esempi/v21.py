from props3 import *

TITLE = '8 settimane stessi carichi'
HOOK = '8 SETTIMANE.\nSTESSI CARICHI.'
HOOK_MIN = 2.2
LOOP = True; TAIL = 1.1
NONSPEECH = []
SIL = [-32, .1]
SENT = [
    ("Otto settimane.", 's1', {'OTTO'}, 0.1),
    ("Stessi carichi, stesse ripetizioni.", 's2', {'STESSI', 'STESSE'}, 0.1),
    ("E poi: «sono fermo».", 's3', {'FERMO'}, 0.1),
    ("Il corpo si adatta. Se lo stimolo non cresce, smette di cambiare.", 's4', {'ADATTA'}, 0.1),
    ("Esempio su quattro settimane! Prima: tre serie da otto. Seconda: tre da dieci. Terza: quattro da dieci. Quarta: più due chili e mezzo… e si riparte da otto.", 's5', {'PRIMA', 'SECONDA', 'TERZA', 'QUARTA'}, 0.1),
    ("Nell'editor di iki imposti la progressione settimana per settimana, e il cliente vede ogni volta cosa fare.", 's6', {"NELL'EDITOR"}, 0.1),
    ("Scrivi «progressione» nei commenti, e ti mando come funziona.", 's7', {'PROGRESSIONE'}, 0.0),
]
COLS = [('S1', '3×8', '60 kg'), ('S2', '3×10', '60 kg'), ('S3', '4×10', '60 kg'), ('S4', '3×8', '62,5 kg')]

def bored_curl(ctx, tau, x, s=1.0, face=None, buff=0.0):
    A = fig(ctx, 'client', curl(.9), face or dict(eyes='tired', mouth='flat', brows='neutral', look=(0, .3)), x, tau, seed=2, U_=U * s, buff=buff)
    dumbbell(ctx, A['hR'], 8, .6 * s); ctx.arc(*A['hR'], .085 * U * s, 0, 2 * math.pi); col(ctx, INK); ctx.fill()
    return A

def s1(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    floor(ctx, G)
    ph = tau * 3.2; wk = min(8, int(ph) + 1)
    flip_calendar(ctx, 90, 600, 400, f'S{wk}', '60 kg × 8', ph % 1 if wk < 8 else 0)
    bored_curl(ctx, tau, 780)

def s2(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    for i in range(6):
        t0 = .1 + i * L / 7
        k = prog(tau, t0, t0 + .15)
        if k <= 0: continue
        cx = 280 + (i % 2) * 520; cy = 620 + (i // 2) * 200
        stamp(ctx, (cx, cy), '60 kg × 8', k, cc=INK, size=60, rot=-.08 + .05 * (i % 3))
    floor(ctx, G)
    bored_curl(ctx, tau, 540, .7)

def s3(ctx, tau, L, wt):
    cam(ctx, 1.02, 540, 1000)
    tf = wt.get('FERMO', .6)
    floor(ctx, G)
    fig(ctx, 'client', lambda t: P(t=0, h=-6, la1=-35, la2=70, ra1=35, ra2=-70), dict(eyes='open', mouth='frown', brows='angry', look=(1, 0)), 320, tau, fx=.4, seed=2)
    fig(ctx, 'pt', lambda t: P(t=-4, h=-8, ra1=40, ra2=30), dict(eyes='wide', mouth='o' if tau > tf else 'smile', brows='worried', look=(-1, 0)), 790, tau, fx=-.4, seed=1)
    bubble(ctx, 380, 700, 360, 130, 'Sono fermo.', eback(prog(tau, tf - .3, tf)), (-.3, 1), WHITE, INK, 48, FONT)

def s4(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    ta = wt.get('ADATTA', .6); tc = wt.get('CRESCE', L * .6)
    x0, y0, w = 140, 760, 800
    rrect(ctx, x0 - 40, y0 - 220, w + 80, 360, 30); fill_stroke(ctx, WHITE, 7)
    text(ctx, 'STIMOLO', x0, y0 - 160, 40, FONT, INK, anchor='l')
    k = clamp(prog(tau, .1, 1.2))
    poly(ctx, [(x0, y0), (x0 + w * k, y0)], 14, GRAY)
    if k >= 1: ctx.move_to(x0 + w + 30, y0); ctx.line_to(x0 + w - 10, y0 - 30); ctx.line_to(x0 + w - 10, y0 + 30); ctx.close_path(); col(ctx, GRAY); ctx.fill()
    if tau > tc: stamp(ctx, (540, y0 - 30), 'NON CRESCE', prog(tau, tc - .1, tc + .2), size=70)
    floor(ctx, G)
    fig(ctx, 'client', lambda t: P(t=4, h=12, la1=-14, la2=-6, ra1=14, ra2=6), dict(eyes='tired', mouth='flat', brows='worried', look=(0, .6)), 540, tau, seed=2, U_=U * .75)
    for i in range(3):
        kk = (tau * .8 + i * .33) % 1
        text(ctx, 'z', 680 + kk * 60, 1100 - kk * 140, 44 + 24 * kk, FONT, INK)
    plate_label(ctx, (540, 1000), 'SI ADATTA', eback(prog(tau, ta - .1, ta + .2)), bg=INK, tc=WHITE, size=44)

def s5(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    ts = [wt.get(w_, 1 + i * 1.6) for i, w_ in enumerate(('PRIMA', 'SECONDA', 'TERZA', 'QUARTA'))]
    ks = [prog(tau, t - .1, t + .2) for t in ts]
    hl = max([i for i in range(4) if tau > ts[i] - .1] or [-1])
    table_cols(ctx, 60, 500, 960, 560, COLS, ks, hl)
    plate_label(ctx, (540, 1110), 'ESEMPIO: PANCA PIANA', eback(prog(tau, 0, .3)), bg=INK, tc=WHITE, size=34)
    floor(ctx, G)
    buff = clamp(sum(ks) / 4)
    fig(ctx, 'client', lambda t: P(t=0, h=-4, la1=-90, la2=-160, ra1=90, ra2=160), dict(eyes='happy' if buff > .5 else 'open', mouth='grin', brows='raised'), 540, tau, seed=2, U_=U * .55, buff=buff)

def s6(ctx, tau, L, wt):
    tv = wt.get('VEDE', L - 1.8); te = wt.get("NELL'EDITOR", .3)
    up = eout(prog(tau, 0, .35))
    sw = eout(prog(tau, tv - .3, tv + .1))
    hl = int(clamp(prog(tau, te + 1.2, tv - .4)) * 3.99) if tau > te + 1.2 else -1
    phone(ctx, 540 - 1100 * sw, lerp(2600, 1150, up), 640, 1180, editor_screen(prog(tau, te, te + 1.0), hl))
    if sw > 0:
        wk = 2 if tau < tv + .8 else 3
        phone(ctx, 540 + 1100 * (1 - sw), 1150, 640, 1180, client_week_screen(wk))

def s7(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    tp = wt.get('PROGRESSIONE', .4)
    floor(ctx, G)
    ph = tau * 1.2; i = int(ph) % 4
    flip_calendar(ctx, 90, 1020, 330, COLS[i][0], COLS[i][1] + (' +2,5' if i == 3 else ''), ph % 1 if (ph % 1) > .75 else 0)
    bored_curl(ctx, tau, 790, .85, dict(eyes='happy', mouth='grin', brows='raised'), buff=.7)
    cta_card(ctx, 'PROGRESSIONE', prog(tau, tp - .3, tp + .1), 640, tau)

SCENES = dict(s1=s1, s2=s2, s3=s3, s4=s4, s5=s5, s6=s6, s7=s7)

def SFX(fx, at):
    for i in range(7): fx('whoosh', at('s1', None, .25 + i * .31), .12)
    for i in range(6): fx('thud', at('s2', None, .1 + i * .3), .25)
    fx('pop', at('s3', 'FERMO', -.2), .35); fx('sad', at('s3', 'FERMO', .2), .15)
    fx('boing', at('s4', 'ADATTA'), .2); fx('thud', at('s4', 'CRESCE', -.1), .4)
    for i, w in enumerate(('PRIMA', 'SECONDA', 'TERZA', 'QUARTA')): fx('pop', at('s5', w), .3, f=900 + i * 150)
    fx('chime', at('s5', 'QUARTA', .6), .25)
    fx('whoosh', at('s6', None), .35); fx('pop', at('s6', "NELL'EDITOR", .5), .25); fx('whoosh', at('s6', 'VEDE', -.3), .3); fx('ding', at('s6', 'VEDE', .1), .25)
    fx('pop', at('s7', 'PROGRESSIONE', -.2), .35, f=800)

if __name__ == '__main__':
    main(sys.modules[__name__], '21')
