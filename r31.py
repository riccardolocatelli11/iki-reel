from props4 import *

TITLE = 'Riscaldamento sul tapis roulant'
HOOK = "BASTA IL\nTAPIS ROULANT?"
LOOP = True; TAIL = 1.4
CTA = 'RISCALDAMENTO'
SENT = [
    ("Per scaldarsi basta il tapis roulant?", 's1', {'SCALDARSI', 'TAPIS', 'ROULANT'}, 0.1),
    ("Quasi mai.", 's2', {'MAI'}, 0.1),
    ("Ti alza la temperatura, ma non prepara i movimenti che farai dopo.", 's3', {'TEMPERATURA', 'MOVIMENTI'}, 0.1),
    ("Di solito bastano cinque minuti leggeri, poi mobilità sulle articolazioni del giorno.", 's4', {'CINQUE', 'MOBILITÀ', 'ARTICOLAZIONI'}, 0.1),
    ("E prima del primo esercizio, due o tre serie di avvicinamento, con il carico che sale.", 's5', {'AVVICINAMENTO', 'SALE'}, 0.1),
    ("In iki scrivi il riscaldamento nella scheda, e il cliente lo trova in rosso, prima degli esercizi.", 's6', {'RISCALDAMENTO', 'SCHEDA', 'ROSSO'}, 0.1),
    ("Scrivi «riscaldamento» nei commenti, e ti mando come funziona.", 's7', {'RISCALDAMENTO'}, 0.0),
]

CHIP_BG = (.95, .94, .92)

def treadmill(ctx, x, g, t, s=1.0, speed=1.0):
    """Tapis roulant di lato (console a destra). Ritorna l'altezza del nastro."""
    ctx.save(); ctx.translate(x, g); sscale(ctx, s)
    # montante e console
    poly(ctx, [(250, -50), (300, -470)], 16)
    ctx.save(); ctx.translate(300, -490); ctx.rotate(-.35)
    rrect(ctx, -90, -40, 180, 80, 18); fill_stroke(ctx, DARK, 7)
    text(ctx, f"{int(t * 1.2) % 60 + 1:02d}:{int(t * 37) % 60:02d}", 0, 2, 34, FONT, (.5, .95, .6))
    ctx.restore()
    poly(ctx, [(300, -470), (120, -430)], 12)          # maniglia
    # pedana
    rrect(ctx, -330 + 6, -58 + 8, 660, 58, 26); col(ctx, INK, .15); ctx.fill()
    rrect(ctx, -330, -58, 660, 58, 26); fill_stroke(ctx, WHITE, 8)
    ctx.save(); rrect(ctx, -318, -50, 636, 18, 9); ctx.clip()
    col(ctx, INK); ctx.rectangle(-318, -50, 636, 18); ctx.fill()
    off = (t * 260 * speed) % 60
    for i in range(13):
        xx = 318 - i * 60 - off
        poly(ctx, [(xx, -46), (xx - 22, -36)], 4, WHITE, .6)
    ctx.restore()
    for wx in (-300, 300):
        ctx.arc(wx, -20, 14, 0, 2 * math.pi); fill_stroke(ctx, GRAY, 5)
    poly(ctx, [(-280, 0), (-240, 0)], 10); poly(ctx, [(240, 0), (280, 0)], 10)
    ctx.restore()
    return g - 50 * s

def thermometer(ctx, c, level, s=1.0, t=0.0):
    ctx.save(); ctx.translate(*c); sscale(ctx, s)
    rrect(ctx, -46 + 8, -330 + 10, 92, 380, 46); col(ctx, INK, .15); ctx.fill()
    ctx.arc(8, 90 + 10, 80, 0, 2 * math.pi); col(ctx, INK, .15); ctx.fill()
    rrect(ctx, -46, -330, 92, 380, 46); fill_stroke(ctx, WHITE, 8)
    ctx.arc(0, 90, 80, 0, 2 * math.pi); fill_stroke(ctx, RED, 8)
    h = 330 * clamp(level) + 6 * math.sin(t * 7)
    rrect(ctx, -22, 40 - h, 44, h + 30, 22); col(ctx, RED); ctx.fill()
    ctx.arc(0, 90, 64, 0, 2 * math.pi); col(ctx, RED); ctx.fill()
    for i in range(5):
        y = -260 + i * 62
        poly(ctx, [(46, y), (78, y)], 6)
    ctx.restore()

