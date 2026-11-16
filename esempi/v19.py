from props3 import *

TITLE = 'Recupero 90 secondi'
HOOK = 'RECUPERO 90 SECONDI.\nNE PASSANO 4 MINUTI.'
HOOK_MIN = 2.4
LOOP = True; TAIL = 1.1
NONSPEECH = []
SIL = [-32, .1]
SENT = [
    ("Recupero novanta secondi.", 's1', {'NOVANTA'}, 0.1),
    ("Il cliente guarda il telefono, chiacchiera… e riparte dopo quattro minuti!", 's2', {'QUATTRO', 'MINUTI'}, 0.1),
    ("O dopo trenta secondi.", 's3', {'TRENTA'}, 0.1),
    ("Il recupero è una variabile, come carico e ripetizioni.", 's4', {'VARIABILE'}, 0.1),
    ("Sui multiarticolari pesanti, due o tre minuti.", 's5', {'MULTIARTICOLARI'}, 0.1),
    ("Sugli esercizi di isolamento, sessanta, novanta secondi.", 's6', {'ISOLAMENTO'}, 0.1),
    ("Con iki il recupero lo imposti tu nella scheda!", 's7', {'SCHEDA'}, 0.1),
    ("Il cliente avvia il timer, e quando è ora di ripartire, il telefono suona e vibra.", 's8', {'VIBRA', 'SUONA'}, 0.1),
    ("Scrivi «timer» nei commenti, e ti mando come funziona.", 's9', {'TIMER'}, 0.0),
]
SEAT = G - 150

def bench(ctx, x, w=420):
    rrect(ctx, x - w / 2, SEAT, w, 36, 12); fill_stroke(ctx, (.35, .36, .42), 7)
    for sx in (-1, 1): poly(ctx, [(x + sx * (w / 2 - 40), SEAT + 36), (x + sx * (w / 2 - 40), G)], 14, DARK)

def sitting(arms=None, face_dir=1):
    def pose(t):
        p = P(t=-4 * face_dir, h=6 * math.sin(t * 2), ll1=-82 * face_dir, ll2=-4 * face_dir, rl1=-78 * face_dir, rl2=2 * face_dir)
        if arms: p.update(arms(t))
        return p
    return pose

def sit_fig(ctx, kind, pose, face, x, tau, seed, fx=0.0, band=True, s=1.0):
    p = pose(tau); A = placed(kind, p, x, U_=U * s)
    hip_y = A['hip'][1]
    return draw_anim(ctx, kind, pose, face, x, G - (hip_y - SEAT) + 4 - (G - max(A['fL'][1], A['fR'][1]) - .075 * U * s) * 0, U * s, tau, fx=fx, seed=seed, band=band)

def wall_clock(ctx, c, r, ang, label, k=1.0, lc=RED):
    clock(ctx, c, r, ang)
    if label: plate_label(ctx, (c[0], c[1] + r + 55), label, k, bg=lc, tc=WHITE, size=46)

def phone_arms(t):
    return dict(la1=-30, la2=118, ra1=30, ra2=-118 + 6 * math.sin(t * 30))

def talk_arms(t):
    return dict(la1=-60 + 20 * math.sin(t * 6), la2=-130 + 25 * math.sin(t * 7), ra1=20, ra2=10)

def scene_bench(ctx, tau, phone_on=False, client_face=None):
    floor(ctx, G)
    bench(ctx, 500, 640)
    # amico che chiacchiera (senza fascia)
    sit_fig(ctx, 'client', sitting(talk_arms, -1), dict(eyes='open', mouth='grin' if (tau * 3) % 1 < .5 else 'o', brows='raised', look=(-1, 0)), 690, tau, 7, fx=-.5, band=False)
    A = sit_fig(ctx, 'client', sitting(phone_arms if phone_on else None, 1), client_face or dict(eyes='happy', mouth='grin', brows='raised', look=(1, 0)), 330, tau, 2, fx=.5)
    if phone_on:
        hc = (A['hL'] + A['hR']) / 2; rrect(ctx, hc[0] - 26, hc[1] - 50, 52, 90, 10); fill_stroke(ctx, DARK, 5)
    return A

