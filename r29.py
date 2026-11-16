from props4 import *

TITLE = 'Ogni serie a cedimento'
HOOK = "OGNI SERIE\nA CEDIMENTO?"
LOOP = True; TAIL = 1.4
CTA = 'SFORZO'
SENT = [
    ("Ogni serie a cedimento?", 's1', {'CEDIMENTO'}, 0.1),
    ("Sbagliato.", 's2', {'SBAGLIATO'}, 0.1),
    ("Il cedimento stanca tantissimo, e le serie dopo crollano.", 's3', {'STANCA', 'CROLLANO'}, 0.1),
    ("Fermati una o due ripetizioni prima: lo stimolo è quasi lo stesso, ma recuperi molto meglio.", 's4', {'DUE', 'STESSO', 'MEGLIO'}, 0.1),
    ("Il cedimento tienilo per l'ultima serie, sugli esercizi di isolamento.", 's5', {"L'ULTIMA", 'ISOLAMENTO'}, 0.1),
    ("In iki, a fine esercizio il cliente ti dice com'è andata: facile, giusto, duro, o al limite.", 's6', {'FACILE', 'GIUSTO', 'DURO', 'LIMITE'}, 0.1),
    ("Scrivi «sforzo» nei commenti, e ti mando come funziona.", 's7', {'SFORZO'}, 0.0),
]

def lifter(ctx, tau, x, strain, freq=1.1, s=.95, seed=2):
    """Cliente che fa curl con il manubrio; strain 0..1 = quanto è al limite."""
    face = dict(eyes='wince' if strain > .6 else 'open', mouth='shout' if strain > .6 else ('flat' if strain > .25 else 'smile'),
                brows='angry' if strain > .6 else 'neutral', look=(.4, -.2))
    A = fig(ctx, 'client', curl(freq * (1 - .55 * strain), strain), face, x, tau, fx=.15, seed=seed, U_=U * s)
    hold_dumbbell(ctx, A, 'R', 8, .95 * s)
    if strain > .4:
        for i in range(3):
            k = (tau * 1.3 + i * .33) % 1
            drop(ctx, A['head'][0] - 95 + i * 95, A['head'][1] - 60 + k * 120, .9, (1 - k) * strain)
        shake_lines(ctx, A['eR'] + np.array([40, 0]), 1, strain * (.5 + .5 * math.sin(tau * 30)))
    return A

def s1(ctx, tau, L, wt):
    cam(ctx, 1.04, 540, 1040)
    floor(ctx, G)
    halo(ctx, (540, 1150), 520, RED, .10 + .05 * math.sin(tau * 9))
    lifter(ctx, tau, 540, 1.0, s=1.25)
    n = 9 + int(tau * 1.1)
    plate_label(ctx, (250, 760), f'REP {n}', 1 + .08 * math.sin(tau * 12), bg=INK, tc=WHITE, size=50, rot=-.06)
    plate_label(ctx, (830, 700), 'ANCORA!', eback(prog(tau, .35, .6)), bg=RED, tc=WHITE, size=46, rot=.07)

