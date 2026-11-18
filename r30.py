from props4 import *

TITLE = 'Massimale a una ripetizione'
HOOK = "TESTI IL\nMASSIMALE?"
LOOP = True; TAIL = 1.4
CTA = 'MASSIMALE'
SENT = [
    ("Testi il massimale con una ripetizione secca?", 's1', {'MASSIMALE', 'SECCA'}, 0.1),
    ("Quasi mai serve.", 's2', {'MAI'}, 0.1),
    ("È rischioso, stanca tanto, e con chi è alle prime armi spesso non è affidabile.", 's3', {'RISCHIOSO', 'STANCA', 'AFFIDABILE'}, 0.1),
    ("Usa un carico da tre a cinque ripetizioni pulite, e da lì stimi il massimale.", 's4', {'CINQUE', 'PULITE', 'STIMI'}, 0.1),
    ("Poi lavora in percentuale, e aggiornalo a ogni nuovo ciclo.", 's5', {'PERCENTUALE', 'CICLO'}, 0.1),
    ("In iki salvi il massimale del cliente, scrivi settantacinque per cento nella scheda, e lui vede già i chili.", 's6', {'MASSIMALE', 'SCHEDA', 'CHILI'}, 0.1),
    ("Scrivi «massimale» nei commenti, e ti mando come funziona.", 's7', {'MASSIMALE'}, 0.0),
]

def squatter(ctx, tau, x, strain, freq=.45, s=1.0, seed=2, plates=1.0):
    """Cliente che fa squat col bilanciere; strain 0..1 = quanto è al limite."""
    face = dict(eyes='wince' if strain > .6 else 'open', mouth='shout' if strain > .6 else ('flat' if strain > .25 else 'smile'),
                brows='angry' if strain > .6 else 'neutral', look=(0, -.2))
    depth = 1.0 if strain < .6 else .55 + .1 * math.sin(tau * 3)
    sh = math.sin(tau * 40) * 6 * strain
    pose = squat_bar(freq * (1 - .5 * strain), depth)
    A = fig(ctx, 'client', pose, face, x + sh, tau, fx=.1, seed=seed, U_=U * s)
    draw_bar_on(ctx, A, x, tau, plates=plates, s=1.05 * s, shake=sh)
    if strain > .5:
        for i in range(3):
            k = (tau * 1.3 + i * .33) % 1
            drop(ctx, A['head'][0] - 95 * s + i * 95 * s, A['head'][1] - 60 + k * 120, .9 * s, (1 - k) * strain)
    return A

def s1(ctx, tau, L, wt):
    cam(ctx, 1.04, 540, 1040)
    floor(ctx, G)
    halo(ctx, (540, 1150), 520, RED, .10 + .05 * math.sin(tau * 9))
    squatter(ctx, tau, 540, 1.0, s=1.15, plates=1.6)
    plate_label(ctx, (250, 700), '1 REP', 1 + .08 * math.sin(tau * 12), bg=INK, tc=WHITE, size=56, rot=-.06)
    plate_label(ctx, (830, 660), 'MAX!', eback(prog(tau, .35, .6)), bg=RED, tc=WHITE, size=56, rot=.07)

