"""Il PT. Un documentario — puntata 01: il richiamo notturno.
Serie della domenica: documentario naturalistico sussurrato sul personal trainer nel suo habitat."""
from props4 import *

TITLE = 'Documentario 01 - Il richiamo notturno'
HOOK = "L'ERRORE\nDELLE 23:47"
LOOP = False; TAIL = 1.4
SENT = [
    ("Eccolo: il personal trainer, nel suo habitat, alle ventitré e quarantasette.", 's1', {'HABITAT', 'QUARANTASETTE'}, 0.15),
    ("Sta per commettere l'errore più grave della sua giornata.", 's2', {'ERRORE', 'GRAVE'}, 0.2),
    ("Risponde. In quattro secondi.", 's3', {'RISPONDE', 'QUATTRO'}, 0.2),
    ("Ora il branco ha capito: il richiamo funziona a qualsiasi ora.", 's4', {'BRANCO', 'QUALSIASI'}, 0.25),
    ("Ma alcuni esemplari si sono evoluti.", 's5', {'EVOLUTI'}, 0.15),
    ("Le chat dei clienti stanno in iki, fuori da WhatsApp. E con Non disturbare, le notifiche aspettano il mattino.", 's6', {'IKI', 'WHATSAPP', 'DISTURBARE', 'MATTINO'}, 0.15),
    ("Il personal trainer evoluto dorme. E il cliente, al mattino, ha la sua risposta.", 's7', {'DORME', 'RISPOSTA'}, 0.2),
    ("La natura è crudele.", 's8', {'CRUDELE'}, 1.5),
    ("Sì. Scusate.", 's9', set(), 0.0),
]

GRASS = (.42, .62, .30); GRASS2 = (.30, .50, .24)

# ---------------------------------------------------------------- oggetti del documentario
def night(ctx, k=1.0):
    """Notte: velo blu sulla carta, più scuro ai bordi."""
    if k <= 0: return
    col(ctx, NIGHT, .42 * k); ctx.paint()
    g = cairo.RadialGradient(540, 1000, 300, 540, 1000, 1100)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, .02, .03, .08, .55 * k)
    ctx.set_source(g); ctx.paint()

def grass(ctx, x0, x1, g, t, h=170, n=14, seed=0, c=GRASS):
    """Ciuffi d'erba alta che ondeggiano (in primo piano: si disegnano dopo le figure)."""
    rnd = np.random.default_rng(seed)
    for i in range(n):
        x = lerp(x0, x1, (i + rnd.uniform(.1, .9)) / n); hh = h * rnd.uniform(.65, 1.15)
        sw = 18 * math.sin(t * 1.6 + i * .9 + seed)
        ctx.move_to(x - 22, g + 10)
        ctx.curve_to(x - 10, g - hh * .5, x + sw * .5, g - hh * .8, x + sw, g - hh)
        ctx.curve_to(x + 4 + sw * .4, g - hh * .6, x + 14, g - hh * .3, x + 22, g + 10)
        ctx.close_path(); fill_stroke(ctx, c if i % 2 else GRASS2, 5)

def species_card(ctx, k, name, latin, y=1430):
    """Sottopancia da documentario: nome della specie + nome latino."""
    if k <= 0: return
    kk = eout(clamp(k)); x = lerp(-700, 70, kk)
    ctx.save()
    rrect(ctx, x + 8, y + 10, 700, 150, 18); col(ctx, INK, .25); ctx.fill()
    rrect(ctx, x, y, 700, 150, 18); fill_stroke(ctx, WHITE, 6)
    ctx.rectangle(x, y, 22, 150); col(ctx, RED); ctx.fill()
    text(ctx, name, x + 50, y + 55, 46, FONT, INK, anchor='l')
    text(ctx, latin, x + 50, y + 108, 34, FONTB, GRAY, anchor='l')
    ctx.restore()

def binocular(ctx, k=1.0, cx=540, cy=1000, r=330):
    """Vista nel binocolo: nero tutto intorno a due cerchi."""
    if k <= 0: return
    ctx.push_group()
    col(ctx, (.03, .03, .05), .96 * k); ctx.paint()
    ctx.set_operator(cairo.OPERATOR_CLEAR)
    for s in (-1, 1): ctx.arc(cx + s * r * .55, cy, r, 0, 2 * math.pi); ctx.fill()
    ctx.set_operator(cairo.OPERATOR_OVER)
    ctx.pop_group_to_source(); ctx.paint()
    poly(ctx, [(cx - 40, cy), (cx + 40, cy)], 3, WHITE, .5 * k); poly(ctx, [(cx, cy - 40), (cx, cy + 40)], 3, WHITE, .5 * k)

