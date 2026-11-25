from props4 import *

TITLE = 'Mai una settimana di scarico'
HOOK = "MAI UNA SETTIMANA\nDI SCARICO?"
LOOP = True; TAIL = 1.4
SENT = [
    ("Il tuo cliente spinge forte ogni settimana, e non scarica mai?", 's1', {'FORTE', 'MAI'}, 0.1),
    ("Errore.", 's2', {'ERRORE'}, 0.1),
    ("La fatica si accumula: i carichi si fermano e le articolazioni si lamentano.", 's3', {'FATICA', 'FERMANO', 'ARTICOLAZIONI'}, 0.1),
    ("Di solito, dopo cinque o sei settimane in salita, serve una settimana di scarico.", 's4', {'CINQUE', 'SEI', 'SCARICO'}, 0.1),
    ("Stessi esercizi, metà delle serie, carico un po' più leggero.", 's5', {'STESSI', 'METÀ', 'LEGGERO'}, 0.1),
    ("Poi si riparte, e i carichi tornano a salire.", 's6', {'RIPARTE', 'SALIRE'}, 0.1),
    ("In iki, con la progressione scegli serie e carico per ogni settimana: lo scarico è già nella scheda.", 's7', {'PROGRESSIONE', 'SERIE', 'CARICO', 'SCHEDA'}, 0.1),
    ("Mandalo al collega che non scarica mai.", 's8', {'COLLEGA'}, 0.0),
]

LOADS = (80, 82.5, 85, 87.5, 90, 75)      # kg per settimana (esempio)
SERIES = (4, 4, 4, 4, 4, 2)

def kg(v): return (f'{v:.1f}'.replace('.', ',')).replace(',0', '')

def squatter(ctx, tau, x, strain, freq=.45, s=1.0, seed=2, plates=1.0):
    face = dict(eyes='wince' if strain > .6 else ('happy' if strain < .1 else 'open'),
                mouth='shout' if strain > .6 else ('flat' if strain > .25 else 'grin'),
                brows='angry' if strain > .6 else 'neutral', look=(0, -.2))
    depth = 1.0 if strain < .6 else .55 + .1 * math.sin(tau * 3)
    sh = math.sin(tau * 40) * 6 * strain
    A = fig(ctx, 'client', squat_bar(freq * (1 - .5 * strain), depth), face, x + sh, tau, fx=.1, seed=seed, U_=U * s)
    draw_bar_on(ctx, A, x, tau, plates=plates, s=1.05 * s, shake=sh)
    if strain > .5:
        for i in range(3):
            k = (tau * 1.3 + i * .33) % 1
            drop(ctx, A['head'][0] - 95 * s + i * 95 * s, A['head'][1] - 60 + k * 120, .9 * s, (1 - k) * strain)
    return A

def s1(ctx, tau, L, wt):
    cam(ctx, 1.04, 540, 1040)
    floor(ctx, G)
    halo(ctx, (330, 1150), 480, RED, .10 + .05 * math.sin(tau * 9))
    squatter(ctx, tau, 330, 1.0, s=.95, plates=1.4)
    ph = tau * 1.6; n = int(ph) % 9 + 1
    kb = 1 + .12 * (1 - eout(clamp((ph % 1) * 4)))
    ctx.save(); ctx.translate(815, 820); ctx.scale(kb, kb); ctx.translate(-815, -820)
    flip_calendar(ctx, 650, 640, 330, str(n), 'A TUTTA', 0, head='SETT.')
    ctx.restore()
    plate_label(ctx, (815, 1110), 'NO STOP', eback(prog(tau, .35, .6)) * (1 + .06 * math.sin(tau * 12)), bg=RED, tc=WHITE, size=50, rot=.06)