def s2(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    floor(ctx, G)
    ts = wt.get('MAI', .3)
    no = math.sin(tau * 14) * 9
    fig(ctx, 'pt', lambda t: P(t=0, h=no, la1=-60, la2=60, ra1=60, ra2=-60), dict(eyes='open', mouth='flat', brows='angry', look=(0, 0)), 540, tau, seed=1, U_=U * .95)
    stamp_x(ctx, (540, 690), prog(tau, ts - .1, ts + .15), 1.5)

def s3(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    ts = [wt.get('RISCHIOSO', .3), wt.get('STANCA', 1.2), wt.get('AFFIDABILE', L - .7)]
    rows = ('RISCHIOSO', 'STANCA TANTO', 'POCO AFFIDABILE')
    for i, a in enumerate(rows):
        k = eback(prog(tau, ts[i] - .2, ts[i] + .1))
        if k <= 0: continue
        y = 630 + i * 140
        ctx.save(); ctx.translate(540, y); sscale(ctx, k); ctx.rotate((-.02, .015, -.01)[i])
        rrect(ctx, -400 + 8, -60 + 10, 800, 120, 30); col(ctx, INK, .15); ctx.fill()
        rrect(ctx, -400, -60, 800, 120, 30); fill_stroke(ctx, WHITE, 8)
        text(ctx, a, -350, 2, 48, FONT, INK, anchor='l')
        xmark(ctx, (330, 0), .55)
        ctx.restore()
    floor(ctx, G)
    lv = lerp(1.0, .1, eio(prog(tau, ts[1] - .2, ts[1] + .8)))
    squatter(ctx, tau, 330, .9, s=.72, plates=1.4)
    battery(ctx, (810, 1260), lv, 1.0)

def s4(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    tc = wt.get('CINQUE', .8); tp = wt.get('PULITE', 1.6); te = wt.get('STIMI', L - .8)
    floor(ctx, G)
    squatter(ctx, tau, 260, .1, freq=.8, s=.9, plates=1.2)
    n = 1 + min(4, int(max(0, tau - tc + .3) * 1.6))
    plate_label(ctx, (260, 640), f'REP {n}', eback(prog(tau, tc - .3, tc)), bg=INK, tc=WHITE, size=52, rot=-.04)
    if tau > tp: check(ctx, (430, 600), .8 * eback(prog(tau, tp, tp + .25)))
    # card di stima
    k = eback(prog(tau, tc - .1, tc + .25))
    if k > 0:
        ctx.save(); ctx.translate(830, 900); sscale(ctx, k); ctx.rotate(.03)
        rrect(ctx, -195 + 8, -170 + 10, 390, 340, 34); col(ctx, INK, .15); ctx.fill()
        rrect(ctx, -195, -170, 390, 340, 34); fill_stroke(ctx, WHITE, 8)
        text(ctx, '97,5 kg × 5', 0, -105, 44, FONT, INK)
        a = prog(tau, te - .3, te + .1)
        poly(ctx, [(0, -60), (0, -60 + 70 * a)], 8, RED)
        if a > .9:
            text(ctx, 'STIMA', 0, 45, 32, FONTB, GRAY)
            text(ctx, '≈ 110 kg', 0, 110, 66, FONT, RED, stroke=INK, sw=3)
        ctx.restore()

def s5(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    tp = wt.get('PERCENTUALE', .7); tc = wt.get('CICLO', L - .6)
    bars = (('70%', '77'), ('75%', '82,5'), ('80%', '88'))
    for i, (p, kg) in enumerate(bars):
        k = eback(prog(tau, tp - .3 + i * .2, tp + .0 + i * .2))
        if k <= 0: continue
        h = 280 + i * 70; x = 140 + i * 240
        ctx.save(); ctx.translate(x + 90, 1330); ctx.scale(1, max(k, .02)); ctx.translate(-(x + 90), -1330)
        rrect(ctx, x + 8, 1330 - h + 10, 180, h, 18); col(ctx, INK, .15); ctx.fill()
        rrect(ctx, x, 1330 - h, 180, h, 18); fill_stroke(ctx, (YELLOW, ORANGE, RED)[i], 8)
        ctx.restore()
        text(ctx, p, x + 90, 1330 - h - 60, 64, FONT, INK)
        text(ctx, kg + ' kg', x + 90, 1380, 34, FONT, INK)
    poly(ctx, [(110, 1332), (870, 1332)], 7)
    kc = eback(prog(tau, tc - .3, tc + .05))
    if kc > 0:
        ctx.save(); ctx.translate(850, 680); sscale(ctx, kc); ctx.rotate(.05 + .02 * math.sin(tau * 4))
        rrect(ctx, -150, -95, 300, 190, 30); fill_stroke(ctx, BLUE, 8)
        text(ctx, 'NUOVO CICLO', 0, -38, 30, FONT, WHITE)
        text(ctx, '110 → 115', 0, 30, 44, FONT, WHITE)
        ctx.restore()
    plate_label(ctx, (360, 640), 'MASSIMALE 110 kg', eback(prog(tau, .05, .35)), bg=INK, tc=WHITE, size=40, rot=-.03)

CHIP_BG = (.95, .94, .92)
def maxes_screen(typed, hl):
    """Schermata reale di iki, lato PT: pagina cliente, sezione Massimali (Esercizio / Massimale)."""
    def content(ctx, w, h):
        app_head(ctx, w, 'Marco')
        text(ctx, 'Massimali', 40, 220, 44, FONT, INK, anchor='l')
        text(ctx, 'Il massimale (1 ripetizione) per esercizio.', 40, 280, 24, FONTB, GRAY, anchor='l')
        text(ctx, 'ESERCIZIO', 40, 360, 22, FONT, GRAY, anchor='l'); text(ctx, 'MASSIMALE', w - 40, 360, 22, FONT, GRAY, anchor='r')
        rows = (('Squat bilanciere', '110' [:max(0, int(typed * 3 + .001))] if typed < 1 else '110', True),
                ('Panca piana', '80', False), ('Stacco da terra', '130', False))
        for i, (n, v, pc) in enumerate(rows):
            y = 400 + i * 130
            on = i == 0 and hl > 0
            rrect(ctx, 30, y, w - 60, 112, 18); col(ctx, LIGHT_RED if on else CHIP_BG); ctx.fill()
            text(ctx, n, 54, y + 44, 30, FONT, INK, anchor='l')
            if pc: text(ctx, 'in % nella scheda', 54, y + 84, 22, FONT, RED, anchor='l')
            rrect(ctx, w - 210, y + 24, 170, 64, 14); fill_stroke(ctx, WHITE, 3, RED if on else (.8, .78, .75))
            text(ctx, v or '—', w - 60, y + 57, 32, FONT, INK, anchor='r')
    return content

def client_load_screen(hl):
    """Schermata reale di iki, lato cliente: chip Obiettivo / Carico '75% · 82,5 kg', serie con i kg già scritti."""
    def content(ctx, w, h):
        app_head(ctx, w, 'Allenamento')
        text(ctx, 'Squat bilanciere', 40, 215, 42, FONT, INK, anchor='l')
        cw = (w - 80 - 16) / 3
        chips = (('OBIETTIVO', '4×5', 1), ('CARICO', '75% · 82,5 kg', 2))
        x = 40
        for lab, v, span in chips:
            ww = cw * span + 16 * (span - 1); on = lab == 'CARICO' and hl > 0
            z = 1 + .08 * hl * on
            ctx.save(); ctx.translate(x + ww / 2, 330); ctx.scale(z, z)
            rrect(ctx, -ww / 2, -62, ww, 124, 18)
            if on: fill_stroke(ctx, LIGHT_RED, 4, RED)
            else: col(ctx, CHIP_BG); ctx.fill()
            text(ctx, lab, -ww / 2 + 22, -24, 20, FONT, GRAY, anchor='l')
            text(ctx, v, -ww / 2 + 22, 24, 36, FONT, RED if on else INK, anchor='l')
            ctx.restore(); x += ww + 16
        for i in range(4):
            y = 440 + i * 100
            rrect(ctx, 40, y, w - 80, 82, 16); col(ctx, CHIP_BG); ctx.fill()
            text(ctx, f'Serie {i + 1}', 64, y + 42, 28, FONTB, INK, anchor='l')
            text(ctx, '82,5 kg', w - 250, y + 42, 28, FONTB, GRAY, anchor='r')
            text(ctx, '5', w - 140, y + 42, 28, FONTB, GRAY, anchor='r')
            ctx.arc(w - 82, y + 41, 21, 0, 2 * math.pi); fill_stroke(ctx, WHITE, 3, (.8, .78, .75))
    return content

def s6(ctx, tau, L, wt):
    up = eout(prog(tau, 0, .35))
    halo(ctx, (540, 1100), 760, RED, .12)
    tm = wt.get('MASSIMALE', .8); ts = wt.get('SCHEDA', L * .55); tk = wt.get('CHILI', L - .5)
    if tau < ts - .2:
        scr = maxes_screen(prog(tau, tm - .2, tm + .3), prog(tau, tm - .2, tm))
        chip = ("Lato PT: i massimali di Marco", INK, prog(tau, .3, .6))
    else:
        hl = prog(tau, tk - .15, tk + .2)
        scr = client_load_screen(hl)
        chip = ("Lato cliente: i kg sono già calcolati", RED, prog(tau, tk - .2, tk + .1))
    sw = 1 - abs(2 * prog(tau, ts - .4, ts) - 1) if ts - .4 < tau < ts else 1
    phone(ctx, 540, lerp(2600, 1130, up), 640 * max(.05, sw), 1120, scr)
    status_chip(ctx, 540, 500, chip[0], chip[1], chip[2], 34)

def s7(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    tc = wt.get('MASSIMALE', .4)
    floor(ctx, G)
    fig(ctx, 'pt', lambda t: P(t=3, ra1=150 + 16 * math.sin(t * 9), ra2=172 + 20 * math.sin(t * 9 + .6), la1=-16, la2=-8),
        dict(eyes='happy', mouth='grin', brows='raised'), 300, tau, fx=.2, seed=1, U_=U * .95)
    squatter(ctx, tau, 770, .1, freq=.7, s=.85, seed=3, plates=1.0)
    cta_card(ctx, CTA, prog(tau, tc - .3, tc + .1), 660, tau)

SCENES = dict(s1=s1, s2=s2, s3=s3, s4=s4, s5=s5, s6=s6, s7=s7)

def SFX(fx, at):
    for i in range(3): fx('thud', at('s1', None, .15 + i * .55), .3)
    fx('buzz', at('s2', 'MAI', -.1), .3); fx('thud', at('s2', 'MAI', .0), .5)
    for w in ('RISCHIOSO', 'STANCA', 'AFFIDABILE'): fx('pop', at('s3', w, -.15), .25, f=900)
    fx('sad', at('s3', 'AFFIDABILE', .1), .14)
    fx('ding', at('s4', 'CINQUE', -.1), .25); fx('chime', at('s4', 'PULITE', 0), .2); fx('swoosh_down', at('s4', 'STIMI', -.2), .25)
    for i in range(3): fx('pop', at('s5', 'PERCENTUALE', -.25 + i * .2), .22, f=800 + i * 150)
    fx('ding', at('s5', 'CICLO', -.1), .22, f=1500)
    fx('whoosh', at('s6', None), .35); fx('msg', at('s6', 'MASSIMALE', 0), .3, f=800)
    fx('swoosh_up', at('s6', 'SCHEDA', -.35), .25); fx('chime', at('s6', 'CHILI', -.05), .22)
    fx('pop', at('s7', 'MASSIMALE', -.2), .35, f=800); fx('chime', at('s7', 'MASSIMALE', .1), .2)

if __name__ == '__main__':
    main(sys.modules[__name__], '30')