def s1(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    scene_bench(ctx, tau)
    bubble(ctx, 760, 930, 200, 90, 'bla bla', eback(prog(tau, .2, .45)), (-1, 1), WHITE, INK, 34)
    wall_clock(ctx, (820, 650), 120, tau * 14, '90 s', eback(prog(tau, .1, .4)), GREEN)

def s2(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    tq = wt.get('QUATTRO', L - 1)
    A = scene_bench(ctx, tau, True, dict(eyes='open', mouth='smile', brows='raised', look=(0, .7)))
    bubble(ctx, 760, 930, 200, 90, 'bla bla', 1, (-1, 1), WHITE, INK, 34)
    ang = tau * 22
    wall_clock(ctx, (820, 650), 120, ang, '4:00' if tau > tq else f'{int(1.5 + 2.5 * clamp(tau / tq))}:{int((tau * 37) % 60):02d}', 1, RED if tau > tq else INK)
    if tau > tq: burst(ctx, (820, 650), 140, 190, 12, 7, 1 - prog(tau, tq + .3, tq + .8), RED)

def s3(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    tt = wt.get('TRENTA', .5)
    floor(ctx, G)
    bench(ctx, 260, 360)
    run = eout(prog(tau, .05, .6))
    x = lerp(260, 660, run)
    if run < 1:
        fig(ctx, 'client', lambda t: walk(t * 2 * math.pi * 3, 1, .1, 1.6), dict(eyes='wide', mouth='shout', brows='worried'), x, tau, fx=.6, seed=2, U_=U * .85)
    else:
        ctx.save(); ctx.translate(660, G); sscale(ctx, .85); ctx.translate(-660, -G)
        squat_with_bar(ctx, squat_bar(1.6, .7), dict(eyes='wince', mouth='shout', brows='worried'), 660, tau, plates=.9, seed=2, shake=math.sin(tau * 40) * 4)
        ctx.restore()
    wall_clock(ctx, (820, 650), 110, tau * 3, '0:30', eback(prog(tau, tt - .2, tt + .1)), RED)

def s4(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    tv = wt.get('VARIABILE', 1.0)
    rv = .3 + .5 * eio(prog(tau, tv - .2, tv + .5)) + .05 * math.sin(tau * 3)
    mixer(ctx, 110, 660, ['CARICO', 'RIPETIZIONI', 'RECUPERO'], [.7 + .03 * math.sin(tau * 2), .55, rv], hl=2 if tau > tv - .2 else -1)
    floor(ctx, G)
    fig(ctx, 'pt', lambda t: P(t=0, ra1=150, ra2=170 + 8 * math.sin(t * 4)), dict(eyes='open', mouth='grin', brows='raised', look=(.6, -.7)), 820, tau, fx=-.2, seed=1, U_=U * .6)

def s5(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    tm = wt.get('MULTIARTICOLARI', .4)
    floor(ctx, G)
    ctx.save(); ctx.translate(360, G); sscale(ctx, .95); ctx.translate(-360, -G)
    squat_with_bar(ctx, squat_bar(.45, .9), dict(eyes='wince', mouth='shout', brows='angry'), 360, tau, plates=1.0, seed=2, shake=math.sin(tau * 40) * 3)
    ctx.restore()
    wall_clock(ctx, (830, 760), 120, tau * 2, '2-3 MIN', eback(prog(tau, tm + .2, tm + .5)), GREEN)
    plate_label(ctx, (360, 640), 'PESANTE', eback(prog(tau, tm - .1, tm + .2)), bg=INK, tc=WHITE, size=46)

def s6(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    ti = wt.get('ISOLAMENTO', .5)
    floor(ctx, G)
    A = fig(ctx, 'client', curl(1.2), dict(eyes='open', mouth='grin', brows='raised'), 360, tau, seed=2)
    hold_dumbbell(ctx, A)
    wall_clock(ctx, (830, 760), 120, tau * 4, '60-90 S', eback(prog(tau, ti + .3, ti + .6)), GREEN)
    plate_label(ctx, (360, 640), 'ISOLAMENTO', eback(prog(tau, ti - .1, ti + .2)), bg=INK, tc=WHITE, size=46)

def s7(ctx, tau, L, wt):
    up = eout(prog(tau, 0, .35))
    ts = wt.get('SCHEDA', L - 1)
    phone(ctx, 540, lerp(2600, 1150, up), 640, 1180, rest_setting_screen(prog(tau, ts - .6, ts)))

def s8(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    tv = wt.get('SUONA', L - 1.2)
    frac = clamp(1 - tau / tv)
    secs = int(round(150 * frac)); big = f'{secs // 60}:{secs % 60:02d}'
    done = tau >= tv
    shake = math.sin(tau * 60) * 8 if done else 0
    phone(ctx, 540 + shake, 1100, 600, 1100, timer_screen(frac if not done else 1, 'RECUPERO' if not done else 'RIPARTI!', big if not done else 'VIA!', done))
    if done:
        vibrate_lines(ctx, (540, 1100), 600, 1100, tau)
        bubble(ctx, 820, 560, 240, 110, 'BEEP!', eback(prog(tau, tv, tv + .2)), (-1, 1), YELLOW, INK, 50, FONT)

def s9(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    tt = wt.get('TIMER', .4)
    floor(ctx, G)
    bench(ctx, 400, 520)
    up = eout(prog(tau, .3, .7))
    if up < .05:
        sit_fig(ctx, 'client', sitting(phone_arms, 1), dict(eyes='open', mouth='smile', brows='raised', look=(0, .7)), 330, tau, 2, fx=.5)
    else:
        A = fig(ctx, 'client', lambda t: P(t=0, la1=-30, la2=-40, ra1=150 + 10 * math.sin(t * 6), ra2=170), dict(eyes='happy', mouth='grin', brows='raised'), 330, tau, seed=2)
    bubble(ctx, 720, 1060, 220, 100, 'BEEP!', eback(prog(tau, .2, .4)), (-1, 1), YELLOW, INK, 46, FONT)
    sit_fig(ctx, 'client', sitting(talk_arms, -1), dict(eyes='wide', mouth='o', brows='raised', look=(-1, 0)), 560, tau, 7, fx=-.5, band=False)
    cta_card(ctx, 'TIMER', prog(tau, tt - .3, tt + .1), 640, tau)

SCENES = dict(s1=s1, s2=s2, s3=s3, s4=s4, s5=s5, s6=s6, s7=s7, s8=s8, s9=s9)

def SFX(fx, at):
    for i in range(10): fx('tick', at('s1', None, .1 + i * .15), .25)
    for i in range(14): fx('tick', at('s2', None, .1 + i * .2), .2)
    fx('boing', at('s2', 'QUATTRO'), .3); fx('ding', at('s2', 'MINUTI', .1), .3, f=1100)
    fx('whoosh', at('s3', None, .05), .35); fx('thud', at('s3', 'TRENTA', .2), .4)
    fx('swoosh_up', at('s4', 'VARIABILE', -.2), .3); fx('pop', at('s4', 'VARIABILE', .3), .25)
    fx('thud', at('s5', None, .3), .4); fx('pop', at('s5', 'MULTIARTICOLARI', .3), .3)
    fx('pop', at('s6', 'ISOLAMENTO', .3), .3, f=1200)
    fx('whoosh', at('s7', None), .35); fx('ding', at('s7', 'SCHEDA', -.1), .3)
    for i in range(6): fx('tick', at('s8', None, .3 + i * .4), .25)
    fx('msg', at('s8', 'SUONA'), .4); fx('msg', at('s8', 'SUONA', .35), .4); fx('zing', at('s8', 'VIBRA'), .12)
    fx('msg', at('s9', None, .2), .35); fx('pop', at('s9', 'TIMER', -.2), .35, f=800)

if __name__ == '__main__':
    main(sys.modules[__name__], '19')