def runner(ctx, tau, x, g, s=.8, face=None, fast=1.0):
    return fig(ctx, 'client', lambda t: walk(t * 2 * math.pi * 1.6 * fast, 1, 0, 1.1), face or dict(eyes='open', mouth='smile', look=(1, 0)),
               x, tau, fx=.6, seed=2, U_=U * s, g=g)

def s1(ctx, tau, L, wt):
    cam(ctx, 1.04, 540, 1040)
    floor(ctx, G)
    halo(ctx, (540, 1150), 520, RED, .10 + .05 * math.sin(tau * 9))
    gb = treadmill(ctx, 500, G, tau, 1.0)
    runner(ctx, tau, 470, gb, s=1.0, face=dict(eyes='open', mouth='grin', brows='raised', look=(1, 0)))
    plate_label(ctx, (250, 680), '10 MIN', 1 + .08 * math.sin(tau * 12), bg=INK, tc=WHITE, size=56, rot=-.06)
    plate_label(ctx, (820, 640), 'PRONTO?', eback(prog(tau, .35, .6)), bg=RED, tc=WHITE, size=52, rot=.07)

def s2(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    floor(ctx, G)
    ts = wt.get('MAI', .3)
    no = math.sin(tau * 14) * 9
    fig(ctx, 'pt', lambda t: P(t=0, h=no, la1=-60, la2=60, ra1=60, ra2=-60), dict(eyes='open', mouth='flat', brows='angry', look=(0, 0)), 540, tau, seed=1, U_=U * .95)
    stamp_x(ctx, (540, 690), prog(tau, ts - .1, ts + .15), 1.5)

def s3(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    tt = wt.get('TEMPERATURA', .5); tm = wt.get('MOVIMENTI', L * .6)
    lv = lerp(.15, .92, eio(prog(tau, tt - .3, tt + .8)))
    thermometer(ctx, (230, 1050), lv, 1.05, tau)
    if tau > tt + .5: check(ctx, (230, 640), .9 * eback(prog(tau, tt + .5, tt + .75)))
    rows = ('SQUAT', 'PANCA', 'STACCO')
    for i, a in enumerate(rows):
        k = eback(prog(tau, tm - .45 + i * .2, tm - .2 + i * .2))
        if k <= 0: continue
        y = 700 + i * 200
        ctx.save(); ctx.translate(700, y); sscale(ctx, k); ctx.rotate((-.02, .015, -.01)[i])
        rrect(ctx, -250 + 8, -70 + 10, 500, 140, 30); col(ctx, INK, .15); ctx.fill()
        rrect(ctx, -250, -70, 500, 140, 30); fill_stroke(ctx, WHITE, 8)
        text(ctx, a, -210, 2, 52, FONT, INK, anchor='l')
        if tau > tm + .2 + i * .15:
            xmark(ctx, (180, 0), .6 * eback(prog(tau, tm + .2 + i * .15, tm + .4 + i * .15)))
        ctx.restore()
    plate_label(ctx, (700, 1380), 'NON PRONTI', eback(prog(tau, tm + .6, tm + .9)), bg=RED, tc=WHITE, size=46, rot=.03)

def s4(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    tc = wt.get('CINQUE', .6); tm = wt.get('MOBILITÀ', L * .55); ta = wt.get('ARTICOLAZIONI', L - .8)
    floor(ctx, G)
    bike(ctx, 300, G, tau, s=.95)
    plate_label(ctx, (300, 720), "5' LEGGERI", eback(prog(tau, tc - .2, tc + .1)), bg=INK, tc=WHITE, size=50, rot=-.04)
    km = prog(tau, tm - .3, tm)
    if km > 0:
        ph = max(0, tau - tm + .3)
        a = ph * 2 * math.pi * .9
        A = fig(ctx, 'pt', lambda t: P(t=0, h=0, la1=-90 - 70 * math.cos(a), la2=-90 - 70 * math.cos(a),
                                      ra1=90 + 70 * math.cos(a), ra2=90 + 70 * math.cos(a), ll1=-10, rl1=10),
                dict(eyes='happy', mouth='smile', brows='raised'), 800, tau, seed=1, U_=U * .85 * eback(km))
        if tau > ta - .2:
            ka = eback(prog(tau, ta - .2, ta + .1))
            for jt, sx in (('shL', -1), ('shR', 1), ('hpL', -1), ('hpR', 1)):
                c = A[jt] + np.array([sx * 95, 0])
                ctx.save(); ctx.translate(*c); ctx.rotate(sx * tau * 4)
                ctx.arc(0, 0, 38 * ka, 0, 1.4 * math.pi); col(ctx, RED); ctx.set_line_width(8); ctx.stroke()
                ctx.restore()
        plate_label(ctx, (800, 690), 'MOBILITÀ', eback(prog(tau, tm - .15, tm + .15)), bg=RED, tc=WHITE, size=50, rot=.04)

def s5(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    ta = wt.get('AVVICINAMENTO', 1.2); tsl = wt.get('CARICO', L - 1.0); td = wt.get('DUE', ta - 1.5)
    kp = eback(prog(tau, .05, .35)) * (1 - eio(prog(tau, td - .35, td - .05)))
    if kp > 0.01:
        ctx.save(); ctx.translate(540, 960); sscale(ctx, kp * 1.4); ctx.rotate(-.04 + .03 * math.sin(tau * 5))
        barbell(ctx, (0, 0), 420); ctx.restore()
        plate_label(ctx, (540, 760), "PRIMO ESERCIZIO", kp, bg=WHITE, tc=INK, size=42, rot=.03)
    bars = (('40', '×8', GRAY), ('60', '×5', YELLOW), ('75', '×3', ORANGE), ('85', '×5', RED))
    for i, (kg, rp, cc) in enumerate(bars):
        t0 = td - .2 + i * (ta - td) / 2.5 if i < 3 else tsl - .15
        k = eback(prog(tau, t0, t0 + .3))
        if k <= 0: continue
        h = 180 + i * 110; x = 105 + i * 225
        ctx.save(); ctx.translate(x + 90, 1330); ctx.scale(1, max(k, .02)); ctx.translate(-(x + 90), -1330)
        rrect(ctx, x + 8, 1330 - h + 10, 180, h, 18); col(ctx, INK, .15); ctx.fill()
        rrect(ctx, x, 1330 - h, 180, h, 18); fill_stroke(ctx, cc, 8)
        ctx.restore()
        text(ctx, kg, x + 90, 1330 - h - 55, 64, FONT, INK)
        text(ctx, rp, x + 90, 1385, 40, FONT, INK)
    poly(ctx, [(80, 1332), (1000, 1332)], 7)
    k1 = eback(prog(tau, ta - .3, ta))
    plate_label(ctx, (400, 650), 'AVVICINAMENTO', k1, bg=INK, tc=WHITE, size=44, rot=-.03)
    ka = prog(tau, ta - .2, tsl)
    if ka > 0:
        pts = curve_pts((300, 1040), (740, 800), .25)
        dashed_path(ctx, pts, ka, 8, RED, arrow=True)
    plate_label(ctx, (850, 620), 'LAVORO', eback(prog(tau, tsl, tsl + .25)), bg=RED, tc=WHITE, size=44, rot=.05)

WARM = ("5' bike leggera", "Mobilità spalle e anche", "Squat: 3 serie di avvicinamento")

def editor_warm_screen(open_, typed, hl):
    """Schermata reale di iki, lato PT: editor scheda, testata con i chip (settimane, da..., Riscaldamento) e il campo del riscaldamento."""
    def content(ctx, w, h):
        app_head(ctx, w, 'Scheda')
        rrect(ctx, 30, 190, w - 60, 560 if open_ > 0 else 260, 24); fill_stroke(ctx, WHITE, 3, (.85, .83, .8))
        text(ctx, 'Marco', 60, 245, 34, FONT, INK, anchor='l')
        text(ctx, 'Forza A/B', 60, 300, 30, FONTB, GRAY, anchor='l')
        chips = ('4 settimane', 'da lun 23/11', 'Riscaldamento ✓' if typed >= 1 else '+ Riscaldamento')
        x = 60
        for i, c in enumerate(chips):
            ctx.select_font_face(FONTB); ctx.set_font_size(24); cw = ctx.text_extents(c).width + 44
            if x + cw > w - 50: x = 60; yrow = 1
            y = 340 if i < 2 else 410
            if i == 2: x = 60
            on = i == 2
            z = 1 + .1 * hl * on
            ctx.save(); ctx.translate(x + cw / 2, y + 30); ctx.scale(z, z)
            rrect(ctx, -cw / 2, -30, cw, 60, 30)
            fill_stroke(ctx, LIGHT_RED if (on and open_ > 0) else CHIP_BG, 3, (.82, .8, .77))
            text(ctx, c, 0, 1, 24, FONTB, RED if (on and typed < 1) else INK)
            ctx.restore()
            x += cw + 14
        if open_ > 0:
            rrect(ctx, 60, 500, w - 120, 220, 16); fill_stroke(ctx, WHITE, 3, RED)
            full = '\n'.join(WARM); n = int(len(full) * clamp(typed))
            for j, ln in enumerate(full[:n].split('\n')):
                text(ctx, ln, 84, 550 + j * 56, 25, FONTB, INK, anchor='l')
        y0 = 790 if open_ > 0 else 490
        text(ctx, 'Giorno 1', 40, y0, 34, FONT, INK, anchor='l')
        for i, n_ in enumerate(('Squat bilanciere', 'Panca piana')):
            yy = y0 + 40 + i * 100
            rrect(ctx, 30, yy, w - 60, 84, 16); col(ctx, CHIP_BG); ctx.fill()
            text(ctx, n_, 54, yy + 43, 28, FONTB, INK, anchor='l')
    return content

def client_warm_screen(hl):
    """Schermata reale di iki, lato cliente: 'Giorno 1', 'Avvia cronometro allenamento', sezione Riscaldamento in rosso, poi gli esercizi."""
    def content(ctx, w, h):
        app_head(ctx, w, 'Allenamento')
        text(ctx, 'Giorno 1', 40, 220, 46, FONT, INK, anchor='l')
        ctx.set_dash([12, 8]); rrect(ctx, 40, 270, w - 80, 76, 16); col(ctx, RED); ctx.set_line_width(3); ctx.stroke(); ctx.set_dash([])
        text(ctx, 'Avvia cronometro allenamento', w / 2, 309, 24, FONTB, RED)
        z = 1 + .05 * hl
        ctx.save(); ctx.translate(w / 2, 520); ctx.scale(z, z); ctx.translate(-w / 2, -520)
        rrect(ctx, 40, 372, w - 80, 296, 16); col(ctx, CHIP_BG); ctx.fill()
        ctx.rectangle(40, 380, 7, 280); col(ctx, RED); ctx.fill()
        text(ctx, 'RISCALDAMENTO', 72, 418, 24, FONT, RED, anchor='l')
        poly(ctx, [(w - 92, 424), (w - 78, 410), (w - 64, 424)], 4, RED)
        for j, ln in enumerate(WARM):
            text(ctx, ln, 72, 478 + j * 58, 26, FONTB, INK, anchor='l')
        ctx.restore()
        for i, n_ in enumerate(('Squat bilanciere', 'Panca piana', 'Rematore')):
            yy = 700 + i * 100
            rrect(ctx, 40, yy, w - 80, 84, 16); col(ctx, CHIP_BG); ctx.fill()
            text(ctx, n_, 64, yy + 43, 28, FONTB, INK, anchor='l')
    return content

def s6(ctx, tau, L, wt):
    up = eout(prog(tau, 0, .35))
    halo(ctx, (540, 1100), 760, RED, .12)
    tr = wt.get('RISCALDAMENTO', .8); ts = wt.get('SCHEDA', L * .4); tro = wt.get('ROSSO', L - .9)
    sw_t = ts + .5
    if tau < sw_t:
        scr = editor_warm_screen(prog(tau, tr - .1, tr + .1), prog(tau, tr + .1, sw_t - .3), prog(tau, tr - .3, tr))
        chip = ("Lato PT: lo scrivi nella scheda", INK, prog(tau, .3, .6))
    else:
        scr = client_warm_screen(math.sin(prog(tau, tro - .1, tro + .4) * math.pi))
        chip = ("Lato cliente: prima degli esercizi", RED, prog(tau, sw_t + .2, sw_t + .5))
    sw = 1 - abs(2 * prog(tau, sw_t - .4, sw_t) - 1) if sw_t - .4 < tau < sw_t else 1
    phone(ctx, 540, lerp(2600, 1130, up), 640 * max(.05, sw), 1120, scr)
    status_chip(ctx, 540, 500, chip[0], chip[1], chip[2], 34)

def s7(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    tc = wt.get('RISCALDAMENTO', .4)
    floor(ctx, G)
    fig(ctx, 'pt', lambda t: P(t=3, ra1=150 + 16 * math.sin(t * 9), ra2=172 + 20 * math.sin(t * 9 + .6), la1=-16, la2=-8),
        dict(eyes='happy', mouth='grin', brows='raised'), 260, tau, fx=.2, seed=1, U_=U * .95)
    gb = treadmill(ctx, 760, G, tau, .62, .8)
    runner(ctx, tau, 740, gb, s=.62)
    cta_card(ctx, CTA, prog(tau, tc - .3, tc + .1), 660, tau)

SCENES = dict(s1=s1, s2=s2, s3=s3, s4=s4, s5=s5, s6=s6, s7=s7)

def SFX(fx, at):
    for i in range(4): fx('thud', at('s1', None, .15 + i * .4), .2)
    fx('buzz', at('s2', 'MAI', -.1), .3); fx('thud', at('s2', 'MAI', .0), .5)
    fx('swoosh_up', at('s3', 'TEMPERATURA', -.2), .25); fx('chime', at('s3', 'TEMPERATURA', .5), .2)
    for i in range(3): fx('pop', at('s3', 'MOVIMENTI', -.45 + i * .2), .22, f=900 + i * 100)
    fx('sad', at('s3', 'MOVIMENTI', .6), .14)
    fx('ding', at('s4', 'CINQUE', -.1), .25); fx('pop', at('s4', 'MOBILITÀ', -.2), .3, f=800); fx('swoosh_up', at('s4', 'ARTICOLAZIONI', -.2), .2)
    for i in range(3): fx('pop', at('s5', 'AVVICINAMENTO', -.5 + i * .3), .22, f=700 + i * 150)
    fx('ding', at('s5', 'SALE', -.1), .25, f=1500)
    fx('whoosh', at('s6', None), .35); fx('msg', at('s6', 'RISCALDAMENTO', -.2), .3, f=800)
    fx('swoosh_up', at('s6', 'SCHEDA', .1), .25); fx('chime', at('s6', 'ROSSO', -.05), .22)
    fx('pop', at('s7', 'RISCALDAMENTO', -.2), .35, f=800); fx('chime', at('s7', 'RISCALDAMENTO', .1), .2)

if __name__ == '__main__':
    main(sys.modules[__name__], '31')
