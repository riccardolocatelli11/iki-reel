from props4 import *

TITLE = 'Disdetta un ora prima'
HOOK = "TI DISDICE\nUN'ORA PRIMA?"
LOOP = True; TAIL = 1.4
CTA = 'DISDETTA'
SENT = [
    ("Il cliente ti disdice un'ora prima, e tu non dici niente?", 's1', {'DISDICE', 'NIENTE'}, 0.1),
    ("Errore.", 's2', {'ERRORE'}, 0.1),
    ("Quell'ora l'avevi tenuta per lui, e ormai non la riempi più.", 's3', {'TENUTA', 'RIEMPI'}, 0.1),
    ("Di solito funziona una regola chiara, detta dal primo giorno: si disdice fino a ventiquattro ore prima.", 's4', {'REGOLA', 'PRIMO', 'VENTIQUATTRO'}, 0.1),
    ("Dopo quel limite decidi tu: la sposti, o la conti come fatta.", 's5', {'LIMITE', 'SPOSTI', 'FATTA'}, 0.1),
    ("In iki scegli fino a quando il cliente può disdire da solo: dopo, può solo chiederti di spostarla.", 's6', {'DISDIRE', 'DOPO', 'SPOSTARLA'}, 0.1),
    ("Scrivi «disdetta» nei commenti, e ti mando come funziona.", 's7', {'DISDETTA'}, 0.0),
]

def pt_phone(ctx, tau, x, face, glow=0.0, s=.95):
    """PT con il telefono in mano (braccio destro piegato davanti al petto)."""
    A = fig(ctx, 'pt', lambda t: P(t=0, h=-4, ra1=35, ra2=150, la1=-14, la2=-8), face, x, tau, fx=.1, seed=1, U_=U * s)
    small_phone(ctx, A['hR'] + np.array([0, -30]), rot=.15, glow=glow, s=1.1 * s)
    return A

def msg_bubble(ctx, c, lines, k, side='l', w=420, size=34):
    """Messaggio del cliente (fumetto stile chat)."""
    if k <= 0: return
    h = 50 + 46 * len(lines)
    ctx.save(); ctx.translate(*c); sscale(ctx, eback(clamp(k)))
    rrect(ctx, -w / 2 + 8, -h / 2 + 10, w, h, 30); col(ctx, INK, .15); ctx.fill()
    rrect(ctx, -w / 2, -h / 2, w, h, 30); fill_stroke(ctx, WHITE, 6)
    tx = -w / 2 + 34
    for j, l in enumerate(lines): text(ctx, l, tx, -h / 2 + 50 + j * 46, size, FONTB, INK, anchor='l')
    ctx.restore()

def s1(ctx, tau, L, wt):
    cam(ctx, 1.04, 540, 1040)
    floor(ctx, G)
    td = wt.get('DISDICE', .5); tn = wt.get('NIENTE', L - .6)
    face = dict(eyes='open', mouth='flat' if tau > td else 'smile', brows='worried' if tau > td else 'neutral', look=(.5, -.3))
    pt_phone(ctx, tau, 330, face, glow=clamp((tau - td + .3) * 3))
    mm = int(tau * 7) % 60
    digital_clock(ctx, (790, 660), f'17:{mm:02d}', .95, glow=.3 + .2 * math.sin(tau * 6))
    plate_label(ctx, (790, 790), 'ALLENAMENTO 18:00', 1, bg=INK, tc=WHITE, size=30)
    msg_bubble(ctx, (770, 1020), ['Scusa, oggi', 'non riesco'], prog(tau, td - .3, td), w=440, size=42)
    if tau > tn - .2:
        plate_label(ctx, (330, 640), '…ok', eback(prog(tau, tn - .2, tn + .1)), bg=WHITE, tc=GRAY, size=44, rot=-.05)

