from props4 import *

TITLE = 'Nuova scheda a occhio'
HOOK = "NUOVA SCHEDA\nA OCCHIO?"
LOOP = True; TAIL = 1.4
CTA = 'QUESTIONARIO'
SENT = [
    ("La nuova scheda la fai a occhio?", 's1', {'OCCHIO'}, 0.1),
    ("Sbagliato.", 's2', {'SBAGLIATO'}, 0.1),
    ("Così rischi di ripetere gli stessi sbagli: l'esercizio che gli dava fastidio, le sedute troppo lunghe.", 's3', {'SBAGLI', 'FASTIDIO', 'LUNGHE'}, 0.1),
    ("Prima chiedigli tre cose: se i carichi sono saliti, com'era il recupero, e su cosa vuole puntare.", 's4', {'TRE', 'CARICHI', 'RECUPERO', 'PUNTARE'}, 0.1),
    ("E se ti segnala un fastidio, quell'esercizio lo cambi.", 's5', {'FASTIDIO', 'CAMBI'}, 0.1),
    ("In iki, una settimana prima della fine, al cliente arriva il questionario, e tu leggi le risposte prima della prossima scheda.", 's6', {'SETTIMANA', 'QUESTIONARIO', 'RISPOSTE', 'PROSSIMA'}, 0.1),
    ("Scrivi «questionario» nei commenti, e ti mando come funziona.", 's7', {'QUESTIONARIO'}, 0.0),
]

CHIP_BG = (.95, .94, .92)
EX = ('Squat', 'Dip', 'Rematore')
POOL = ('Squat', 'Dip', 'Affondi', 'Rematore', 'Stacco', 'Lat machine', 'Panca')

def wrap(ctx, s, size, font, maxw):
    ctx.select_font_face(font); ctx.set_font_size(size)
    out, cur = [], ''
    for w in s.split():
        tr = (cur + ' ' + w).strip()
        if ctx.text_extents(tr).width > maxw and cur: out.append(cur); cur = w
        else: cur = tr
    if cur: out.append(cur)
    return out

def para(ctx, s, x, y, size, font, c, maxw, lh=1.3):
    lines = wrap(ctx, s, size, font, maxw)
    for i, ln in enumerate(lines): text(ctx, ln, x, y + i * size * lh, size, font, c, anchor='l')
    return y + len(lines) * size * lh

def pt_point(ctx, tau, x, face, s=.95, g=None):
    return fig(ctx, 'pt', lambda t: P(t=3, ra1=120 + 25 * math.sin(t * 7), ra2=140 + 25 * math.sin(t * 7 + .6), la1=-20, la2=-10),
               face, x, tau, fx=.2, seed=1, U_=U * s, g=g)

def s1(ctx, tau, L, wt):
    cam(ctx, 1.04, 540, 1040)
    floor(ctx, G)
    halo(ctx, (540, 1150), 520, RED, .10 + .05 * math.sin(tau * 9))
    pt_point(ctx, tau, 270, dict(eyes='closed', mouth='smirk', brows='raised'), s=1.0)
    # scheda che si riempie a caso
    items = [POOL[(int(tau * 7) + i * 3) % len(POOL)] for i in range(3)]
    ctx.save(); ctx.translate(740, 820); ctx.rotate(.04 + .02 * math.sin(tau * 6)); ctx.translate(-740, -820)
    list_card(ctx, 530, 610, 420, items, title='NUOVA')
    ctx.restore()
    plate_label(ctx, (740, 1130), 'A CASO?', eback(prog(tau, .35, .6)) * (1 + .06 * math.sin(tau * 12)), bg=RED, tc=WHITE, size=52, rot=.06)