def s2(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    floor(ctx, G)
    ts = wt.get('ERRORE', .15)
    no = math.sin(tau * 14) * 9
    fig(ctx, 'pt', lambda t: P(t=0, h=no, la1=-60, la2=60, ra1=60, ra2=-60), dict(eyes='open', mouth='flat', brows='angry', look=(0, 0)), 540, tau, seed=1, U_=U * .95)
    stamp_x(ctx, (540, 690), prog(tau, ts - .05, ts + .2), 1.5)

def load_bars(ctx, x0, base, vals, ks, hl=None, bw=120, gap=26, vmin=70, scale=14, cols=None, labs=None):
    for i, v in enumerate(vals):
        k = clamp(ks[i])
        if k <= 0: continue
        h = (v - vmin) * scale + 90; hh = h * eout(k); x = x0 + i * (bw + gap)
        c = (cols[i] if cols else WHITE)
        rrect(ctx, x + 7, base - hh + 9, bw, hh, 16); col(ctx, INK, .15); ctx.fill()
        rrect(ctx, x, base - hh, bw, hh, 16); fill_stroke(ctx, c, 7)
        if k > .5:
            text(ctx, kg(v), x + bw / 2, base - hh - 36, 40, FONT, RED if hl == i else INK)
            text(ctx, labs[i] if labs else f'S{i + 1}', x + bw / 2, base + 40, 30, FONTB, GRAY)
    poly(ctx, [(x0 - 30, base + 2), (x0 + len(vals) * (bw + gap) + 4, base + 2)], 7)

def s3(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    tf = wt.get('FATICA', .3); tm = wt.get('FERMANO', L * .45); ta = wt.get('ARTICOLAZIONI', L - 1.2)
    lv = lerp(1.0, .1, eio(prog(tau, tf - .1, tf + 1.2)))
    battery(ctx, (250, 700), lv, 1.6)
    plate_label(ctx, (250, 850), 'ENERGIA', 1, bg=WHITE, tc=INK, size=32)
    vals = (85, 85, 85, 85)
    ks = [prog(tau, tm - .35 + i * .16, tm - .1 + i * .16) for i in range(4)]
    load_bars(ctx, 470, 920, vals, ks, bw=110, gap=22, scale=10)
    kf = eback(prog(tau, tm + .4, tm + .7))
    plate_label(ctx, (720, 590), 'FERMI', kf, bg=INK, tc=WHITE, size=40, rot=-.04)
    floor(ctx, G)
    hurt = tau > ta - .1
    A = fig(ctx, 'client', lambda t: P(t=4, h=4, la1=-30 if hurt else -14, la2=-70 if hurt else -8, ll1=-10, ll2=-4),
            dict(eyes='wince' if hurt else 'open', mouth='frown' if hurt else 'flat', brows='worried' if hurt else 'neutral'),
            540, tau, seed=2, U_=U * .72)
    if hurt:
        k = eback(prog(tau, ta - .1, ta + .2))
        zig(ctx, A['kL'] + np.array([-60, -10]), .7 * k, -2.4, k)
        zig(ctx, A['shL'] + np.array([-60, -10]), .6 * k, -2.2, k)
        plate_label(ctx, (850, 1220), 'AHI', k, bg=RED, tc=WHITE, size=50, rot=.06)

def s4(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    tc = wt.get('CINQUE', .8); ts = wt.get('SCARICO', L - .7)
    ks = [prog(tau, .1 + i * (tc + .6) / 5, .35 + i * (tc + .6) / 5) for i in range(5)] + [prog(tau, ts - .25, ts + .05)]
    cols = [WHITE] * 5 + [SKY]
    load_bars(ctx, 85, 1260, LOADS, ks, hl=5, bw=118, gap=34, scale=26, cols=cols,
              labs=[f'SETT {i + 1}' if i == 0 else f'S{i + 1}' for i in range(6)])
    ka = prog(tau, tc + .3, tc + 1.0)
    if ka > 0:
        dashed_path(ctx, curve_pts((130, 770), (820, 520), 0), ka, 8, RED, arrow=True)
        plate_label(ctx, (300, 560), 'IN SALITA', eback(ka), bg=RED, tc=WHITE, size=40, rot=-.06)
    k6 = eback(prog(tau, ts - .1, ts + .2))
    plate_label(ctx, (860, 1370), 'SCARICO', k6 * (1 + .05 * math.sin(tau * 10)), bg=BLUE, tc=WHITE, size=46, rot=.05)

def s5(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    tst = wt.get('STESSI', .2); tm = wt.get('METÀ', L * .4); tl = wt.get('LEGGERO', L - .6)
    k = eback(prog(tau, .05, .3))
    if k <= 0: return
    ctx.save(); ctx.translate(540, 900); sscale(ctx, k); ctx.rotate(-.02); ctx.translate(-540, -900)
    rrect(ctx, 100 + 10, 580 + 14, 880, 620, 40); col(ctx, INK, .15); ctx.fill()
    rrect(ctx, 100, 580, 880, 620, 40); fill_stroke(ctx, WHITE, 9)
    text(ctx, 'SQUAT', 540, 670, 80, FONT, INK)
    if tau > tst + .2: check(ctx, (830, 660), .55 * eback(prog(tau, tst + .2, tst + .45)))
    # serie: 4 pallini, due si spengono
    text(ctx, 'SERIE', 220, 820, 40, FONT, GRAY, anchor='l')
    km = prog(tau, tm - .1, tm + .4)
    for i in range(4):
        off = i >= 2 and km > (i - 2) * .5
        cx = 520 + i * 110
        ctx.arc(cx, 818, 38, 0, 2 * math.pi); fill_stroke(ctx, (.9, .88, .85) if off else RED, 7, GRAY if off else INK)
        if off: xmark(ctx, (cx, 818), .35)
    plate_label(ctx, (540, 930), '4 → 2', eback(prog(tau, tm + .2, tm + .5)), bg=INK, tc=WHITE, size=42)
    text(ctx, 'CARICO', 220, 1080, 40, FONT, GRAY, anchor='l')
    kl = eio(prog(tau, tl - .2, tl + .4))
    v = lerp(90, 75, kl)
    text(ctx, f'{int(round(v))} kg', 700, 1080, 76, FONT, BLUE if kl > .5 else INK)
    ctx.restore()
    if kl > .3:
        for i in range(3):
            kk = (tau * 1.4 + i * .33) % 1
            ctx.save(); ctx.translate(920, 1180 - kk * 70); poly(ctx, [(-18, 0), (0, -26), (18, 0)], 8, BLUE, 1 - kk); ctx.restore()

def s6(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    tr = wt.get('RIPARTE', .4); tsa = wt.get('SALIRE', L - .6)
    vals = (85, 90, 75, 85, 90, 95)
    labs = ('S4', 'S5', 'S6', 'S1', 'S2', 'S3')
    cols = [WHITE, WHITE, SKY, LGREEN, LGREEN, LGREEN]
    ks = [1, 1, 1] + [prog(tau, tr + i * .35, tr + .25 + i * .35) for i in range(3)]
    load_bars(ctx, 85, 1000, vals, ks, hl=5, bw=118, gap=34, scale=16, cols=cols, labs=labs)
    kx = eback(prog(tau, tsa - .1, tsa + .2))
    plate_label(ctx, (900, 1110), 'RECORD', kx * (1 + .06 * math.sin(tau * 11)), bg=RED, tc=WHITE, size=40, rot=.06)
    if kx > 0: confetti(ctx, (900, 520), tau, kx)
    floor(ctx, G)
    squatter(ctx, tau, 540, .05, freq=.7, s=.6, plates=1.0)

def editor_prog_screen(w_act, chk, kprog):
    """Schermata reale di iki, lato PT: editor scheda con «Progressione» accesa (Sett 1…6, Serie / Reps / Carico / Rec (s))."""
    def content(ctx, w, h):
        app_head(ctx, w, 'Scheda')
        text(ctx, 'Giorno A', 40, 215, 38, FONT, INK, anchor='l')
        rrect(ctx, 24, 260, w - 48, 680, 22); fill_stroke(ctx, WHITE, 4, RED)
        text(ctx, 'SQUAT', 54, 315, 36, FONT, INK, anchor='l')
        sub = 'Progressione · 6 settimane' if kprog > .5 else '4 × 8 · 80 kg · rec 2\''
        text(ctx, sub, 54, 360, 24, FONTB, RED if kprog > .5 else GRAY, anchor='l')
        if kprog <= .5:
            text(ctx, '+ Progressione', 54, 860, 26, FONTB, GRAY, anchor='l')
            vals = ('4', '8', '80', '120'); wk = None
        else:
            cw = (w - 108) / 6
            for i in range(6):
                x = 54 + i * cw; on = i == w_act
                rrect(ctx, x + 3, 400, cw - 8, 54, 14)
                if on: fill_stroke(ctx, LIGHT_RED, 3, RED)
                else: fill_stroke(ctx, WHITE, 2, (.8, .78, .75))
                text(ctx, f'Sett {i + 1}', x + cw / 2 - 1, 428, 20, FONT, INK if on else GRAY)
            text(ctx, f'Copia su Sett {min(w_act + 2, 6)} →' if w_act < 5 else '', 54, 495, 22, FONTB, GRAY, anchor='l')
            text(ctx, 'Copia su tutte', w - 54, 495, 22, FONTB, RED, anchor='r')
            vals = (str(SERIES[w_act]), '8', kg(LOADS[w_act]), '120'); wk = w_act
            check(ctx, (70, 858), .3, RED); text(ctx, 'Progressione', 92, 860, 26, FONTB, RED, anchor='l')
        fw = (w - 108 - 3 * 10) / 4
        for i, (lab, v) in enumerate(zip(('SERIE', 'REPS', 'CARICO', 'REC (S)'), vals)):
            x = 54 + i * (fw + 10)
            text(ctx, lab, x + fw / 2, 560, 19, FONT, GRAY)
            hot = wk == 5 and i in (0, 2)
            z = 1 + .1 * chk * hot
            ctx.save(); ctx.translate(x + fw / 2, 640); ctx.scale(z, z)
            rrect(ctx, -fw / 2, -48, fw, 96, 14); fill_stroke(ctx, LIGHT_RED if hot else (.97, .96, .94), 3, RED if hot else (.8, .78, .75))
            text(ctx, v, 0, 2, 40, FONT, INK)
            ctx.restore()
        text(ctx, 'Nota per il cliente…', 54, 760, 24, FONTB, (.7, .68, .65), anchor='l')
        text(ctx, 'PANCA PIANA', 40, 1010, 32, FONT, INK, anchor='l')
        text(ctx, 'Progressione · 6 settimane', 40, 1050, 22, FONTB, RED, anchor='l')
    return content

def s7(ctx, tau, L, wt):
    up = eout(prog(tau, 0, .35))
    halo(ctx, (540, 1100), 760, RED, .12)
    tp = wt.get('PROGRESSIONE', 1.0); tse = wt.get('SERIE', L * .5); tsc = wt.get('SCHEDA', L - .6)
    tscar = max(tse + .9, wt.get('SCARICO', tsc - 1.0) - .25)
    kprog = prog(tau, tp - .1, tp + .1)
    if tau < tse: w_act = 0
    elif tau < tscar: w_act = min(4, int((tau - tse) / max(.2, (tscar - tse) / 5)))
    else: w_act = 5
    chk = math.sin(prog(tau, tscar, tscar + .5) * math.pi)
    phone(ctx, 540, lerp(2600, 1130, up), 640, 1120, editor_prog_screen(w_act, chk, kprog))
    if tau < tscar:
        status_chip(ctx, 540, 500, 'Ogni settimana i suoi numeri', INK, prog(tau, tse - .3, tse), 34)
    else:
        status_chip(ctx, 540, 500, 'Sett 6: scarico già in scheda', RED, prog(tau, tscar, tscar + .3), 34)

def s8(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    tc = wt.get('COLLEGA', .4)
    floor(ctx, G)
    fig(ctx, 'pt', lambda t: P(t=3, ra1=150 + 16 * math.sin(t * 9), ra2=172 + 20 * math.sin(t * 9 + .6), la1=-16, la2=-8),
        dict(eyes='happy', mouth='grin', brows='raised'), 300, tau, fx=.2, seed=1, U_=U * .95)
    squatter(ctx, tau, 770, .05, freq=.6, s=.8, seed=3, plates=.8)
    send_card(ctx, prog(tau, tc - .5, tc - .1), 660, tau, sub='CHE NON SCARICA MAI')

SCENES = dict(s1=s1, s2=s2, s3=s3, s4=s4, s5=s5, s6=s6, s7=s7, s8=s8)

def SFX(fx, at):
    for i in range(4): fx('thud', at('s1', None, .15 + i * .55), .28)
    fx('buzz', at('s2', 'ERRORE', -.05), .3); fx('thud', at('s2', 'ERRORE', .0), .5)
    fx('swoosh_down', at('s3', 'FATICA', -.1), .3)
    for i in range(4): fx('tick', at('s3', 'FERMANO', -.35 + i * .16), .25)
    fx('buzz', at('s3', 'ARTICOLAZIONI', -.05), .2); fx('sad', at('s3', 'ARTICOLAZIONI', .3), .14)
    for i in range(5): fx('pop', at('s4', None, .15 + i * .3), .22, f=700 + i * 110)
    fx('swoosh_down', at('s4', 'SCARICO', -.25), .25); fx('ding', at('s4', 'SCARICO', .0), .22, f=1100)
    fx('ding', at('s5', 'STESSI', .2), .2, f=1300); fx('pop', at('s5', 'METÀ', 0), .25, f=600); fx('swoosh_down', at('s5', 'LEGGERO', -.1), .22)
    for i in range(3): fx('pop', at('s6', 'RIPARTE', i * .35), .22, f=900 + i * 150)
    fx('chime', at('s6', 'SALIRE', -.05), .22); fx('clap', at('s6', 'SALIRE', .1), .18)
    fx('whoosh', at('s7', None), .35); fx('ding', at('s7', 'PROGRESSIONE', 0), .22)
    for i in range(5): fx('tick', at('s7', 'SERIE', .2 + i * .3), .2)
    fx('chime', at('s7', 'SCHEDA', -.6), .22)
    fx('swoosh_up', at('s8', 'COLLEGA', -.4), .3); fx('chime', at('s8', 'COLLEGA', .1), .2)

if __name__ == '__main__':
    main(sys.modules[__name__], '33')