def s2(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    floor(ctx, G)
    ts = wt.get('ERRORE', .15)
    no = math.sin(tau * 14) * 9
    fig(ctx, 'pt', lambda t: P(t=0, h=no, la1=-60, la2=60, ra1=60, ra2=-60), dict(eyes='open', mouth='flat', brows='angry', look=(0, 0)), 540, tau, seed=1, U_=U * .95)
    stamp_x(ctx, (540, 690), prog(tau, ts - .05, ts + .2), 1.5)

def agenda(ctx, x, y, w, rows, ks, hl=None, cross=0.0):
    """Agenda della giornata: (ora, nome)."""
    h = 40 + 120 * len(rows)
    rrect(ctx, x + 9, y + 12, w, h, 26); col(ctx, INK, .15); ctx.fill()
    rrect(ctx, x, y, w, h, 26); fill_stroke(ctx, PAPERL, 7)
    for i, (ora, nome) in enumerate(rows):
        k = clamp(ks[i]) if i < len(ks) else 0
        if k <= 0: continue
        yy = y + 30 + i * 120
        on = hl == i
        ctx.save(); ctx.translate(x + w / 2, yy + 50); sscale(ctx, eback(k)); ctx.translate(-(x + w / 2), -(yy + 50))
        rrect(ctx, x + 24, yy, w - 48, 100, 20); fill_stroke(ctx, RED if on and cross > 0 else WHITE, 5)
        tc = WHITE if on and cross > 0 else INK
        text(ctx, ora, x + 56, yy + 50, 40, FONT, tc, anchor='l')
        nm = 'VUOTA' if on and cross > .5 else nome
        text(ctx, nm, x + w - 56, yy + 50, 38, FONTB, tc, anchor='r')
        ctx.restore()

def s3(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    tt = wt.get('TENUTA', .5); tr = wt.get('RIEMPI', L - .8)
    rows = (('16:00', 'Giulia'), ('17:00', 'Luca'), ('18:00', 'Marco'), ('19:00', 'Sara'))
    ks = [prog(tau, .05 + i * .14, .3 + i * .14) for i in range(4)]
    cross = prog(tau, tr - .4, tr)
    agenda(ctx, 110, 560, 560, rows, ks, hl=2, cross=cross)
    if tau > tt - .1:
        plate_label(ctx, (860, 930), 'TENUTA PER LUI', eback(prog(tau, tt - .1, tt + .2)), bg=INK, tc=WHITE, size=30, rot=.05)
    clock(ctx, (860, 760), 120, tau * 3)
    if tau > tr - .3:
        k = eback(prog(tau, tr - .3, tr + .1))
        euro_crossed(ctx, (500, 1240), 1.3 * k)
        plate_label(ctx, (780, 1250), 'ORA PERSA', k, bg=RED, tc=WHITE, size=40, rot=-.05)

def rule_card(ctx, c, k, big, t, glow=0.0):
    if k <= 0: return
    ctx.save(); ctx.translate(*c); sscale(ctx, eback(clamp(k))); ctx.rotate(-.03 + .01 * math.sin(t * 3))
    w, h = 820, 330
    if glow > 0: halo(ctx, (0, 0), 520, RED, .2 * glow)
    rrect(ctx, -w / 2 + 10, -h / 2 + 14, w, h, 40); col(ctx, INK, .18); ctx.fill()
    rrect(ctx, -w / 2, -h / 2, w, h, 40); fill_stroke(ctx, WHITE, 9)
    text(ctx, 'DISDETTA GRATIS', 0, -100, 44, FONT, INK)
    text(ctx, 'FINO A', 0, -40, 36, FONTB, GRAY)
    text(ctx, big, 0, 60, 110, FONT, RED, stroke=INK, sw=9)
    ctx.restore()

def s4(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    tg = wt.get('REGOLA', .8); tp = wt.get('PRIMO', L * .45); tv = wt.get('VENTIQUATTRO', L - 1.2)
    floor(ctx, G)
    A = fig(ctx, 'pt', lambda t: P(t=2, ra1=120 + 8 * math.sin(t * 5), ra2=150, la1=-14, la2=-8),
            dict(eyes='open', mouth='smile', brows='raised', look=(.5, -.4)), 250, tau, fx=.15, seed=1, U_=U * .85)
    fig(ctx, 'client', lambda t: P(t=0, h=3 * math.sin(t * 4)), dict(eyes='open', mouth='smile', brows='neutral', look=(-.5, -.2)), 850, tau, fx=.1, seed=3, U_=U * .8)
    kc = prog(tau, tg - .2, tg + .15)
    hrs = int(lerp(0, 24, eout(prog(tau, tv - .5, tv + .2))))
    big = f'{hrs} ORE' if tau < tv + .2 else '24 ORE'
    rule_card(ctx, (560, 700), kc, big if tau > tv - .5 else '?? ORE', tau, glow=prog(tau, tv, tv + .3))
    if tau > tp - .2:
        plate_label(ctx, (560, 930), 'DAL PRIMO GIORNO', eback(prog(tau, tp - .2, tp + .1)), bg=INK, tc=WHITE, size=34, rot=-.04)

def s5(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    tl = wt.get('LIMITE', .4); ts = wt.get('SPOSTI', L * .55); tf = wt.get('FATTA', L - .6)
    # linea del tempo verso l'allenamento
    y = 700; x0, x1, xl = 110, 970, 720
    kk = eout(prog(tau, 0, .5))
    rrect(ctx, x0, y - 40, (xl - x0) * kk, 80, 40); fill_stroke(ctx, GREEN, 6)
    if tau > tl - .2:
        k2 = eout(prog(tau, tl - .2, tl + .3))
        rrect(ctx, xl, y - 40, (x1 - xl) * k2, 80, 40); fill_stroke(ctx, RED, 6)
    text(ctx, 'PUÒ DISDIRE', (x0 + xl) / 2, y + 2, 34, FONT, WHITE)
    poly(ctx, [(xl, y - 90), (xl, y + 90)], 10)
    plate_label(ctx, (xl, y - 130), '−24 ORE', eback(prog(tau, tl - .2, tl + .1)), bg=INK, tc=WHITE, size=32)
    plate_label(ctx, ((xl + x1) / 2 + 10, y + 140), 'DECIDI TU', eback(prog(tau, tl, tl + .3)), bg=RED, tc=WHITE, size=40, rot=.04)
    # due scelte
    for i, (lab, t0) in enumerate((('LA SPOSTI', ts), ('CONTA COME FATTA', tf))):
        k = eback(prog(tau, t0 - .3, t0))
        if k <= 0: continue
        yy = 1010 + i * 170
        ctx.save(); ctx.translate(540, yy); sscale(ctx, k)
        rrect(ctx, -380 + 8, -65 + 10, 760, 130, 30); col(ctx, INK, .15); ctx.fill()
        rrect(ctx, -380, -65, 760, 130, 30); fill_stroke(ctx, WHITE, 8)
        text(ctx, lab, 0, 2, 46, FONT, INK)
        ctx.restore()
        if tau > t0 + .1: check(ctx, (880, yy - 40), .6 * eback(prog(tau, t0 + .1, t0 + .35)))

def segmenti(ctx, x, y, w, voci, sel, press=0.0):
    n = len(voci); bw = (w - (n - 1) * 10) / n
    for i, v in enumerate(voci):
        on = i == sel; xx = x + i * (bw + 10)
        z = 1 + .1 * press * on
        ctx.save(); ctx.translate(xx + bw / 2, y + 38); ctx.scale(z, z)
        rrect(ctx, -bw / 2, -38, bw, 76, 16)
        if on: col(ctx, RED); ctx.fill()
        else: fill_stroke(ctx, (.97, .96, .94), 3, (.8, .78, .75))
        text(ctx, v, 0, 1, 22, FONT, WHITE if on else INK)
        ctx.restore()

def orari_screen(sel, press, k_on):
    """Schermata reale di iki (PT): Calendario → Orari prenotabili → Regole."""
    def content(ctx, w, h):
        app_head(ctx, w, 'Calendario')
        text(ctx, 'Orari prenotabili', 40, 210, 38, FONT, INK, anchor='l')
        rrect(ctx, 30, 255, w - 60, 110, 20); fill_stroke(ctx, (.97, .96, .94), 3, (.85, .83, .8))
        text(ctx, 'I clienti possono prenotare', 54, 295, 25, FONT, INK, anchor='l')
        text(ctx, 'Negli orari qui sotto, solo quando sei libero', 54, 332, 18, FONTB, GRAY, anchor='l')
        sx = w - 90
        rrect(ctx, sx - 34, 290, 68, 40, 20); col(ctx, mix_c((.8, .78, .75), GREEN, k_on)); ctx.fill()
        ctx.arc(lerp(sx - 14, sx + 14, k_on), 310, 16, 0, 2 * math.pi); col(ctx, WHITE); ctx.fill()
        text(ctx, 'REGOLE', 44, 410, 20, FONT, GRAY, anchor='l')
        text(ctx, 'Durata di ogni allenamento', 40, 455, 22, FONTB, GRAY, anchor='l')
        segmenti(ctx, 30, 475, w - 60, ("30'", "45'", "60'", "90'"), 2)
        text(ctx, 'Prenotabile almeno', 40, 595, 22, FONTB, GRAY, anchor='l')
        segmenti(ctx, 30, 615, w - 60, ('2 ore prima', '12 ore', '1 giorno', '2 giorni'), 1)
        hl = sel >= 0
        if hl:
            rrect(ctx, 18, 718, w - 36, 136, 20); col(ctx, RED, .1); ctx.fill()
        text(ctx, 'Il cliente può disdire da solo fino a', 40, 740, 22, FONT if hl else FONTB, RED if hl else GRAY, anchor='l')
        segmenti(ctx, 30, 762, w - 60, ('6 ore prima', '12 ore', '1 giorno', '2 giorni'), sel if hl else 1, press)
        rrect(ctx, 30, h - 150, w - 60, 90, 20); col(ctx, RED); ctx.fill()
        text(ctx, 'Salva', w / 2, h - 105, 30, FONT, WHITE)
    return content

def mix_c(a, b, k): return tuple(lerp(x, y, clamp(k)) for x, y in zip(a, b))

def card_screen(locked):
    """Schermata reale di iki (cliente): card dell'appuntamento prenotato da lui."""
    def content(ctx, w, h):
        app_head(ctx, w, 'Home')
        y0 = 210
        rrect(ctx, 30, y0, w - 60, 420, 24); fill_stroke(ctx, WHITE, 4, (.85, .83, .8))
        text(ctx, 'PROSSIMO APPUNTAMENTO', 56, y0 + 45, 18, FONT, GRAY, anchor='l')
        rrect(ctx, w - 250, y0 + 24, 196, 42, 21); col(ctx, LGREEN); ctx.fill()
        text(ctx, 'Prenotato da te', w - 152, y0 + 45, 18, FONT, GREEN)
        text(ctx, 'Giovedì 18:00', 56, y0 + 110, 40, FONT, INK, anchor='l')
        text(ctx, "Allenamento con Riccardo · 60'", 56, y0 + 160, 22, FONTB, GRAY, anchor='l')
        bw = (w - 60 - 48 - 16) / 2
        if not locked:
            for i, lab in enumerate(('Disdici', 'Cambia orario')):
                x = 54 + i * (bw + 16)
                rrect(ctx, x, y0 + 210, bw, 80, 18); fill_stroke(ctx, (.97, .96, .94), 3, (.8, .78, .75))
                text(ctx, lab, x + bw / 2, y0 + 250, 26, FONT, INK)
            text(ctx, 'Puoi disdire o cambiare da solo', 56, y0 + 330, 20, FONTB, GRAY, anchor='l')
            text(ctx, 'fino a mercoledì 18:00', 56, y0 + 362, 20, FONTB, GRAY, anchor='l')
        else:
            rrect(ctx, 54, y0 + 210, bw, 80, 18); col(ctx, RED); ctx.fill()
            check(ctx, (54 + 50, y0 + 250), .4, WHITE)
            text(ctx, 'Ci sono', 54 + bw / 2 + 20, y0 + 250, 26, FONT, WHITE)
            x = 54 + bw + 16
            rrect(ctx, x, y0 + 210, bw, 80, 18); fill_stroke(ctx, (.97, .96, .94), 3, (.8, .78, .75))
            text(ctx, 'Chiedi di spostare', x + bw / 2, y0 + 250, 21, FONT, INK)
    return content

def s6(ctx, tau, L, wt):
    up = eout(prog(tau, 0, .35))
    halo(ctx, (540, 1100), 760, RED, .12)
    td = wt.get('DISDIRE', 1.2); tdo = wt.get('DOPO', L * .6); tsp = wt.get('SPOSTARLA', L - .6)
    k_on = prog(tau, .4, .7)
    sel = 2 if tau > td - .2 else -1
    press = 1 - eout(prog(tau, td - .2, td + .2)) if tau > td - .2 else 0
    swap = prog(tau, tdo - .45, tdo - .1)
    if swap < 1:
        phone(ctx, 540 - 1400 * eio(swap), lerp(2600, 1130, up), 640, 1120, orari_screen(sel, press, k_on))
        status_chip(ctx, 540, 500, 'Lo scegli tu', RED, prog(tau, td - .1, td + .2) * (1 - swap * 2), 36)
    if swap > 0:
        locked = tau > tsp - .5
        phone(ctx, 540 + 1400 * (1 - eio(swap)), 1130, 640, 1120, card_screen(locked))
        if locked:
            status_chip(ctx, 540, 500, 'Dopo il limite: decidi tu', RED, prog(tau, tsp - .5, tsp - .2), 34)
        else:
            status_chip(ctx, 540, 500, 'Quello che vede il cliente', INK, prog(tau, tdo, tdo + .3), 34)

def s7(ctx, tau, L, wt):
    cam(ctx, 1.0, 540, 1000)
    tc = wt.get('DISDETTA', .4)
    floor(ctx, G)
    fig(ctx, 'pt', lambda t: P(t=3, ra1=150 + 16 * math.sin(t * 9), ra2=172 + 20 * math.sin(t * 9 + .6), la1=-16, la2=-8),
        dict(eyes='happy', mouth='grin', brows='raised'), 330, tau, fx=.2, seed=1, U_=U * .95)
    fig(ctx, 'client', lambda t: P(t=0, h=4 * math.sin(t * 5), ra1=40, ra2=60), dict(eyes='happy', mouth='smile', brows='neutral', look=(-.5, 0)), 770, tau, fx=.1, seed=3, U_=U * .85)
    cta_card(ctx, CTA, prog(tau, tc - .3, tc + .1), 660, tau)

SCENES = dict(s1=s1, s2=s2, s3=s3, s4=s4, s5=s5, s6=s6, s7=s7)

def SFX(fx, at):
    for i in range(3): fx('tick', at('s1', None, .15 + i * .4), .2)
    fx('msg', at('s1', 'DISDICE', -.2), .35, f=800); fx('sad', at('s1', 'NIENTE', -.1), .14)
    fx('buzz', at('s2', 'ERRORE', -.05), .3); fx('thud', at('s2', 'ERRORE', .0), .5)
    for i in range(4): fx('pop', at('s3', None, .1 + i * .14), .22, f=800 + i * 100)
    fx('ding', at('s3', 'TENUTA', 0), .2, f=1200); fx('buzz', at('s3', 'RIEMPI', -.3), .22); fx('sad', at('s3', 'RIEMPI', .1), .14)
    fx('swoosh_up', at('s4', 'REGOLA', -.2), .28); fx('pop', at('s4', 'PRIMO', -.1), .22, f=700)
    for i in range(5): fx('tick', at('s4', 'VENTIQUATTRO', -.5 + i * .14), .2)
    fx('chime', at('s4', 'VENTIQUATTRO', .2), .22)
    fx('swoosh_up', at('s5', None, .05), .25); fx('thud', at('s5', 'LIMITE', -.1), .35)
    fx('ding', at('s5', 'SPOSTI', -.1), .22, f=1100); fx('ding', at('s5', 'FATTA', -.1), .22, f=1400)
    fx('whoosh', at('s6', None), .35); fx('pop', at('s6', None, .5), .2, f=900); fx('msg', at('s6', 'DISDIRE', -.15), .3, f=1000)
    fx('swoosh_up', at('s6', 'DOPO', -.4), .28); fx('ding', at('s6', 'SPOSTARLA', -.4), .22, f=1300)
    fx('pop', at('s7', 'DISDETTA', -.2), .35, f=800); fx('chime', at('s7', 'DISDETTA', .1), .2)

if __name__ == '__main__':
    main(sys.modules[__name__], '34')