def s2(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    floor(ctx, G)
    ts = wt.get('SBAGLIATO', .15)
    no = math.sin(tau * 14) * 9
    fig(ctx, 'pt', lambda t: P(t=0, h=no, la1=-60, la2=60, ra1=60, ra2=-60), dict(eyes='open', mouth='flat', brows='angry', look=(0, 0)), 540, tau, seed=1, U_=U * .95)
    stamp_x(ctx, (540, 690), prog(tau, ts - .05, ts + .2), 1.5)

def s3(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    tsb = wt.get('SBAGLI', .8); tf = wt.get('FASTIDIO', L * .55); tl = wt.get('LUNGHE', L - .7)
    for i, (x, tit) in enumerate(((65, 'SCHEDA 1'), (575, 'SCHEDA 2'))):
        k = eback(prog(tau, .05 + i * (tsb - .1), .35 + i * (tsb - .1)))
        if k <= 0: continue
        hl = 1 if tau > tf - .1 else None
        ctx.save(); ctx.translate(x + 220, 880); sscale(ctx, k); ctx.rotate((-.03, .03)[i]); ctx.translate(-(x + 220), -880)
        list_card(ctx, x, 670, 440, EX, hl=hl, title=tit)
        ctx.restore()
    if tau > tsb:
        ka = prog(tau, tsb, tsb + .5)
        dashed_path(ctx, curve_pts((380, 640), (720, 640), -.3), ka, 8, RED, arrow=True)
        plate_label(ctx, (550, 590), 'DI NUOVO', eback(ka), bg=INK, tc=WHITE, size=34)
    plate_label(ctx, (540, 1170), 'FASTIDIO SPALLA', eback(prog(tau, tf - .1, tf + .2)), bg=RED, tc=WHITE, size=46, rot=-.03)
    kl = eback(prog(tau, tl - .25, tl + .05))
    if kl > 0:
        ctx.save(); ctx.translate(330, 1350); sscale(ctx, kl)
        clock(ctx, (0, 0), 90, tau * 5); ctx.restore()
        plate_label(ctx, (650, 1350), '90 MINUTI', kl, bg=WHITE, tc=INK, size=50, rot=.03)
        if tau > tl + .3: xmark(ctx, (870, 1290), .7 * eback(prog(tau, tl + .3, tl + .55)))

def s4(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    tt = wt.get('TRE', .5); tc = wt.get('CARICHI', 1.2); tr = wt.get('RECUPERO', L * .6); tp = wt.get('PUNTARE', L - .6)
    kb = eback(prog(tau, .05, .35))
    bubble(ctx, 540, 540, 560, 120, "Com'è andata?", kb, tail=(1, 1), size=50)
    items = (('dumbbell', 'CARICHI SALITI?'), ('clock', 'RECUPERO?'), ('target', 'SU COSA PUNTARE?'))
    ks = [prog(tau, t0 - .05, t0 + .2) for t0 in (tc, tr, tp)]
    ka = eback(prog(tau, tt - .3, tt))
    if ka > 0:
        ctx.save(); ctx.translate(540, 870); sscale(ctx, ka); ctx.translate(-540, -870)
        checklist(ctx, 90, 660, 900, items, ks, row=130)
        ctx.restore()
    floor(ctx, G)
    pt_point(ctx, tau, 820, dict(eyes='happy', mouth='smile', brows='raised'), s=.55)
    fig(ctx, 'client', lambda t: P(t=0, h=6 * math.sin(t * 4)), dict(eyes='open', mouth='smile', look=(1, 0)), 260, tau, seed=2, U_=U * .55)
    plate_label(ctx, (540, 1180), '3 DOMANDE', eback(prog(tau, tt - .1, tt + .2)), bg=RED, tc=WHITE, size=46, rot=.03)

def s5(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    tf = wt.get('FASTIDIO', .8); tc = wt.get('CAMBI', L - .5)
    floor(ctx, G)
    hurt = tau > tf - .1
    A = fig(ctx, 'client', lambda t: P(t=0, la1=-14, la2=-8, ra1=-25 if hurt else 14, ra2=-165 if hurt else 8),
            dict(eyes='wince' if hurt else 'open', mouth='frown' if hurt else 'smile', brows='angry' if hurt else 'neutral'),
            300, tau, seed=2, U_=U * .9)
    if hurt:
        k = eback(prog(tau, tf - .1, tf + .2))
        zig(ctx, A['shL'] + np.array([-70, -20]), .8 * k, -2.4, k)
        zig(ctx, A['shL'] + np.array([-60, 50]), .6 * k, 3.0, k)
        plate_label(ctx, (290, 700), 'SPALLA', k, bg=RED, tc=WHITE, size=44, rot=-.05)
    # card esercizio
    k1 = eback(prog(tau, .05, .35))
    if k1 > 0:
        ctx.save(); ctx.translate(780, 800); sscale(ctx, k1); ctx.rotate(.03)
        rrect(ctx, -200 + 8, -90 + 10, 400, 180, 30); col(ctx, INK, .15); ctx.fill()
        rrect(ctx, -200, -90, 400, 180, 30); fill_stroke(ctx, LIGHT_RED if hurt else WHITE, 8, RED if hurt else INK)
        text(ctx, 'DIP', 0, 2, 76, FONT, INK)
        if tau > tc - .1:
            kx = eback(prog(tau, tc - .1, tc + .15))
            poly(ctx, [(-150, 10), (150, -10)], 12 * kx, RED)
        ctx.restore()
    kn = eback(prog(tau, tc + .1, tc + .4))
    if kn > 0:
        dashed_path(ctx, curve_pts((780, 900), (780, 1040), .3), prog(tau, tc, tc + .3), 8, RED, arrow=True)
        ctx.save(); ctx.translate(780, 1150); sscale(ctx, kn); ctx.rotate(-.03)
        rrect(ctx, -220 + 8, -80 + 10, 440, 160, 30); col(ctx, INK, .15); ctx.fill()
        rrect(ctx, -220, -80, 440, 160, 30); fill_stroke(ctx, LGREEN, 8, INK)
        text(ctx, 'ALTERNATIVA', -20, 2, 48, FONT, INK)
        ctx.restore()
        check(ctx, (990, 1080), .7 * kn)

def client_q_screen(hl):
    """Schermata reale di iki, lato cliente: card del questionario in home (CardQuestionario)."""
    def content(ctx, w, h):
        app_head(ctx, w, '')
        rrect(ctx, 30, 200, w - 60, 470, 24); fill_stroke(ctx, WHITE, 4, RED)
        text(ctx, 'Dal tuo personal trainer', 60, 248, 24, FONTB, GRAY, anchor='l')
        y = para(ctx, 'Manca una settimana alla fine della scheda', 60, 298, 34, FONT, INK, w - 130, 1.2)
        y = para(ctx, "Dimmi com'è andata, così preparo la prossima su misura per te. Ti servono 3 minuti.", 60, y + 20, 25, FONTB, GRAY, w - 130, 1.35)
        z = 1 + .1 * hl
        ctx.save(); ctx.translate(140, y + 50); ctx.scale(z, z)
        rrect(ctx, -90, -34, 180, 68, 16); col(ctx, RED); ctx.fill()
        text(ctx, 'Rispondi  ›', 0, 1, 26, FONT, WHITE)
        ctx.restore()
        text(ctx, 'Più tardi', 300, y + 51, 26, FONTB, GRAY, anchor='l')
        text(ctx, 'Giorno 1', 40, 740, 38, FONT, INK, anchor='l')
        for i, n_ in enumerate(EX):
            yy = 780 + i * 96
            rrect(ctx, 30, yy, w - 60, 80, 16); col(ctx, CHIP_BG); ctx.fill()
            text(ctx, n_, 54, yy + 41, 28, FONTB, INK, anchor='l')
    return content

QA = (('VALUTAZIONE E CARICHI', (("Come valuti questa scheda nel complesso?", 'Molto impegnativa'),
                                 ("Hai aumentato carichi o ripetizioni nel corso delle settimane?", 'Solo in alcuni esercizi'))),
      ('TEMPI, VOLUME E RECUPERO', (("Com'era il recupero tra una seduta e l'altra?", "Un po' di stanchezza, ma gestibile"),)))

def pt_q_screen(p, hl):
    """Schermata reale di iki, lato PT: 'Marco · questionario' (LeggiQuestionarioPT) con avviso Fastidio e risposte."""
    def content(ctx, w, h):
        app_head(ctx, w, '')
        text(ctx, 'Marco · questionario', 40, 210, 34, FONT, INK, anchor='l')
        text(ctx, 'Forza A/B · risposto il 20/11/2026', 40, 256, 22, FONTB, GRAY, anchor='l')
        y = 290
        k0 = eout(prog(p, 0, .2))
        if k0 > 0:
            rrect(ctx, 30, y, w - 60, 110, 16); fill_stroke(ctx, LIGHT_RED, 3, RED)
            ctx.move_to(56, y + 50); ctx.line_to(72, y + 22); ctx.line_to(88, y + 50); ctx.close_path(); ctx.set_line_width(4); col(ctx, RED); ctx.stroke()
            text(ctx, '!', 72, y + 41, 16, FONT, RED)
            text(ctx, 'Fastidio: Dip', 100, y + 38, 27, FONT, RED, anchor='l')
            text(ctx, 'fastidio alla spalla destra', 56, y + 80, 23, FONTB, INK, anchor='l')
        y += 140
        n = 0
        for si, (sez, rows) in enumerate(QA):
            ks = eout(prog(p, .2 + n * .17, .35 + n * .17))
            if ks <= 0: break
            text(ctx, sez, 40, y, 19, FONT, GRAY, anchor='l'); y += 22
            for q, a in rows:
                kr = eout(prog(p, .2 + n * .17, .35 + n * .17)); n += 1
                if kr <= 0: break
                ql = wrap(ctx, q, 20, FONTB, w - 120)
                rh = 30 + len(ql) * 26 + 34
                rrect(ctx, 30, y, w - 60, rh, 14); col(ctx, CHIP_BG); ctx.fill()
                for j, ln in enumerate(ql): text(ctx, ln, 54, y + 26 + j * 26, 20, FONTB, GRAY, anchor='l')
                text(ctx, a, 54, y + 30 + len(ql) * 26 + 6, 25, FONTB, INK, anchor='l')
                y += rh + 10
            y += 24
        kb = prog(p, .85, 1)
        if kb > 0:
            z = 1 + .06 * hl
            ctx.save(); ctx.translate(w / 2, h - 105); ctx.scale(z * eback(kb), z * eback(kb))
            rrect(ctx, -(w - 60) / 2, -38, w - 60, 76, 16); col(ctx, RED); ctx.fill()
            text(ctx, 'Prepara la prossima scheda', 0, 1, 27, FONT, WHITE)
            ctx.restore()
    return content

def s6(ctx, tau, L, wt):
    up = eout(prog(tau, 0, .35))
    halo(ctx, (540, 1100), 760, RED, .12)
    tse = wt.get('SETTIMANA', 1.0); tq = wt.get('QUESTIONARIO', L * .45); tr = wt.get('RISPOSTE', L * .7); tp = wt.get('PROSSIMA', L - .6)
    sw_t = min(tr - .3, tq + .6)
    if tau < sw_t:
        scr = client_q_screen(math.sin(prog(tau, tq - .1, tq + .4) * math.pi))
        chip = ("Lato cliente: arriva da solo", INK, prog(tau, tse - .2, tse + .1))
    else:
        scr = pt_q_screen(prog(tau, sw_t + .1, tp - .1), math.sin(prog(tau, tp - .1, tp + .4) * math.pi))
        chip = ("Lato PT: leggi le risposte", RED, prog(tau, sw_t + .2, sw_t + .5))
    sw = 1 - abs(2 * prog(tau, sw_t - .4, sw_t) - 1) if sw_t - .4 < tau < sw_t else 1
    phone(ctx, 540, lerp(2600, 1130, up), 640 * max(.05, sw), 1120, scr)
    status_chip(ctx, 540, 500, chip[0], chip[1], chip[2], 34)

def s7(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    tc = wt.get('QUESTIONARIO', .4)
    floor(ctx, G)
    fig(ctx, 'pt', lambda t: P(t=3, ra1=150 + 16 * math.sin(t * 9), ra2=172 + 20 * math.sin(t * 9 + .6), la1=-16, la2=-8),
        dict(eyes='happy', mouth='grin', brows='raised'), 300, tau, fx=.2, seed=1, U_=U * .95)
    fig(ctx, 'client', lambda t: P(t=0, h=5 * math.sin(t * 5), ra1=150 + 10 * math.sin(t * 7), ra2=170),
        dict(eyes='happy', mouth='smile', look=(-1, 0)), 780, tau, seed=3, U_=U * .85)
    cta_card(ctx, CTA, prog(tau, tc - .3, tc + .1), 660, tau)

SCENES = dict(s1=s1, s2=s2, s3=s3, s4=s4, s5=s5, s6=s6, s7=s7)

def SFX(fx, at):
    for i in range(4): fx('pop', at('s1', None, .15 + i * .35), .2, f=700 + i * 120)
    fx('buzz', at('s2', 'SBAGLIATO', -.05), .3); fx('thud', at('s2', 'SBAGLIATO', .0), .5)
    fx('swoosh_up', at('s3', 'SBAGLI', -.1), .25); fx('buzz', at('s3', 'FASTIDIO', -.05), .2)
    fx('sad', at('s3', 'LUNGHE', .2), .14)
    fx('pop', at('s4', None, .05), .25, f=800)
    for i, w in enumerate(('CARICHI', 'RECUPERO', 'PUNTARE')): fx('ding', at('s4', w, -.05), .22, f=1200 + i * 150)
    fx('thud', at('s5', 'FASTIDIO', -.05), .35); fx('swoosh_down', at('s5', 'CAMBI', -.1), .25); fx('chime', at('s5', 'CAMBI', .3), .2)
    fx('whoosh', at('s6', None), .35); fx('msg', at('s6', 'QUESTIONARIO', -.1), .3, f=800)
    fx('swoosh_up', at('s6', 'RISPOSTE', -.3), .25); fx('chime', at('s6', 'PROSSIMA', -.05), .22)
    fx('pop', at('s7', 'QUESTIONARIO', -.2), .35, f=800); fx('chime', at('s7', 'QUESTIONARIO', .1), .2)

if __name__ == '__main__':
    main(sys.modules[__name__], '32')
