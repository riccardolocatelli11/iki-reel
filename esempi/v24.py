from props4 import *

TITLE = 'EMOM o AMRAP'
HOOK = "EMOM O AMRAP?\nNON A CASO."
LOOP = True; TAIL = 1.8
AMB = ('24_amb', .45)
SENT = [
    ("EMOM o AMRAP?", 's1', {'EMOM', 'AMRAP'}, 0.1),
    ("Molti li usano a caso.", 's2', {'CASO'}, 0.1),
    ("EMOM vuol dire: all'inizio di ogni minuto fai le tue ripetizioni, e quello che avanza è recupero.", 's3', {'MINUTO', 'RECUPERO'}, 0.1),
    ("Perfetto per tenere un ritmo costante.", 's4', {'COSTANTE'}, 0.1),
    ("AMRAP vuol dire: più giri possibili in un tempo fisso.", 's5', {'GIRI', 'FISSO'}, 0.1),
    ("Perfetto per misurare i progressi: la prossima volta, un giro in più!", 's6', {'PROGRESSI', 'PIÙ'}, 0.1),
    ("In iki il cliente trova il timer già impostato nella scheda, con il beep a ogni minuto.", 's7', {'TIMER', 'BEEP'}, 0.1),
    ("Scrivi «circuito» nei commenti, e ti mando come funziona.", 's8', {'CIRCUITO'}, 0.0),
]

def mode_card(ctx, c, title, sub, k, cc=RED, rot=0.0, ok=0.0):
    if k <= 0: return
    ctx.save(); flip_in(ctx, c, k); ctx.translate(*c); ctx.rotate(rot)
    rrect(ctx, -200 + 10, -150 + 12, 400, 300, 34); col(ctx, INK, .15); ctx.fill()
    rrect(ctx, -200, -150, 400, 300, 34); fill_stroke(ctx, WHITE, 9)
    rrect(ctx, -200, -150, 400, 110, 34); col(ctx, cc); ctx.fill(); ctx.rectangle(-200, -70, 400, 30); ctx.fill()
    text(ctx, title, 0, -92, 72, FONT, WHITE)
    for i, ln in enumerate(sub.split('\n')): text(ctx, ln, 0, 30 + i * 52, 40, FONT, INK)
    ctx.restore()
    if ok > 0: check(ctx, (c[0] + 170, c[1] - 160), .8 * eback(ok))