def pt_phone(ctx, tau, x, face, glow=0.0, s=.95, tilt=0, head=-4, g=None, typing=0.0):
    """PT con il telefono in mano davanti al petto."""
    sh = 10 * typing * math.sin(tau * 40)
    A = fig(ctx, 'pt', lambda t: P(t=tilt, h=head, ra1=35 + sh, ra2=150 - sh, la1=-25 - sh, la2=120 + sh),
            face, x, tau, fx=.1, seed=1, U_=U * s, g=g)
    small_phone(ctx, A['hR'] + np.array([0, -30 * s]), rot=.15, glow=glow, s=1.1 * s)
    return A

def msg(ctx, c, lines, k, w=440, size=34, fillc=WHITE, ora=None):
    """Fumetto di chat (messaggio del cliente)."""
    if k <= 0: return
    h = 50 + 46 * len(lines) + (26 if ora else 0)
    ctx.save(); ctx.translate(*c); sscale(ctx, eback(clamp(k)))
    rrect(ctx, -w / 2 + 8, -h / 2 + 10, w, h, 30); col(ctx, INK, .18); ctx.fill()
    rrect(ctx, -w / 2, -h / 2, w, h, 30); fill_stroke(ctx, fillc, 6)
    for j, l in enumerate(lines): text(ctx, l, -w / 2 + 34, -h / 2 + 50 + j * 46, size, FONTB, INK, anchor='l')
    if ora: text(ctx, ora, w / 2 - 26, h / 2 - 26, 24, FONT, RED, anchor='r')
    ctx.restore()

# ---------------------------------------------------------------- scene
def s1(ctx, tau, L, wt):
    cam(ctx, 1.04, 540, 1040)
    night(ctx)
    th = wt.get('HABITAT', L * .4)
    night_window(ctx, 640, 600, 300, 280, tau)
    floor(ctx, G)
    pt_phone(ctx, tau, 380, dict(eyes='tired', mouth='flat', brows='neutral', look=(.4, -.4)), glow=.8 + .2 * math.sin(tau * 5), s=1.2)
    digital_clock(ctx, (800, 1080), '23:47', .8, glow=.4)
    grass(ctx, 30, 1050, G + 30, tau, h=230, n=16, seed=1)
    species_card(ctx, prog(tau, 0, .35), 'PERSONAL TRAINER', 'Homo sapiens')