def s2(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    floor(ctx, G)
    ts = wt.get('SBAGLIATO', .15)
    no = math.sin(tau * 14) * 9
    fig(ctx, 'pt', lambda t: P(t=0, h=no, la1=-60, la2=60, ra1=60, ra2=-60), dict(eyes='open', mouth='flat', brows='angry', look=(0, 0)), 540, tau, seed=1, U_=U * .95)
    stamp_x(ctx, (540, 690), prog(tau, ts - .05, ts + .2), 1.5)

def s3(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    ta = wt.get('STANCA', .6); tc = wt.get('CROLLANO', L - .6)
    lv = lerp(1.0, .08, eio(prog(tau, ta - .2, ta + .9)))
    battery(ctx, (540, 640), lv, 1.5)
    plate_label(ctx, (540, 770), 'ENERGIA', 1, bg=WHITE, tc=INK, size=34)
    reps = (10, 6, 3); x0 = 190
    for i, r in enumerate(reps):
        k = eback(prog(tau, tc - .5 + i * .22, tc - .25 + i * .22))
        if k <= 0: continue
        h = 34 * r; x = x0 + i * 260
        ctx.save(); ctx.translate(x + 90, 1330); ctx.scale(1, max(k, .02)); ctx.translate(-(x + 90), -1330)
        rrect(ctx, x + 8, 1330 - h + 10, 180, h, 18); col(ctx, INK, .15); ctx.fill()
        rrect(ctx, x, 1330 - h, 180, h, 18); fill_stroke(ctx, (GREEN, YELLOW, RED)[i], 8)
        ctx.restore()
        text(ctx, str(r), x + 90, 1330 - h - 60, 84, FONT, INK)
        text(ctx, f'SERIE {i + 1}', x + 90, 1385, 32, FONT, INK)
    poly(ctx, [(150, 1332), (930, 1332)], 7)

def s4(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    td = wt.get('DUE', 1.0); ts = wt.get('STESSO', L * .6); tm = wt.get('MEGLIO', L - .5)
    floor(ctx, G)
    A = lifter(ctx, tau, 330, .15, freq=1.2, s=1.05)
    k = eback(prog(tau, td - .2, td + .1))
    plate_label(ctx, (330, 700), 'STOP: −2 REP', k, bg=RED, tc=WHITE, size=50, rot=-.04)
    for i, (lab, t0, val, cc) in enumerate((('STIMOLO', ts, .9, RED), ('RECUPERO', tm, .95, GREEN))):
        kk = prog(tau, t0 - .25, t0 + .35)
        if kk <= 0: continue
        y = 900 + i * 230
        plate_label(ctx, (790, y - 70), lab, eback(clamp(kk * 2)), bg=INK, tc=WHITE, size=36)
        rrect(ctx, 610, y - 20, 360, 60, 30); fill_stroke(ctx, WHITE, 7)
        rrect(ctx, 618, y - 12, 344 * val * eout(kk), 44, 22); col(ctx, cc); ctx.fill()
        if kk >= 1: check(ctx, (1000, y - 70), .6)

def s5(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    tu = wt.get("L'ULTIMA", 1.2); ti = wt.get('ISOLAMENTO', L - .7)
    rows = (('SERIE 1', '2 in riserva'), ('SERIE 2', '2 in riserva'), ('SERIE 3', 'CEDIMENTO'))
    for i, (a, b) in enumerate(rows):
        k = eback(prog(tau, .1 + i * .18, .35 + i * .18)); last = i == 2
        if k <= 0: continue
        hl = last and tau > tu - .1
        y = 640 + i * 140
        ctx.save(); ctx.translate(540, y); sscale(ctx, k * (1 + .05 * math.sin(tau * 9) * hl))
        rrect(ctx, -400 + 8, -65 + 10, 800, 130, 30); col(ctx, INK, .15); ctx.fill()
        rrect(ctx, -400, -65, 800, 130, 30); fill_stroke(ctx, RED if hl else WHITE, 8)
        text(ctx, a, -360, 2, 46, FONT, WHITE if hl else INK, anchor='l')
        text(ctx, b, 360, 2, 40, FONT, WHITE if hl else GRAY, anchor='r')
        ctx.restore()
    floor(ctx, G)
    lifter(ctx, tau, 300, 1.0 if tau > tu else .2, s=.7)
    plate_label(ctx, (760, 1260), 'ISOLAMENTO', eback(prog(tau, ti - .15, ti + .15)), bg=BLUE, tc=WHITE, size=46, rot=.04)
    if tau > ti: check(ctx, (980, 1190), .7 * eback(prog(tau, ti, ti + .25)))

def effort_screen(sel, press):
    """Schermata reale di iki, lato cliente: a fine esercizio 'Com'è andata?' con Facile / Giusto / Duro / Al limite."""
    def content(ctx, w, h):
        app_head(ctx, w, 'Allenamento')
        text(ctx, 'Curl con manubri', 40, 215, 40, FONT, INK, anchor='l')
        text(ctx, '3 × 10 · 12 kg', 40, 268, 30, FONTB, GRAY, anchor='l')
        for i in range(3):
            y = 320 + i * 86
            rrect(ctx, 40, y, w - 80, 70, 16); col(ctx, (.95, .94, .92)); ctx.fill()
            text(ctx, f'Serie {i + 1}', 64, y + 36, 28, FONTB, INK, anchor='l')
            text(ctx, '12 kg × 10', w - 130, y + 36, 28, FONTB, INK, anchor='r')
            ctx.arc(w - 82, y + 35, 19, 0, 2 * math.pi); col(ctx, GREEN); ctx.fill(); check(ctx, (w - 82, y + 35), .28, WHITE)
        text(ctx, "Com'è andata?", 40, 640, 38, FONT, INK, anchor='l')
        labs = ('Facile', 'Giusto', 'Duro', 'Al limite'); bw = (w - 80 - 3 * 12) / 4
        for i, lab in enumerate(labs):
            x = 40 + i * (bw + 12); on = i == sel
            z = 1 + .12 * press * on
            ctx.save(); ctx.translate(x + bw / 2, 730); ctx.scale(z, z)
            rrect(ctx, -bw / 2, -46, bw, 92, 16)
            if on: col(ctx, RED); ctx.fill()
            else: fill_stroke(ctx, (.97, .96, .94), 3, (.8, .78, .75))
            text(ctx, lab, 0, 1, 25, FONT, WHITE if on else INK)
            ctx.restore()
        text(ctx, 'Una nota per il tuo PT', 40, 850, 26, FONTB, GRAY, anchor='l')
    return content

def s6(ctx, tau, L, wt):
    up = eout(prog(tau, 0, .35))
    halo(ctx, (540, 1100), 760, RED, .12)
    ts = [wt.get(k, L) for k in ('FACILE', 'GIUSTO', 'DURO', 'LIMITE')]
    sel = -1; press = 0.0
    for i, t0 in enumerate(ts):
        if tau >= t0 - .05: sel = i; press = 1 - eout(prog(tau, t0 - .05, t0 + .25))
    phone(ctx, 540, lerp(2600, 1130, up), 640, 1120, effort_screen(sel, press))
    status_chip(ctx, 540, 500, "Lo vedi tu, per ogni esercizio", RED, prog(tau, ts[0] - .9, ts[0] - .6), 34)

def s7(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    tc = wt.get('SFORZO', .4)
    floor(ctx, G)
    fig(ctx, 'pt', lambda t: P(t=3, ra1=150 + 16 * math.sin(t * 9), ra2=172 + 20 * math.sin(t * 9 + .6), la1=-16, la2=-8),
        dict(eyes='happy', mouth='grin', brows='raised'), 330, tau, fx=.2, seed=1, U_=U * .95)
    lifter(ctx, tau, 760, .15, s=.9, seed=3)
    cta_card(ctx, CTA, prog(tau, tc - .3, tc + .1), 660, tau)

SCENES = dict(s1=s1, s2=s2, s3=s3, s4=s4, s5=s5, s6=s6, s7=s7)

def SFX(fx, at):
    for i in range(3): fx('thud', at('s1', None, .15 + i * .5), .3)
    fx('buzz', at('s2', 'SBAGLIATO', -.05), .3); fx('thud', at('s2', 'SBAGLIATO', .0), .5)
    fx('swoosh_down', at('s3', 'STANCA', -.1), .3); fx('sad', at('s3', 'CROLLANO', -.2), .16)
    for i in range(3): fx('pop', at('s3', 'CROLLANO', -.45 + i * .22), .25, f=1100 - i * 200)
    fx('ding', at('s4', 'DUE', -.1), .25); fx('swoosh_up', at('s4', 'STESSO', -.3), .25); fx('chime', at('s4', 'MEGLIO', -.1), .22)
    for i in range(3): fx('pop', at('s5', None, .12 + i * .18), .22, f=900 + i * 100)
    fx('thud', at('s5', "L'ULTIMA", -.05), .4); fx('ding', at('s5', 'ISOLAMENTO', 0), .22, f=1500)
    fx('whoosh', at('s6', None), .35)
    for i, w in enumerate(('FACILE', 'GIUSTO', 'DURO', 'LIMITE')): fx('msg', at('s6', w, -.05), .3, f=700 + i * 120)
    fx('pop', at('s7', 'SFORZO', -.2), .35, f=800); fx('chime', at('s7', 'SFORZO', .1), .2)

if __name__ == '__main__':
    main(sys.modules[__name__], '29')