def s1(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    te = wt.get('EMOM', .1); ta = wt.get('AMRAP', .7)
    mode_card(ctx, (290, 760), 'EMOM', 'ogni\nminuto', prog(tau, te - .1, te + .25), RED, -.05)
    mode_card(ctx, (790, 760), 'AMRAP', 'più giri\npossibili', prog(tau, ta - .1, ta + .25), BLUE, .05)
    floor(ctx, G)
    fig(ctx, 'pt', lambda t: P(t=0, h=12 * math.sin(t * 5), la1=-150, la2=-200, ra1=30, ra2=20), dict(eyes='wide', mouth='wavy', brows='worried', look=(math.sin(tau * 4), -.6)), 540, tau, seed=1, U_=U * .75)

def s2(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    tc = wt.get('CASO', L - .4)
    spin = 14 * eout(prog(tau, 0, tc + .1))
    c = (540, 820); r = 260
    ctx.save(); ctx.translate(*c); ctx.rotate(spin)
    for i in range(6):
        ctx.move_to(0, 0); ctx.arc(0, 0, r, i * math.pi / 3, (i + 1) * math.pi / 3); ctx.close_path(); fill_stroke(ctx, RED if i % 2 == 0 else BLUE, 7)
        a = (i + .5) * math.pi / 3
        ctx.save(); ctx.translate(math.cos(a) * r * .62, math.sin(a) * r * .62); ctx.rotate(a + math.pi / 2)
        text(ctx, 'EMOM' if i % 2 == 0 else 'AMRAP', 0, 0, 36, FONT, WHITE); ctx.restore()
    ctx.restore()
    ctx.arc(*c, 34, 0, 2 * math.pi); fill_stroke(ctx, WHITE, 8)
    ctx.move_to(c[0] - 30, c[1] - r - 40); ctx.line_to(c[0] + 30, c[1] - r - 40); ctx.line_to(c[0], c[1] - r + 20); ctx.close_path(); fill_stroke(ctx, YELLOW, 7)
    floor(ctx, G)
    fig(ctx, 'pt', lambda t: P(t=0, la1=-70, la2=-120, ra1=70, ra2=120), dict(eyes='open', mouth='wavy', brows='worried', look=(0, -.6)), 540, tau, seed=1, U_=U * .5)
    plate_label(ctx, (540, 1180), 'A CASO', eback(prog(tau, tc - .1, tc + .2)), bg=INK, tc=WHITE, size=50)

def burpee_guy(ctx, x, tau, active, s=.55, seed=2):
    if active:
        q = .5 + .5 * math.sin(tau * 9)
        pose = lambda t: P(t=0, la1=lerp(-160, -20, q), la2=lerp(-175, -10, q), ra1=lerp(160, 20, q), ra2=lerp(175, 10, q), y=-60 * q, ll1=-14 * q, rl1=14 * q)
        face = dict(eyes='wince', mouth='shout', brows='angry')
    else:
        pose = lambda t: P(t=0, h=6 * math.sin(t * 3), la1=-20, ra1=20)
        face = dict(eyes='closed', mouth='smile', brows='neutral')
    return fig(ctx, 'client', pose, face, x, tau, seed=seed, U_=U * s)

def s3(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    tm = wt.get('MINUTO', 1.5); tr = wt.get('RECUPERO', L - .8)
    mode_card(ctx, (540, 640), 'EMOM', 'Every Minute On the Minute', 1, RED) if False else None
    rrect(ctx, 300, 560, 480, 110, 30); col(ctx, RED); ctx.fill(); text(ctx, 'EMOM', 540, 616, 70, FONT, WHITE)
    cur = clamp((tau - tm + .5) / max(L - tm, 1)) * 4.0
    minute_blocks(ctx, 90, 760, 900, 4, cur, .6)
    work = (cur % 1) < .6 and cur > 0
    floor(ctx, G)
    burpee_guy(ctx, 540, tau, work, .6)
    if tau > tm: plate_label(ctx, (270, 1040), 'LAVORO', eback(prog(tau, tm, tm + .3)), bg=RED, tc=WHITE, size=40)
    if tau > tr - .1: plate_label(ctx, (810, 1040), 'RECUPERO', eback(prog(tau, tr - .1, tr + .2)), bg=GREEN, tc=WHITE, size=40)

def s4(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    tc = wt.get('COSTANTE', L - .8)
    pts = []
    for i in range(121):
        x = 80 + i * 7.6; ph = (i % 30) / 30
        y = 860 - (160 if .3 < ph < .36 else (-60 if .36 <= ph < .42 else 0))
        pts.append((x, y))
    dashed_path(ctx, pts, eio(prog(tau, 0, L * .9)), 10, RED, 4000)
    for i in range(4): text(ctx, f"{i + 1}'", 80 + (i * 30 + 10) * 7.6, 960, 34, FONT, GRAY)
    k = prog(tau, tc - .2, tc + .2)
    if k > 0:
        ctx.save(); flip_in(ctx, (540, 1220), k)
        rrect(ctx, 200, 1150, 680, 140, 34); fill_stroke(ctx, RED, 8); text(ctx, 'RITMO COSTANTE', 540, 1222, 58, FONT, WHITE); ctx.restore()

def s5(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    tg = wt.get('GIRI', 1.2); tf = wt.get('FISSO', L - .6)
    rrect(ctx, 300, 560, 480, 110, 30); col(ctx, BLUE); ctx.fill(); text(ctx, 'AMRAP', 540, 616, 70, FONT, WHITE)
    c = np.array([330, 1020]); R = 200
    ctx.arc(*c, R, 0, 2 * math.pi); col(ctx, INK, .25); ctx.set_line_width(26); ctx.stroke()
    lap = max(0, tau - tg + .6) * 1.5
    ctx.arc(*c, R, -math.pi / 2, -math.pi / 2 + 2 * math.pi * (lap % 1)); col(ctx, BLUE); ctx.set_line_width(26); ctx.stroke()
    a = -math.pi / 2 + 2 * math.pi * (lap % 1)
    ctx.arc(c[0] + math.cos(a) * R, c[1] + math.sin(a) * R, 30, 0, 2 * math.pi); fill_stroke(ctx, WHITE, 8)
    lap_counter(ctx, (790, 900), int(lap) + 1, (lap % 1) * 3, 'GIRI', BLUE)
    k = prog(tau, tf - .2, tf + .2)
    if k > 0:
        ctx.save(); flip_in(ctx, (790, 1260), k)
        rrect(ctx, 600, 1180, 380, 160, 30); fill_stroke(ctx, INK, 8)
        text(ctx, 'TEMPO FISSO', 790, 1225, 30, FONTB, WHITE); text(ctx, "12:00", 790, 1290, 64, FONT, YELLOW); ctx.restore()

def s6(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    tp = wt.get('PROGRESSI', .9); tpi = wt.get('PIÙ', L - .5)
    mode_card(ctx, (290, 800), 'OGGI', '5 giri', prog(tau, 0, .3), INK, -.04)
    k = prog(tau, tpi - .5, tpi - .1)
    mode_card(ctx, (790, 800), 'PROSSIMA', '6 giri', k, GREEN, .04)
    dashed_path(ctx, curve_pts((470, 760), (610, 760), -.3), prog(tau, tp - .2, tp + .5), 8, RED, 18)
    if tau > tpi - .1:
        plate_label(ctx, (790, 1020), '+1 GIRO', eback(prog(tau, tpi - .1, tpi + .2)), bg=RED, tc=WHITE, size=56)
        confetti(ctx, (790, 760), tau, prog(tau, tpi, tpi + 1.2))
    floor(ctx, G)
    hop = abs(math.sin(tau * 8)) * 60 if tau > tpi else 0
    fig(ctx, 'client', lambda t: P(t=0, y=-hop, la1=-150, la2=-170, ra1=150, ra2=170), dict(eyes='happy', mouth='grin', brows='raised'), 540, tau, seed=2, U_=U * .55)

def s7(ctx, tau, L, wt):
    tt = wt.get('TIMER', 1.0); tb = wt.get('BEEP', L - 1.2)
    up = eout(prog(tau, 0, .35))
    halo(ctx, (540, 1150), 760, RED, .14)
    sec = 60 - int(clamp(prog(tau, tt, L)) * 59) if tau < tb else 60
    frac = (60 - sec) / 60
    bk = prog(tau, tb, tb + .8)
    phone(ctx, 540, lerp(2600, 1150, up), 640, 1180, emom_screen(frac if tau < tb else 1.0, '0:00' if tau >= tb else f'0:{sec:02d}', 'EMOM · MINUTO 3', bk if 0 < bk < 1 else 0, 'Prossimo minuto: BEEP!' if tau > tb else None))
    status_chip(ctx, 540, 520, 'Timer già impostato', RED, prog(tau, tt - .1, tt + .3), 36)

def s8(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    tc = wt.get('CIRCUITO', .4)
    mode_card(ctx, (290, 1000), 'EMOM', 'ritmo', 1, RED, -.05, prog(tau, .1, .4))
    mode_card(ctx, (790, 1000), 'AMRAP', 'progressi', 1, BLUE, .05, prog(tau, .3, .6))
    cta_card(ctx, 'CIRCUITO', prog(tau, tc - .3, tc + .1), 640, tau)

SCENES = dict(s1=s1, s2=s2, s3=s3, s4=s4, s5=s5, s6=s6, s7=s7, s8=s8)

def SFX(fx, at):
    fx('file:24_fx1', at('s1', None, .05), .5, max=2.6)
    fx('pop', at('s1', 'EMOM', -.1), .3); fx('pop', at('s1', 'AMRAP', -.1), .3, f=1200)
    for i in range(8): fx('tick', at('s2', None, .1 + i * .11 * (1 + i * .15)), .35)
    fx('boing', at('s2', 'CASO', -.05), .25)
    fx('file:24_fx2', at('s3', None, .2), .5)
    fx('ding', at('s3', 'MINUTO', -.1), .25); fx('ding', at('s3', 'RECUPERO', -.1), .2, f=990)
    fx('swoosh_up', at('s4', 'COSTANTE', -.3), .3)
    fx('file:24_fx3', at('s5', None, .05), .55)
    fx('file:24_fx4', at('s6', 'PIÙ', -.2), .55)
    fx('whoosh', at('s7', None), .35); fx('file:24_fx5', at('s7', 'BEEP', -.05), .55)
    fx('pop', at('s8', 'CIRCUITO', -.2), .35, f=800)

if __name__ == '__main__':
    main(sys.modules[__name__], '24')