def s2(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    night(ctx)
    te = wt.get("L'ERRORE", wt.get('ERRORE', L * .5))
    tz = te - .1                                   # circa al secondo 7: zoom sul telefono
    z = eio(prog(tau, tz, tz + .45))
    px, py = 540, 975                             # telefono in mano al PT (coordinate a schermo)
    ctx.save(); ctx.translate(px, py); sscale(ctx, 1 + 3.5 * z); ctx.translate(-px, -py)
    ctx.translate(540, 1000); sscale(ctx, 1.25 + .05 * tau / max(L, .1)); ctx.translate(-540, -1000)
    floor(ctx, G - 80)
    pt_phone(ctx, tau, 380, dict(eyes='open', mouth='flat', brows='raised', look=(.5, -.4)), glow=1, g=G - 80)
    v = math.sin(tau * 50) * 5 * (tau > .3)
    msg(ctx, (650 + v, 880), ['Domani possiamo', 'spostare alle 6?'], prog(tau, .2, .5) * max(0, 1 - 4 * z), w=400, size=30, ora='23:47')
    grass(ctx, 80, 1000, G - 40, tau, h=200, n=12, seed=2)
    ctx.restore()
    binocular(ctx, eout(prog(tau, 0, .3)) * (1 - z))
    if z > 0:
        k = eout(prog(tau, tz + .15, tz + .55))
        if k > 0:
            col(ctx, (.03, .03, .05), .85 * k); ctx.paint()
            ctx.save(); ctx.translate(lerp(px, 540, k), lerp(py, 1180, k)); sscale(ctx, lerp(.12, 1, k))
            shake = math.sin(tau * 60) * 4 * (1 - prog(tau, tz + .6, tz + 1.2))
            phone(ctx, shake, 0, 640, 1120, wa_screen([('Domani possiamo\nspostare alle 6?', 'l')], 1, title='CLIENTE', time='23:47'))
            ctx.restore()
    if tau > te + .3:
        plate_label(ctx, (540, 530), 'ERRORE IN CORSO', eback(prog(tau, te + .3, te + .6)) * (1 if int(tau * 4) % 2 else .85), bg=RED, tc=WHITE, size=40)

def s3(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    night(ctx)
    tq = wt.get('QUATTRO', L * .6); tr = wt.get('RISPONDE', .1)
    floor(ctx, G)
    typing = 1 - prog(tau, tq + .1, tq + .3)
    pt_phone(ctx, tau, 330, dict(eyes='wide', mouth='grin', brows='raised', look=(.5, -.5)), glow=1, typing=typing)
    secs = min(4, int(4 * clamp((tau - tr) / max(tq - tr, .3)) + .001))
    stopwatch_big(ctx, (800, 720), 110, f'0:0{secs}', tau * 9)
    msg(ctx, (760, 1060), ['Domani alle 6?'], 1, w=340, size=32)
    if tau > tq:
        msg(ctx, (650, 1220), ['Certo!! Nessun', 'problema 💪'.replace(' 💪', '')], prog(tau, tq, tq + .25), w=400, size=32, fillc=(1, .86, .84), ora='23:47')
        check(ctx, (880, 1270), .35 * eback(prog(tau, tq + .2, tq + .4)))
    grass(ctx, 20, 1060, G + 30, tau, h=150, n=16, seed=3)

def s4(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    night(ctx)
    tb = wt.get('BRANCO', .4); tq = wt.get('QUALSIASI', L * .7)
    floor(ctx, G)
    grass(ctx, 20, 1060, G - 330, tau, h=150, n=14, seed=7, c=GRASS2)
    heads = ((170, '00:12', ['Posso mangiare', 'la pizza?'], tb - .2), (450, '01:30', ['Non riesco', 'a dormire'], tb + .25),
             (910, '06:02', ['Sono in', 'ritardo!'], tq - .3))
    for i, (x, ora, lines, t0) in enumerate(heads):
        up = eback(prog(tau, t0 - .25, t0 + .1))
        if up <= 0: continue
        bob = 6 * math.sin(tau * 4 + i)
        fig(ctx, 'client', lambda t: P(t=0, h=6 * math.sin(t * 3 + i)), dict(eyes='wide', mouth='o', brows='raised', look=(0, -.4)),
            x, tau, seed=3 + i, U_=U * .6, g=G - 230 + 260 * (1 - up) + bob)
    grass(ctx, 20, 1060, G - 180, tau, h=210, n=15, seed=8)
    for i, (x, ora, lines, t0) in enumerate(heads):
        k = prog(tau, t0, t0 + .25)
        msg(ctx, (x if i != 0 else 260, 640 + (i % 2) * 150), lines, k, w=320, size=28, ora=ora)
    pt_phone(ctx, tau, 690, dict(eyes='wide', mouth='o', brows='worried', look=(-.3, -.6)), glow=1, s=.8, typing=prog(tau, tq, tq + .2))
    grass(ctx, 20, 1060, G + 40, tau, h=120, n=18, seed=9)

def evo_fig(ctx, tau, x, k, stage):
    """Marcia dell'evoluzione: da curvo sul telefono a dritto e sereno."""
    if k <= 0: return
    tilt = (38, 18, 0)[stage]; head = (25, 12, -2)[stage]
    face = (dict(eyes='tired', mouth='flat', brows='worried', look=(.5, .6)),
            dict(eyes='open', mouth='flat', brows='neutral', look=(.5, .2)),
            dict(eyes='happy', mouth='smile', brows='raised', look=(.3, -.2)))[stage]
    ctx.save(); ctx.translate(x, G); sscale(ctx, eback(k)); ctx.translate(-x, -G)
    ph = tau * 2 * math.pi * 1.1 + stage
    def pose(t, st=stage):
        p = walk(ph, 1, .0, .7)
        p['t'] = tilt; p['h'] = head
        if st < 2: p['ra1'] = 60 - tilt; p['ra2'] = 150 - tilt
        else: p['ra1'] = 25 + 8 * math.sin(ph); p['ra2'] = 15
        return p
    A = fig(ctx, 'pt', pose, face, x, tau, fx=.3, seed=1 + stage, U_=U * (.85 + .1 * stage))
    if stage < 2: small_phone(ctx, A['hR'] + np.array([4, -20]), rot=.6, glow=1, s=.8)
    ctx.restore()

def s5(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    te = wt.get('EVOLUTI', L * .6)
    night(ctx, 1 - prog(tau, te - .3, te + .3) * .6)
    floor(ctx, G)
    for i, x in enumerate((170, 500, 840)):
        evo_fig(ctx, tau, x + 18 * tau, prog(tau, .05 + i * .3, .35 + i * .3), i)
    if tau > te:
        for i in range(4): sparkle(ctx, 840 + 18 * tau + (-120, 130, -90, 110)[i], 760 + (0, 60, 260, 300)[i], .5, 1 - prog(tau, te + .6, te + 1.2), tau * 3 + i)
        halo(ctx, (840 + 18 * tau, 1100), 380, YELLOW, .25 * prog(tau, te, te + .3))
    grass(ctx, 20, 1060, G + 40, tau, h=120, n=18, seed=11)

def seg_toggle(ctx, x, y, on):
    rrect(ctx, x - 34, y - 20, 68, 40, 20); col(ctx, tuple(lerp(a, b, clamp(on)) for a, b in zip((.8, .78, .75), GREEN))); ctx.fill()
    ctx.arc(lerp(x - 14, x + 14, clamp(on)), y, 16, 0, 2 * math.pi); col(ctx, WHITE); ctx.fill()

def notifiche_screen(on, times, hl=0.0):
    """Schermata reale di iki (PT): Impostazioni → Notifiche, gruppo «Silenzio» → Non disturbare."""
    def content(ctx, w, h):
        app_head(ctx, w, 'Notifiche')
        text(ctx, 'I TUOI CLIENTI', 44, 205, 20, FONT, GRAY, anchor='l')
        rrect(ctx, 30, 230, w - 60, 200, 20); fill_stroke(ctx, (.97, .96, .94), 3, (.85, .83, .8))
        for j, (t1, t2) in enumerate((('Messaggi', 'Quando un cliente ti scrive'), ('Allenamenti e record', 'Allenamento chiuso o record battuto'))):
            yy = 275 + j * 100
            text(ctx, t1, 56, yy, 25, FONT, INK, anchor='l'); text(ctx, t2, 56, yy + 36, 18, FONTB, GRAY, anchor='l')
            seg_toggle(ctx, w - 90, yy + 14, 1)
        text(ctx, 'SILENZIO', 44, 485, 20, FONT, RED if hl > 0 else GRAY, anchor='l')
        hh = 150 + 110 * clamp(times)
        if hl > 0:
            rrect(ctx, 22, 505, w - 44, hh + 16, 24); col(ctx, RED, .1 * hl); ctx.fill()
        rrect(ctx, 30, 513, w - 60, hh, 20); fill_stroke(ctx, (.97, .96, .94), 3, (.85, .83, .8))
        text(ctx, 'Non disturbare', 56, 560, 27, FONT, INK, anchor='l')
        if on < .5:
            text(ctx, 'Scegli le ore in cui non vuoi', 56, 600, 18, FONTB, GRAY, anchor='l')
            text(ctx, 'notifiche: arrivano alla fine.', 56, 628, 18, FONTB, GRAY, anchor='l')
        else:
            text(ctx, 'Dalle 22:00 alle 07:30 le notifiche', 56, 600, 18, FONTB, GRAY, anchor='l')
            text(ctx, 'aspettano e arrivano dopo.', 56, 628, 18, FONTB, GRAY, anchor='l')
        seg_toggle(ctx, w - 90, 556, on)
        if times > 0:
            ctx.save(); ctx.translate(0, 0)
            for j, (lab, val) in enumerate((('Dalle', '22:00'), ('alle', '07:30'))):
                x = 56 + j * 250; a = clamp(times * 2 - j)
                if a <= 0: continue
                text(ctx, lab, x, 712, 22, FONTB, GRAY, anchor='l')
                rrect(ctx, x + (70 if j == 0 else 55), 682, 130, 60, 12); fill_stroke(ctx, WHITE, 3, (.8, .78, .75))
                text(ctx, val, x + (135 if j == 0 else 120), 713, 26, FONT, INK)
            ctx.restore()
    return content

def s6(ctx, tau, L, wt):
    up = eout(prog(tau, 0, .35))
    halo(ctx, (540, 1100), 760, RED, .12)
    tw = wt.get('WHATSAPP', L * .3); tn = wt.get('NON', L * .45); td = wt.get('DISTURBARE', L * .5); tm = wt.get('MATTINO', L - .6)
    swap = prog(tau, tn - .45, tn - .1)
    if swap < 1:
        phone(ctx, 540 - 1400 * eio(swap), lerp(2600, 1130, up), 640, 1120, iki_chat_screen(prog(tau, .3, .6) + prog(tau, .7, 1.0), hl=prog(tau, tw - .2, tw + .1)))
    if swap > 0:
        on = prog(tau, td - .1, td + .15); times = prog(tau, td + .2, tm - .2)
        phone(ctx, 540 + 1400 * (1 - eio(swap)), 1130, 640, 1120, notifiche_screen(on, times, hl=prog(tau, tn - .1, tn + .2)))
        status_chip(ctx, 540, 500, 'Le notifiche aspettano il mattino', RED, prog(tau, tm - .3, tm), 32)

def lying_pt(ctx, x_head, y, tau, face, s=.75, seed=1, kind='pt'):
    """Sdraiato a letto, testa a sinistra (come lying_fig di props4)."""
    U_ = U * s
    ctx.save(); ctx.translate(x_head, y); ctx.rotate(math.radians(-90)); ctx.translate(-540, -G + 3.05 * U_)
    A = draw_fig(ctx, kind, P(la1=-10, la2=-6, ra1=10, ra2=6, ll1=0, ll2=0, rl1=0, rl2=0), face, 540, G, U_, tau, seed=seed)
    ctx.restore()
    return A

def s7(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    tm = wt.get('MATTINO', L * .55); tr = wt.get('RISPOSTA', L - .7)
    day = prog(tau, tm - .5, tm + .2)
    night(ctx, 1 - day)
    night_window(ctx, 650, 560, 300, 280, tau, day=day)
    floor(ctx, G)
    bed(ctx, 140, 1210, 760)
    lying_pt(ctx, 260, 1185, tau, dict(eyes='closed' if day < 1 or tau < tr - .5 else 'happy', mouth='smile', brows='neutral'), s=.72, seed=1, kind='pt')
    blanket(ctx, 330, 1150, 540, t=tau, breathe=1)
    if day < .9: zzz(ctx, (330, 1010), tau, 1 - day)
    digital_clock(ctx, (300, 740), '23:52' if day < .5 else '07:30', .75, glow=.3)
    if tau > tr - .5:
        msg(ctx, (620, 900), ['Buongiorno! Ok', 'per le 6 di domani'], prog(tau, tr - .5, tr - .2), w=470, size=32, fillc=(1, .86, .84), ora='07:31')
        check(ctx, (860, 960), .35 * eback(prog(tau, tr - .2, tr)))

def s8(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    tc = wt.get('CRUDELE', .5); tb = tc + 1.3          # stacco: arriva un messaggio al narratore
    if tau < tb:
        floor(ctx, G)
        fig(ctx, 'pt', lambda t: P(t=0, h=3 * math.sin(t * 2), ra1=20, ra2=10, la1=-20, la2=-10),
            dict(eyes='happy', mouth='smile', brows='raised'), 300, tau, fx=.1, seed=1, U_=U * .85)
        fig(ctx, 'pt', lambda t: P(t=30, h=25, ra1=30, ra2=150, la1=-30, la2=-150), dict(eyes='tired', mouth='flat', brows='worried', look=(.3, .6)),
            800, tau, fx=-.1, seed=4, U_=U * .75)
        small_phone(ctx, (870, 1240), rot=.5, glow=1, s=.8)
        grass(ctx, 20, 1060, G + 40, tau, h=170, n=18, seed=13)
        species_card(ctx, prog(tau, tc - .4, tc), 'LA NATURA', 'è crudele.')
    else:
        narrator_phone(ctx, tau - tb, 0)

def narrator_phone(ctx, t, reply):
    """Il telefono del narratore: gli scrive il SUO cliente. Nessuna vibrazione, solo il messaggio."""
    col(ctx, (.03, .03, .05)); ctx.paint()
    k = eout(prog(t, 0, .35))
    ctx.save(); ctx.translate(540, lerp(2400, 1150, k))
    phone(ctx, 0, 0, 640, 1120, wa_screen([('Scusi, possiamo\nspostare il\ndocumentario\nalle 6?', 'l'), ('Sì', 'r')], 1 + reply, title='CLIENTE', time='23:58'))
    ctx.restore()

def studio(ctx, onair=1.0):
    """Lo studio del narratore: luce calda, insegna ON AIR."""
    col(ctx, (.13, .11, .10)); ctx.paint()
    g = cairo.RadialGradient(560, 1150, 60, 560, 1150, 760)
    g.add_color_stop_rgba(0, 1, .93, .80, 1); g.add_color_stop_rgba(.7, .55, .45, .36, 1); g.add_color_stop_rgba(1, .13, .11, .10, 1)
    ctx.set_source(g); ctx.arc(560, 1150, 760, 0, 2 * math.pi); ctx.fill()
    for i in range(7):                                                            # pannelli fonoassorbenti
        x = 40 + i * 150; rrect(ctx, x, 180, 120, 120, 10); col(ctx, (0, 0, 0), .18); ctx.fill()
    rrect(ctx, 70, 470, 250, 90, 14); fill_stroke(ctx, (.85, .1, .1) if onair > .5 else (.3, .12, .12), 6)
    if onair > .5:
        col(ctx, RED, .25); rrect(ctx, 50, 450, 290, 130, 24); ctx.fill()
    text(ctx, 'ON AIR', 195, 517, 50, FONT, WHITE if onair > .5 else (.5, .4, .4))

def boom_mic(ctx, sway=0.0):
    """Microfono da studio su braccio che scende dall'alto a sinistra."""
    poly(ctx, [(-20, 640), (250, 760)], 16); poly(ctx, [(-20, 640), (250, 760)], 8, (.4, .4, .42))
    ctx.save(); ctx.translate(250, 760); ctx.rotate(.5 + sway)
    poly(ctx, [(0, 0), (0, 80)], 8)
    rrect(ctx, -40, 80, 80, 170, 38); fill_stroke(ctx, (.32, .32, .35), 7)
    for i in range(5): poly(ctx, [(-28, 110 + i * 26), (28, 110 + i * 26)], 3, (.15, .15, .15))
    ctx.restore()

def narrator(ctx, t, ts, tsc):
    """Il narratore (host.py) in studio: compiaciuto, due colpi di tosse, «Scusate», scappa."""
    from host import draw_host
    c1 = (ts + 1.30, ts + 1.80); c2 = (ts + 2.00, ts + 2.45)
    cough = (c1[0] < t < c1[1]) or (c2[0] < t < c2[1])
    run = prog(t, tsc + .8, tsc + 1.3)
    studio(ctx, onair=0 if run > .2 else 1)
    if run > 0:
        mood = 'panic'
    elif t >= tsc - .15:
        mood = 'sorry'
    elif cough:
        mood = 'cough'
    elif t > ts + 1.3:
        mood = 'sorry'
    else:
        mood = 'smug'
    jolt = math.sin(t * 55) * 10 if cough else 0
    x = 560 + eio(run) * 1100
    draw_host(ctx, t, mood, x=x, lean=.25 * run, jolt=jolt, sweat=prog(t, tsc - .15, tsc + .1))
    if run > 0:                                                                   # linee di velocità
        for i in range(5):
            y = 800 + i * 160; poly(ctx, [(x - 420 - i * 40, y), (x - 650 - i * 40, y)], 8, INK, .5 * (1 - run))
    sway = .25 * math.sin((t - tsc - .9) * 10) * math.exp(-max(0, t - tsc - .9) * 2.5) if t > tsc + .9 else 0
    boom_mic(ctx, sway)
    species_card(ctx, prog(t, ts + .5, ts + .8) * (1 - prog(t, tsc + .6, tsc + .9)), 'IL NARRATORE', 'Homo sapiens televisivus', y=1580)

def s9(ctx, tau, L, wt):
    ts = wt.get('SÌ', .1); tsc = wt.get('SCUSATE', L - .8)
    reply = prog(tau, ts - .15, ts + .05)                # il «Sì» lo scrive soltanto
    if tau < ts + .35:
        narrator_phone(ctx, 3 + tau, reply)
    elif tau < tsc + 1.6:
        narrator(ctx, tau, ts, tsc)
    else:
        col(ctx, (0, 0, 0)); ctx.paint()                # fine

# ---------------------------------------------------------------- colonna sonora da documentario
import engine as _eng
_rng2 = np.random.default_rng(7)
def _t(d): return np.arange(int(d * SR)) / SR
def _mtof(m): return 440 * 2 ** ((m - 69) / 12)

def _pluck(m, d=.45):
    t = _t(d); f = _mtof(m)
    return (np.sin(2 * np.pi * f * t) + .45 * np.sin(4 * np.pi * f * t) * np.exp(-t * 18) + .2 * np.sin(6 * np.pi * f * t) * np.exp(-t * 30)) * np.exp(-t * 9) * np.minimum(1, t * 400)

def _pad(ms, d):
    t = _t(d); s = np.zeros(len(t))
    for m in ms:
        for det in (-.12, 0, .12):
            f = _mtof(m) * 2 ** (det / 12); ph = 2 * np.pi * f * t + _rng2.uniform(0, 6)
            s += np.sin(ph) + .3 * np.sin(2 * ph) + .12 * np.sin(3 * ph)
    env = np.minimum(1, t / 1.2) * np.minimum(1, (d - t) / 1.0)
    return _eng._lp(s, 1400) * env / (3 * len(ms))

def doc_music(N, total):
    """Documentario naturalistico: archi gravi in Re minore + pizzicato «in punta di piedi»."""
    L = np.zeros(N); R = np.zeros(N)
    def add(sig, t, g=1.0, pan=0.0):
        i = int(t * SR); sig = sig[: max(0, N - i)]
        L[i:i + len(sig)] += sig * g * (1 - max(0, pan)); R[i:i + len(sig)] += sig * g * (1 + min(0, pan))
    beat = 60 / 76; bar = 4 * beat
    chords = [[38, 50, 53, 57], [34, 46, 50, 53], [41, 48, 53, 57], [33, 45, 49, 52]]   # Rem, Sib, Fa, La
    motif = [(0, 62), (.5, 65), (1, 69), (2, 67), (2.5, 65), (3, 64)]
    motif2 = [(0, 62), (1, 61), (1.5, 62), (2, 57), (3, 62)]
    for b in range(int(total / bar) + 2):
        t0 = b * bar; ch = chords[b % 4]
        add(_pad(ch, bar + 1.0), t0, .55)
        mot = motif if b % 2 == 0 else motif2
        tr = (0, -2, 3, -5)[b % 4] if b % 4 else 0
        for off, m in mot: add(_pluck(m + tr), t0 + off * beat, .32, .25 if m % 2 else -.25)
        if b % 4 == 0: add(_eng.SYNTH['timp'](), t0, .5)
    fade = np.ones(N); n1 = int(.6 * SR); fade[:n1] = np.linspace(0, 1, n1)
    fo = int((total - 1.0) * SR); fe = int(total * SR); fade[fo:fe] = np.linspace(1, 0, fe - fo); fade[fe:] = 0
    return L * fade * .45, R * fade * .45

def _crickets(f=None):
    d = f or 6.0; t = _t(d); s = np.zeros(len(t))
    for k, (fc, rate, ph) in enumerate(((4300, 2.1, 0), (4700, 1.7, .5), (3900, 2.6, .9))):
        gate = (np.sin(2 * np.pi * rate * t + ph) > .55).astype(float)
        trill = .5 + .5 * np.sign(np.sin(2 * np.pi * 32 * t))
        s += np.sin(2 * np.pi * fc * t) * _eng._lp(gate * trill, 300) * (.6 + .4 * np.sin(t * .7 + k))
    env = np.minimum(1, t / .8) * np.minimum(1, (d - t) / .8)
    return s * env * .35

def _birds(f=None):
    d = f or 3.0; out = np.zeros(int(d * SR))
    for k in range(9):
        st = _rng2.uniform(0, d - .4); n = int(_rng2.uniform(.08, .18) * SR); tt = np.arange(n) / SR
        f0 = _rng2.uniform(2800, 4200); sweep = f0 + _rng2.uniform(-900, 1200) * tt / tt[-1]
        sig = np.sin(2 * np.pi * np.cumsum(sweep) / SR) * np.sin(np.pi * tt / tt[-1]) ** 2
        i = int(st * SR); out[i:i + n] += sig * _rng2.uniform(.4, 1)
    return out * .5

def _swell(f=None):
    d = 2.2; t = _t(d)
    s = sum(np.sin(2 * np.pi * _mtof(m) * t) + .3 * np.sin(4 * np.pi * _mtof(m) * t) for m in (50, 57, 62, 66))
    return _eng._lp(s, 2200) * (t / d) ** 2 * np.minimum(1, (d - t) * 8) * .3

def _timp(f=None):
    t = _t(1.6)
    return (np.sin(2 * np.pi * np.cumsum(60 + 30 * np.exp(-t * 12)) / SR) + .3 * _eng._lp(_rng2.standard_normal(len(t)), 300)) * np.exp(-t * 2.6) * np.minimum(1, t * 300)

def file_music(N, total):
    """Musica orchestrale generata (audio_in/d01_music.mp3); si interrompe di colpo quando arriva il messaggio al narratore."""
    p = os.path.join(HERE, 'audio_in', 'd01_music.mp3')
    if not os.path.exists(p): return doc_music(N, total)
    a = load_voice(p); a = a[:N]; out = np.zeros(N); out[:len(a)] = a
    out = out / (np.abs(out).max() + 1e-9) * 2.2
    w = json.load(open(os.path.join(HERE, 'audio_in', 'd01.json')))
    cut = next((x['end'] for x in w if x['text'].lower().startswith('crudele')), total) + VO + 1.25
    i = int(cut * SR); n = int(.08 * SR); out[i:i + n] *= np.linspace(1, 0, len(out[i:i + n])); out[i + n:] = 0
    n1 = int(.5 * SR); out[:n1] *= np.linspace(0, 1, n1)
    return out.copy(), out.copy()

_eng.SYNTH.update(crickets=_crickets, birds=_birds, swell=_swell, timp=_timp)
_eng._music = file_music

_caption = _eng.caption
def _caption_no_si(ctx, t, words, scenes):
    """Il «Sì» il narratore lo scrive e basta: niente sottotitolo."""
    return _caption(ctx, t, [w for w in words if not w[1].upper().startswith('SÌ')], scenes)
_eng.caption = _caption_no_si

def letterbox(ctx, t):
    """Look da documentario: bande nere da cinema + grana della pellicola."""
    global _GRAIN
    if _GRAIN is None:
        rng = np.random.default_rng(3); a = (rng.random((480, 270)) * 255).astype(np.uint8)
        data = np.zeros((480, 270, 4), np.uint8); data[..., 0] = data[..., 1] = data[..., 2] = a; data[..., 3] = 255
        _GRAIN = cairo.ImageSurface.create_for_data(bytearray(data.tobytes()), cairo.FORMAT_ARGB32, 270, 480, 270 * 4)
    ctx.save(); ctx.identity_matrix(); ctx.scale(4, 4)
    ox = (int(t * 24) * 37) % 60; oy = (int(t * 24) * 53) % 90
    ctx.set_source_surface(_GRAIN, -ox, -oy); ctx.get_source().set_extend(cairo.EXTEND_REPEAT)
    ctx.paint_with_alpha(.05); ctx.restore()
    ctx.save(); ctx.identity_matrix(); col(ctx, (0, 0, 0))
    ctx.rectangle(0, 0, 1080, 130); ctx.rectangle(0, 1790, 1080, 130); ctx.fill(); ctx.restore()
_GRAIN = None
_CLOCK = [0.0]

def _framed(fn):
    def f(ctx, tau, L, wt):
        fn(ctx, tau, L, wt); letterbox(ctx, tau)
    return f

SCENES = {k: _framed(v) for k, v in dict(s1=s1, s2=s2, s3=s3, s4=s4, s5=s5, s6=s6, s7=s7, s8=s8, s9=s9).items()}

# Copertina: il PT nel binocolo con il messaggio delle 23:47
COVER = lambda ctx: s2(ctx, .9, 3.0, {"L'ERRORE": 2.0})

def SFX(fx, at):
    fx('file:notte', 0.0, .5, max=at('s5', None, .8)); fx('file:alba', at('s7', 'MATTINO', -.4), .45)
    fx('timp', at('s2', 'ERRORE', -.05), .35)
    fx('msg', at('s2', 'ERRORE', -.7), .3, f=800)
    for i in range(4): fx('tick', at('s3', 'RISPONDE', .1 + i * .25), .2)
    fx('msg', at('s3', 'QUATTRO', 0), .28, f=1000)
    fx('msg', at('s4', 'BRANCO', -.2), .25, f=800); fx('msg', at('s4', 'BRANCO', .25), .25, f=900); fx('msg', at('s4', 'QUALSIASI', -.3), .25, f=1000)
    fx('whoosh', at('s6', None), .3); fx('pop', at('s6', 'DISTURBARE', 0), .22, f=900)
    fx('msg', at('s7', 'RISPOSTA', -.5), .22, f=1000)
    fx('msg', at('s8', 'CRUDELE', 1.3), .35, f=900)          # arriva il messaggio, niente vibrazione
    for i in range(2): fx('tick', at('s9', 'SÌ', -.2 + i * .12), .22)   # scrive «Sì»
    fx('pop', at('s9', 'SÌ', .05), .2, f=1000)
    fx('pop', at('s9', 'SÌ', .55), .12, f=2600)                # scintilla sui denti
    for i in range(6): fx('tick', at('s9', 'SCUSATE', .85 + i * .11), .3)  # scappa
    fx('whoosh', at('s9', 'SCUSATE', 1.0), .3)

if __name__ == '__main__':
    main(sys.modules[__name__], 'd01')
