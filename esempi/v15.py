from props3 import *

TITLE = 'Mi mandi il bonifico'
HOOK = 'MI MANDI\nIL BONIFICO?'
LOOP = True; TAIL = 1.1
SENT = [
    ("Mi mandi il bonifico?…", 's1', {'BONIFICO'}, 0.1),
    ("Se a fine mese lo scrivi a metà dei clienti, non sei più un coach.", 's2', {'METÀ', 'COACH'}, 0.0),
    ("Sei un esattore.", 's3', {'ESATTORE'}, 0.1),
    ("E ogni sollecito pesa sul rapporto.", 's4', {'RAPPORTO'}, 0.1),
    ("Il trucco? Separare i due ruoli.", 's5', {'SEPARARE'}, 0.1),
    ("Rate fisse, con una data chiara, decise il primo giorno.", 's6', {'FISSE', 'PRIMO'}, 0.1),
    ("Così in allenamento non si parla mai di soldi.", 's7', {'MAI'}, 0.1),
    ("Con iki colleghi il tuo Stripe, e il cliente paga le rate direttamente dall'app!", 's8', {'STRIPE', "DALL'APP"}, 0.1),
    ("Scrivi «rate» nei commenti, e ti mando come funziona.", 's9', {'RATE'}, 0.0),
]
MSG = ('Mi mandi il bonifico?', 'r', (.86, .95, .84), INK)

def typing(t):  # braccia davanti, pollici che digitano
    return P(t=4, h=10, la1=-150 + 6 * math.sin(t * 22), la2=-200, ra1=150 + 6 * math.sin(t * 25 + 1), ra2=200)

def s1(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    floor(ctx, G)
    # cliente che scappa a destra
    xr = lerp(880, 1250, eio(prog(tau, .3, 1.6)))
    fig(ctx, 'client', lambda t: walk(t * 2 * math.pi * 2.6, 1, .1, 1.6), dict(eyes='wide', mouth='shout', brows='worried', look=(1, 0)), xr, tau, fx=.6, seed=2, U_=U * .7)
    phone(ctx, 600, 1060, 560, 1000, chat_screen([MSG] * 6, .6 + tau * 3.2, 'Marco'), rot=.04 * math.sin(tau * 9))
    A = fig(ctx, 'pt', typing, dict(eyes='wide', mouth='wavy', brows='worried', look=(1, 0)), 190, tau, fx=.5, seed=1, U_=U * .75)
    k = (tau * 1.4) % 1; drop(ctx, A['head'][0] - 80, A['head'][1] - 10 + k * 70, 1.0, 1 - k)

def mini(ctx, x, g, face, tau, seed, s=.42):
    return draw_anim(ctx, 'client', lambda t: P(t=0, h=3 * math.sin(t * 3 + seed)), face, x, g, U * s, tau, seed=seed)

def s2(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    tm = wt.get('METÀ', 1.6); tc = wt.get('COACH', L - .8)
    calendar(ctx, 60, 520, 30, eback(prog(tau, 0, .3)), w=240, h=260, head='FINE MESE')
    floor(ctx, G)
    A = fig(ctx, 'pt', typing, dict(eyes='open', mouth='flat', brows='worried', look=(1, -.2)), 210, tau, fx=.4, seed=1, U_=U * .8)
    spots = [(560, 1040), (740, 1040), (920, 1040), (560, 1540), (740, 1540), (920, 1540)]
    for i, (x, g) in enumerate(spots):
        hit = i % 2 == 0
        poly(ctx, [(x - 80, g), (x + 80, g)], 5, INK, .5)
        mini(ctx, x, g, dict(eyes='open', mouth='flat' if hit else 'smile', brows='worried' if hit and tau > tm + .3 else 'neutral'), tau, 10 + i)
        if hit:
            t0 = tm - .4 + i * .12; k = prog(tau, t0, t0 + .45)
            if 0 < k < 1:
                p = np.array(A['hR']) + (np.array([x, g - 280]) - np.array(A['hR'])) * eio(k)
                bubble(ctx, p[0], p[1], 110, 70, '€?', .8, (-1, 1), (.86, .95, .84), INK, 34, FONT)
            if k >= 1: bubble(ctx, x + 40, g - 300, 100, 64, '€?', .75, (-1, 1), (.86, .95, .84), INK, 32, FONT)
    if tau > tc - .1:
        whistle(ctx, A['head'] + np.array([20, 150]), 1.0 * eback(prog(tau, tc - .1, tc + .2)))
        xmark(ctx, A['head'] + np.array([20, 150]), .9 * eback(prog(tau, tc + .2, tc + .5)))

def s3(ctx, tau, L, wt):
    cam(ctx, 1.03, 540, 1000)
    floor(ctx, G)
    te = wt.get('ESATTORE', .4)
    A = fig(ctx, 'pt', lambda t: P(t=-3, h=-6, ra1=60, ra2=20, la1=-14, la2=-8), dict(eyes='open', mouth='smirk', brows='angry', look=(1, 0)), 330, tau, fx=.3, seed=1)
    collector_cap(ctx, A['head'], .46 * U, prog(tau, 0, .35))
    money_bag(ctx, A['hR'] + np.array([20, 70]), .9 * eback(prog(tau, te, te + .3)))
    B = fig(ctx, 'client', lambda t: P(t=4, h=8, la1=-20, la2=-10, ra1=20, ra2=10), dict(eyes='open', mouth='frown', brows='angry', look=(-1, 0)), 820, tau, fx=-.4, seed=2)
    shake_lines(ctx, B['head'] + np.array([90, 0]), 1, prog(tau, te, te + .3))

def s4(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    floor(ctx, G)
    tr = wt.get('RAPPORTO', L - .8)
    fr = eio(prog(tau, .1, tr + .3))
    A = fig(ctx, 'pt', lambda t: P(ra1=80, ra2=85), dict(eyes='open', mouth='flat', brows='worried', look=(1, 0)), 250, tau, fx=.3, seed=1, U_=U * .85)
    B = fig(ctx, 'client', lambda t: P(la1=-80 + 10 * fr, la2=-85), dict(eyes='open', mouth='frown' if fr > .5 else 'flat', brows='worried', look=(-1, 0)), 830 + 40 * fr, tau, fx=-.3, seed=2, U_=U * .85)
    rope(ctx, A['hR'], B['hL'], fr, tau)
    for i in range(3):
        t0 = .2 + i * .45; k = prog(tau, t0, t0 + .3)
        if k > 0: bubble(ctx, 380 + i * 150, 760 - i * 60, 120, 70, '€?', eback(k) * .85, (-1, 1), (.86, .95, .84), INK, 34, FONT)

def s5(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    floor(ctx, G)
    ts = wt.get('SEPARARE', .6)
    sp = eio(prog(tau, ts - .1, ts + .6))
    face = dict(eyes='open', mouth='grin', brows='raised')
    if sp < .02:
        fig(ctx, 'pt', lambda t: P(t=0, h=6 * math.sin(t * 4)), dict(eyes='open', mouth='flat', brows='raised', look=(0, -.5)), 540, tau, seed=1)
    else:
        A = fig(ctx, 'pt', lambda t: P(ra1=120, ra2=150), face, lerp(540, 280, sp), tau, fx=.2, seed=1, U_=U * .9)
        B = fig(ctx, 'pt', lambda t: P(la1=-60, la2=-80), dict(face, mouth='smile'), lerp(540, 800, sp), tau, fx=-.2, seed=3, U_=U * .9)
        whistle(ctx, A['hR'], 1.0 * sp)
        register(ctx, B['hL'] + np.array([-60, 100]), .8 * sp)
        plate_label(ctx, (280, 640), 'COACH', eback(prog(tau, ts + .4, ts + .7)), bg=GREEN, tc=WHITE, size=50)
        plate_label(ctx, (800, 640), 'PAGAMENTI', eback(prog(tau, ts + .6, ts + .9)), bg=RED, tc=WHITE, size=50)
        poly(ctx, [(540, 700), (540, 1500)], 6, INK, .3 * sp)

def s6(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    tf = wt.get('FISSE', .3); td = wt.get('DATA', 1.2); tp = wt.get('PRIMO', L - 1)
    circ = [1, 15, 29]
    ck = [prog(tau, tf + i * .25, tf + .3 + i * .25) for i in range(3)]
    month_card(ctx, 160, 470, 760, circ, eback(prog(tau, 0, .3)), 'OTTOBRE', ck)
    for i, d in enumerate(circ):
        k = prog(tau, td + i * .15, td + .3 + i * .15)
        status_chip(ctx, 160 + [240, 760, 470][i], 470 + [340, 520, 830][i] - 0, f'RATA {i + 1}', RED, k, 26)
    floor(ctx, G)
    sh = prog(tau, tp - .2, tp + .2)
    hand = 6 * math.sin(tau * 18) * sh
    fig(ctx, 'pt', lambda t: P(ra1=lerp(14, 72, sh), ra2=lerp(8, 80, sh) + hand), dict(eyes='happy' if sh > .5 else 'open', mouth='grin', brows='raised'), 400, tau, fx=.3, seed=1, U_=U * .55)
    fig(ctx, 'client', lambda t: P(la1=lerp(-14, -72, sh), la2=lerp(-8, -80, sh) + hand), dict(eyes='happy' if sh > .5 else 'open', mouth='grin', brows='raised'), 680, tau, fx=-.3, seed=2, U_=U * .55)

def s7(ctx, tau, L, wt):
    cam(ctx, 1.02, 540, 1000)
    floor(ctx, G)
    tm = wt.get('MAI', 1.2)
    A = fig(ctx, 'client', curl(1.3), dict(eyes='happy', mouth='grin', brows='raised'), 330, tau, fx=.2, seed=2)
    hold_dumbbell(ctx, A)
    fig(ctx, 'pt', lambda t: P(ra1=130 + 15 * math.sin(t * 6), ra2=160, la1=-130 - 15 * math.sin(t * 6 + 1), la2=-160), dict(eyes='happy', mouth='grin', brows='raised'), 780, tau, fx=-.3, seed=1)
    k = eback(prog(tau, tm - .3, tm))
    bubble(ctx, 560, 640, 240, 200, '', k, (1, 1))
    if k > 0:
        ctx.save(); ctx.translate(560, 640); sscale(ctx, k); euro_crossed(ctx, (0, 0), .9); ctx.restore()

def s8(ctx, tau, L, wt):
    ts = wt.get('STRIPE', 1.0); ta = wt.get("DALL'APP", L - 1)
    up = eout(prog(tau, 0, .35))
    paid = [prog(tau, ta - .6 + i * .3, ta - .3 + i * .3) for i in range(2)]
    phone(ctx, 540, lerp(2600, 1150, up), 640, 1180, payments_screen(prog(tau, ts, ts + 1.2), paid))
    if tau > ts:
        sparkle(ctx, 870, 700, .8, prog(tau, ts, ts + .3), tau * 3)

def s9(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    tr = wt.get('RATE', .4)
    floor(ctx, G)
    msgs = [MSG, ('Fatto! Pagato da iki', 'l', WHITE, INK)]
    phone(ctx, 380, 1140, 420, 760, chat_screen(msgs, 1 + prog(tau, .3, .8), 'Marco'))
    A = fig(ctx, 'pt', lambda t: P(t=-3, ra1=150 + 10 * math.sin(t * 5), ra2=175), dict(eyes='happy', mouth='grin', brows='raised'), 820, tau, fx=-.3, seed=1, U_=U * .8)
    cta_card(ctx, 'RATE', prog(tau, tr - .3, tr + .1), 640, tau)

SCENES = dict(s1=s1, s2=s2, s3=s3, s4=s4, s5=s5, s6=s6, s7=s7, s8=s8, s9=s9)

def SFX(fx, at):
    for i in range(5): fx('msg', at('s1', None, .15 + i * .32), .22)
    fx('whoosh', at('s1', None, .3), .3)
    for i in range(3): fx('pop', at('s2', 'METÀ', -.1 + i * .24), .25, f=1000 + i * 120)
    fx('zing', at('s2', 'COACH', .2), .15)
    fx('thud', at('s3', None, .3), .4); fx('ding', at('s3', 'ESATTORE', .1), .25, f=1700)
    for i in range(3): fx('pop', at('s4', None, .2 + i * .45), .2, f=900)
    fx('sad', at('s4', 'RAPPORTO'), .15)
    fx('whoosh', at('s5', 'SEPARARE'), .35); fx('pop', at('s5', 'SEPARARE', .45), .3); fx('ding', at('s5', 'SEPARARE', .65), .25)
    for i in range(3): fx('pop', at('s6', 'FISSE', i * .25), .25, f=1100 + i * 100)
    fx('clap', at('s6', 'PRIMO'), .3)
    fx('boing', at('s7', 'MAI', -.2), .25)
    fx('whoosh', at('s8', None), .35); fx('chime', at('s8', 'STRIPE', .1), .25)
    fx('ding', at('s8', "DALL'APP", -.5), .25); fx('ding', at('s8', "DALL'APP", -.2), .25, f=1560)
    fx('msg', at('s9', None, .35), .3); fx('pop', at('s9', 'RATE', -.2), .35, f=800)

if __name__ == '__main__':
    main(sys.modules[__name__], '15')
