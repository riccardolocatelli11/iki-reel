"""Oggetti per i reel 22-28."""
from props3 import *

NIGHT = (.13, .16, .3); WA_GREEN = (.07, .37, .33); WA_BUBBLE = (.86, .97, .8)

# ---------------------------------------------------------------- figure in posizioni speciali
def plank_fig(ctx, x_feet, g, tau, face, s=.8, shake=0.0, sag=0.0, seed=2, kind='client'):
    """plank sugli avambracci: testa a sinistra, piedi in (x_feet, g). sag > 0 = bacino che cede"""
    U_ = U * s
    ctx.save(); ctx.translate(x_feet, g - .1 * U_ + shake * math.sin(tau * 60)); ctx.rotate(math.radians(-82 + sag)); ctx.translate(-540, -G)
    A = fig(ctx, kind, lambda t: P(la1=-88, la2=-178, ra1=-92, ra2=-182, ll1=0, ll2=0, rl1=0, rl2=0), face, 540, tau, seed=seed, U_=U_, shadow=False)
    ctx.restore()
    return A

def lying_fig(ctx, x_head, y, tau, face, s=.75, seed=2, kind='client', arms=None, rot=0.0):
    """sdraiato a letto, testa a sinistra (sul cuscino)"""
    U_ = U * s
    ctx.save(); ctx.translate(x_head, y); ctx.rotate(math.radians(90 + rot)); ctx.translate(-540, -G + 3.05 * U_)
    pose = arms or (lambda t: P(la1=-10, la2=-6, ra1=10, ra2=6, ll1=0, ll2=0, rl1=0, rl2=0))
    A = fig(ctx, kind, pose, face, 540, tau, seed=seed, U_=U_, shadow=False)
    ctx.restore()
    return A

def bed(ctx, x, y, w=760, blanket=1.0, t=0.0):
    """letto visto di lato: (x, y) = angolo in alto a sinistra del materasso"""
    rrect(ctx, x - 30, y - 150, 50, 330, 14); fill_stroke(ctx, (.55, .38, .25), 7)          # testiera
    rrect(ctx, x, y, w, 70, 20); fill_stroke(ctx, WHITE, 7)                                  # materasso
    rrect(ctx, x, y + 70, w, 60, 10); fill_stroke(ctx, (.55, .38, .25), 7)                  # rete
    for lx in (x + 20, x + w - 40): rrect(ctx, lx, y + 130, 22, 50, 6); fill_stroke(ctx, (.45, .3, .2), 5)
    ell(ctx, x + 110, y - 18, 95, 38); fill_stroke(ctx, PAPERL, 6)                           # cuscino

def blanket(ctx, x, y, w, h=70, t=0.0, breathe=0.0):
    b = 10 * breathe * math.sin(t * 2.2)
    ctx.move_to(x, y + 60); ctx.curve_to(x + w * .2, y - 30 - b, x + w * .6, y - 40 - b, x + w, y - 10)
    ctx.line_to(x + w + 10, y + 80); ctx.line_to(x - 10, y + 80); ctx.close_path(); fill_stroke(ctx, (.55, .7, .9), 7)
    for i in range(3): poly(ctx, [(x + w * (.25 + i * .22), y - 10 - b * .6), (x + w * (.3 + i * .22), y + 60)], 3, INK, .25)

def nightstand(ctx, x, g, w=190, h=230):
    rrect(ctx, x, g - h, w, h, 12); fill_stroke(ctx, (.62, .45, .3), 7)
    poly(ctx, [(x, g - h * .5), (x + w, g - h * .5)], 5); ctx.arc(x + w / 2, g - h * .3, 9, 0, 2 * math.pi); col(ctx, INK); ctx.fill()

def digital_clock(ctx, c, txt, s=1.0, glow=0.0, cc=RED):
    ctx.save(); ctx.translate(*c); sscale(ctx, s)
    if glow > 0: halo(ctx, (0, 0), 230, cc, .35 * glow)
    rrect(ctx, -150, -70, 300, 140, 26); fill_stroke(ctx, (.15, .15, .17), 8)
    rrect(ctx, -125, -48, 250, 96, 14); col(ctx, (.05, .05, .06)); ctx.fill()
    text(ctx, txt, 0, 2, 74, FONT, cc)
    ctx.restore()

def night_window(ctx, x, y, w, h, t=0.0, day=0.0):
    sky = tuple(lerp(a, b, day) for a, b in zip(NIGHT, (.72, .86, .96)))
    rrect(ctx, x, y, w, h, 12); fill_stroke(ctx, sky, 9)
    ctx.save(); rrect(ctx, x, y, w, h, 12); ctx.clip()
    if day < .5:
        ctx.arc(x + w * .68, y + h * .3, 44, 0, 2 * math.pi); col(ctx, YELLOW, 1 - day * 2); ctx.fill()
        ctx.arc(x + w * .68 + 26, y + h * .3 - 16, 40, 0, 2 * math.pi); col(ctx, sky); ctx.fill()
        for i, (sx, sy) in enumerate(((.2, .2), (.35, .55), (.15, .75), (.85, .7), (.5, .15))):
            a = (.5 + .5 * math.sin(t * 3 + i * 1.7)) * (1 - day * 2)
            sparkle(ctx, x + w * sx, y + h * sy, .35, a)
    else:
        k = (day - .5) * 2
        ctx.arc(x + w * .5, y + h + 40 - 140 * k, 90, 0, 2 * math.pi); col(ctx, YELLOW); ctx.fill()
    ctx.restore()
    poly(ctx, [(x + w / 2, y), (x + w / 2, y + h)], 8); poly(ctx, [(x, y + h / 2), (x + w, y + h / 2)], 8)
    rrect(ctx, x, y, w, h, 12); col(ctx, INK); ctx.set_line_width(9); ctx.stroke()

def small_phone(ctx, c, rot=0.0, glow=0.0, s=1.0, screen=(.75, .85, 1)):
    ctx.save(); ctx.translate(*c); ctx.rotate(rot); sscale(ctx, s)
    if glow > 0: halo(ctx, (0, 0), 200, (.6, .8, 1), .45 * glow)
    rrect(ctx, -34, -60, 68, 120, 12); fill_stroke(ctx, DARK, 5)
    rrect(ctx, -26, -50, 52, 96, 6); col(ctx, screen if glow > 0 else (.3, .3, .32)); ctx.fill()
    ctx.restore()

def zzz(ctx, c, t, a=1.0):
    for i in range(3):
        k = (t * .6 + i / 3) % 1
        text(ctx, 'z', c[0] + 50 * k + i * 6, c[1] - 140 * k, 40 + 30 * k, FONT, BLUE, stroke=None)

# ---------------------------------------------------------------- schermate
def wa_screen(msgs, shown, title='Marco', time='23:04'):
    """chat di messaggistica personale (generica, verde)"""
    def content(ctx, w, h):
        col(ctx, (.93, .9, .85)); ctx.paint()
        ctx.rectangle(0, 0, w, 150); col(ctx, WA_GREEN); ctx.fill()
        ctx.arc(80, 78, 38, 0, 2 * math.pi); fill_stroke(ctx, (.75, .8, .9), 4)
        text(ctx, title, 140, 64, 34, FONTB, WHITE, anchor='l'); text(ctx, 'online', 140, 106, 22, FONTB, (.8, .95, .9), anchor='l')
        y = 200
        for i, (txt, side) in enumerate(msgs):
            k = clamp(shown - i)
            if k <= 0: continue
            lines = txt.split('\n'); ctx.select_font_face(FONTB); ctx.set_font_size(32)
            bw = max(ctx.text_extents(l).width for l in lines) + 70; bh = 40 + 42 * len(lines)
            bx = w - 30 - bw if side == 'r' else 30
            ctx.save(); ctx.translate(bx + bw / 2, y + bh / 2); sscale(ctx, eback(k)); ctx.translate(-bw / 2, -bh / 2)
            rrect(ctx, 0, 0, bw, bh, 26); fill_stroke(ctx, WA_BUBBLE if side == 'r' else WHITE, 3, INK)
            for j, l in enumerate(lines): text(ctx, l, 34, 40 + j * 42, 32, FONTB, INK, anchor='l')
            text(ctx, time, bw - 16, bh - 16, 18, FONTB, GRAY, anchor='r')
            ctx.restore()
            y += bh + 26
    return content

def iki_chat_screen(shown, hl=0.0):
    msgs = [('Domani posso cambiare\nallenamento?', 'l'), ('Certo! Ti rispondo\nentro domani alle 12 💪', 'r')]
    def content(ctx, w, h):
        app_head(ctx, w, 'Chat')
        ctx.arc(85, 225, 44, 0, 2 * math.pi); fill_stroke(ctx, (.75, .8, .9), 4)
        text(ctx, 'Marco Rossi', 150, 210, 34, FONT, INK, anchor='l'); text(ctx, 'Cliente · scheda Forza', 150, 250, 24, FONTB, GRAY, anchor='l')
        poly(ctx, [(30, 300), (w - 30, 300)], 3, INK, .2)
        y = 340
        for i, (txt, side) in enumerate(msgs):
            k = clamp(shown - i)
            if k <= 0: continue
            lines = [l.replace(' 💪', '') for l in txt.split('\n')]; ctx.select_font_face(FONTB); ctx.set_font_size(32)
            bw = max(ctx.text_extents(l).width for l in lines) + 70; bh = 40 + 42 * len(lines)
            bx = w - 30 - bw if side == 'r' else 30
            ctx.save(); ctx.translate(bx + bw / 2, y + bh / 2); sscale(ctx, eback(k)); ctx.translate(-bw / 2, -bh / 2)
            rrect(ctx, 0, 0, bw, bh, 26); fill_stroke(ctx, LIGHT_RED if side == 'r' else WHITE, 3, INK)
            for j, l in enumerate(lines): text(ctx, l, 34, 40 + j * 42, 32, FONTB, INK, anchor='l')
            ctx.restore()
            y += bh + 30
        if hl > 0:
            status_chip(ctx, w / 2, h - 120, 'Separata dal tuo WhatsApp', RED, hl, 28)
    return content

def scheda_video_screen(play, pts):
    """esercizio della scheda con video di esecuzione e punti chiave"""
    def content(ctx, w, h):
        app_head(ctx, w, 'Scheda')
        text(ctx, 'Squat', 40, 215, 44, FONT, INK, anchor='l'); text(ctx, '4 × 8 · 60 kg', w - 40, 218, 30, FONTB, GRAY, anchor='r')
        vx, vy, vw, vh = 30, 260, w - 60, 400
        rrect(ctx, vx, vy, vw, vh, 24); col(ctx, (.18, .18, .2)); ctx.fill()
        ctx.save(); rrect(ctx, vx, vy, vw, vh, 24); ctx.clip()
        col(ctx, (.92, .9, .86)); ctx.rectangle(vx + 10, vy + 10, vw - 20, vh - 20); ctx.fill()
        sq = .5 - .5 * math.cos(play * 2 * math.pi * 1.2) if play > 0 else 0
        draw_fig(ctx, 'pt', P(t=0, la1=-30, la2=-60, ra1=30, ra2=60, ll1=lerp(-12, -60, sq), ll2=lerp(-6, 10, sq), rl1=lerp(12, 60, sq), rl2=lerp(6, -10, sq)),
                 dict(eyes='open', mouth='flat', brows='neutral'), w / 2, vy + vh - 30, 105, play, seed=1, shadow=False)
        ctx.restore()
        if play <= 0:
            ctx.arc(w / 2, vy + vh / 2, 70, 0, 2 * math.pi); col(ctx, RED); ctx.fill()
            ctx.move_to(w / 2 - 22, vy + vh / 2 - 36); ctx.line_to(w / 2 + 38, vy + vh / 2); ctx.line_to(w / 2 - 22, vy + vh / 2 + 36); ctx.close_path(); col(ctx, WHITE); ctx.fill()
        rrect(ctx, vx + 30, vy + vh - 24, vw - 60, 10, 5); col(ctx, WHITE, .5); ctx.fill()
        rrect(ctx, vx + 30, vy + vh - 24, (vw - 60) * clamp(play / 3), 10, 5); col(ctx, RED); ctx.fill()
        text(ctx, 'Video di esecuzione', vx + 34, vy + 38, 24, FONTB, WHITE, anchor='l') if False else None
        for i, t_ in enumerate(('Piedi larghi come le spalle', 'Ginocchia in fuori', 'Petto alto')):
            k = clamp(pts * 3 - i)
            if k <= 0: continue
            y = 720 + i * 92
            ctx.save(); ctx.translate(0, (1 - eout(k)) * 30)
            rrect(ctx, 30, y, w - 60, 76, 20); col(ctx, SOFT); ctx.fill()
            ctx.arc(72, y + 38, 22, 0, 2 * math.pi); col(ctx, RED); ctx.fill(); text(ctx, str(i + 1), 72, y + 39, 26, FONT, WHITE)
            text(ctx, t_, 112, y + 39, 30, FONTB, INK, anchor='l'); ctx.restore()
    return content

def emom_screen(frac, big, label, beep=0.0, rounds=None):
    def content(ctx, w, h):
        timer_screen(frac, label, big)(ctx, w, h)
        if beep > 0:
            for i in range(3):
                r = 270 + i * 40 + 60 * beep
                ctx.arc(w / 2, 560, r, -.6, .6); col(ctx, RED, (1 - beep) * (1 - i * .25)); ctx.set_line_width(10); ctx.stroke()
                ctx.arc(w / 2, 560, r, math.pi - .6, math.pi + .6); ctx.stroke()
        rrect(ctx, 30, 880, w - 60, 100, 24); col(ctx, SOFT); ctx.fill()
        text(ctx, 'Burpee × 10 · Swing × 12', w / 2, 932, 30, FONTB, INK)
        if rounds: status_chip(ctx, w / 2, 1040, rounds, RED, 1, 28)
    return content

def invite_screen(p, done):
    rows = ['Dati personali', 'Consensi', 'Anamnesi']
    def content(ctx, w, h):
        app_head(ctx, w, 'Iscrizione')
        rrect(ctx, 30, 190, w - 60, 130, 24); col(ctx, LIGHT_RED); ctx.fill()
        text(ctx, 'Invito di', w / 2, 230, 26, FONTB, GRAY); text(ctx, 'Riccardo · Personal Trainer', w / 2, 278, 32, FONT, RED)
        for i, r in enumerate(rows):
            k = clamp(p * 3 - i)
            if k <= 0: continue
            y = 370 + i * 150
            ctx.save(); ctx.translate(w / 2, y + 60); sscale(ctx, lerp(.8, 1, eout(k))); ctx.translate(-w / 2, -(y + 60))
            rrect(ctx, 30, y, w - 60, 120, 24); fill_stroke(ctx, WHITE, 4, INK)
            text(ctx, r, 70, y + 60, 36, FONT, INK, anchor='l')
            dk = clamp(done * 3 - i)
            ctx.arc(w - 90, y + 60, 32, 0, 2 * math.pi); fill_stroke(ctx, GREEN if dk > 0 else WHITE, 5, GREEN if dk > 0 else GRAY)
            if dk > 0: check(ctx, (w - 90, y + 60), .45 * eback(dk), WHITE)
            ctx.restore()
        if done >= 1:
            rrect(ctx, 60, 860, w - 120, 110, 55); col(ctx, RED); ctx.fill(); text(ctx, 'Iscrizione completata', w / 2, 916, 32, FONT, WHITE)
    return content

def editor_tech_screen(open_, pick, hl=0.0):
    """editor scheda: tecnica di intensità sul singolo esercizio"""
    rows = [('Panca piana', '4 × 8'), ('Croci ai cavi', '3 × 12'), ('Spinte manubri', '3 × 10')]
    def content(ctx, w, h):
        app_head(ctx, w, 'Editor scheda')
        for i, (a, b) in enumerate(rows):
            y = 200 + i * 150; on = i == 2
            rrect(ctx, 30, y, w - 60, 130, 24); col(ctx, LIGHT_RED if on and hl > 0 else SOFT); ctx.fill()
            if on and hl > 0: rrect(ctx, 30, y, w - 60, 130, 24); col(ctx, RED, hl); ctx.set_line_width(6); ctx.stroke()
            text(ctx, a, 60, y + 48, 34, FONT, INK, anchor='l'); text(ctx, b, 60, y + 96, 26, FONTB, GRAY, anchor='l')
            if on and pick > 0: status_chip(ctx, w - 150, y + 66, 'Drop set', RED, pick, 26)
        y0 = 680
        text(ctx, 'Tecnica di intensità', 40, y0, 30, FONTB, GRAY, anchor='l')
        rrect(ctx, 30, y0 + 30, w - 60, 86, 20); fill_stroke(ctx, WHITE, 4)
        text(ctx, 'Drop set' if pick > .5 else 'Nessuna', 60, y0 + 74, 32, FONT, RED if pick > .5 else INK, anchor='l')
        ctx.move_to(w - 90, y0 + 62); ctx.line_to(w - 70, y0 + 84); ctx.line_to(w - 50, y0 + 62); col(ctx, INK); ctx.set_line_width(6); ctx.stroke()
        if open_ > 0:
            opts = ['Drop set', 'Rest-pause', 'Superserie']
            ctx.save(); ctx.translate(0, y0 + 126); sscale(ctx, 1, eout(open_))
            rrect(ctx, 30, 0, w - 60, 270, 20); fill_stroke(ctx, WHITE, 4)
            for j, o in enumerate(opts):
                if j == 0 and pick > 0: rrect(ctx, 40, 10 + j * 85, w - 80, 80, 14); col(ctx, LIGHT_RED); ctx.fill()
                text(ctx, o, 60, 50 + j * 85, 32, FONTB, INK, anchor='l')
            ctx.restore()
    return content

def client_tech_screen(k):
    def content(ctx, w, h):
        app_head(ctx, w, 'Oggi')
        text(ctx, 'Petto e spalle', 40, 220, 40, FONT, INK, anchor='l')
        for i, (a, b, tech) in enumerate((('Panca piana', '4 × 8 · 70 kg', None), ('Croci ai cavi', '3 × 12', None), ('Spinte manubri', '3 × 10 · 24 kg', 'DROP SET'))):
            y = 270 + i * 170
            rrect(ctx, 30, y, w - 60, 150, 24); col(ctx, SOFT); ctx.fill()
            text(ctx, a, 60, y + 55, 36, FONT, INK, anchor='l'); text(ctx, b, 60, y + 105, 28, FONTB, GRAY, anchor='l')
            if tech and k > 0:
                rrect(ctx, 30, y, w - 60, 150, 24); col(ctx, RED, k); ctx.set_line_width(6); ctx.stroke()
                status_chip(ctx, w - 150, y + 55, tech, RED, k, 26)
                if k > .5: text(ctx, 'Ultima serie: scala e continua', w - 60, y + 108, 22, FONTB, RED, anchor='r')
    return content

def sleep_chart_screen(p, hl=0.0):
    sleep = [5, 5.5, 6, 6.5, 7, 7.2, 7.5, 7.4]; weight = [82, 82, 81.8, 81.2, 80.6, 80.1, 79.5, 79.1]
    def content(ctx, w, h):
        app_head(ctx, w, 'Andamento')
        text(ctx, 'Marco · ultime 8 settimane', 40, 215, 30, FONT, INK, anchor='l')
        x0, y0, cw, ch = 70, 300, w - 120, 380
        rrect(ctx, 26, 260, w - 52, 470, 24); col(ctx, SOFT); ctx.fill()
        n = len(sleep); bw = cw / n
        for i, s in enumerate(sleep):
            k = clamp(p * n * 1.3 - i)
            if k <= 0: continue
            bh = ch * (s / 9) * eout(k)
            rrect(ctx, x0 + i * bw + 10, y0 + ch - bh, bw - 20, bh, 10); col(ctx, (.45, .55, .9)); ctx.fill()
        pts = [(x0 + i * bw + bw / 2, y0 + ch - ch * (wv - 78) / 5) for i, wv in enumerate(weight)]
        m = max(1, int(round(len(pts) * clamp(p * 1.3 - .3))))
        if p > .25:
            poly(ctx, pts[:m], 9, RED)
            for q in pts[:m]: ctx.arc(*q, 11, 0, 2 * math.pi); fill_stroke(ctx, WHITE, 5, RED)
        for j, (cc, lab) in enumerate((((.45, .55, .9), 'Sonno (ore)'), (RED, 'Peso (kg)'))):
            rrect(ctx, 60 + j * 280, 780, 30, 30, 8); col(ctx, cc); ctx.fill(); text(ctx, lab, 102 + j * 280, 796, 26, FONTB, INK, anchor='l')
        for j, (ic, lab) in enumerate((('moon', 'Sonno 7,4 h'), ('plate', '2.100 kcal'))):
            x = 40 + j * (w - 60) / 2
            rrect(ctx, x, 860, (w - 100) / 2, 100, 24); col(ctx, LIGHT_RED if hl > 0 and j == 0 else SOFT); ctx.fill()
            icon(ctx, ic, (x + 50, 910), .4); text(ctx, lab, x + 95, 911, 28, FONTB, INK, anchor='l')
    return content

def work_timer_screen(frac, big, done=False, beep=0.0, serie='Serie 2 di 3'):
    def content(ctx, w, h):
        ctx.rectangle(0, 0, w, 150); col(ctx, RED); ctx.fill()
        logo(ctx, 115, 78, 118, 'bianco'); text(ctx, 'Allenamento', w - 40, 92, 30, FONTB, WHITE, anchor='r')
        text(ctx, 'Plank', 40, 220, 44, FONT, INK, anchor='l'); text(ctx, '3 × 40"', w - 40, 222, 32, FONTB, GRAY, anchor='r')
        c = (w / 2, 560); r = 220
        ctx.arc(*c, r, 0, 2 * math.pi); col(ctx, (.93, .91, .88)); ctx.set_line_width(36); ctx.stroke()
        if frac > 0:
            ctx.arc(*c, r, -math.pi / 2, -math.pi / 2 + 2 * math.pi * frac); col(ctx, GREEN if done else RED); ctx.set_line_width(36); ctx.stroke()
        text(ctx, big, c[0], c[1] - 10, 110, FONT, GREEN if done else INK)
        text(ctx, 'LAVORO', c[0], c[1] + 90, 36, FONTB, GRAY)
        if beep > 0:
            for i in range(3):
                rr = 270 + i * 40 + 60 * beep
                ctx.arc(w / 2, 560, rr, -.6, .6); col(ctx, GREEN, (1 - beep) * (1 - i * .25)); ctx.set_line_width(10); ctx.stroke()
                ctx.arc(w / 2, 560, rr, math.pi - .6, math.pi + .6); ctx.stroke()
        status_chip(ctx, w / 2, 900, serie, INK, 1, 30)
    return content

# ---------------------------------------------------------------- oggetti
def whiteboard(ctx, x, y, w, h, items, ks, title=None, strike=None):
    rrect(ctx, x + 10, y + 12, w, h, 18); col(ctx, INK, .15); ctx.fill()
    rrect(ctx, x, y, w, h, 18); fill_stroke(ctx, WHITE, 9, (.6, .6, .62))
    if title: text(ctx, title, x + w / 2, y + 60, 46, FONT, INK)
    for i, it in enumerate(items):
        k = clamp(ks[i]) if i < len(ks) else 0
        if k <= 0: continue
        yy = y + (130 if title else 70) + i * 92
        n = max(1, int(len(it) * min(1, k * 1.6)))
        ctx.arc(x + 50, yy, 12, 0, 2 * math.pi); col(ctx, RED); ctx.fill()
        text(ctx, it[:n], x + 80, yy + 2, 40, FONT, INK, anchor='l')
    if strike is not None and strike > 0:
        poly(ctx, [(x + 30, y + h - 40), (x + 30 + (w - 60) * eout(strike), y + 40)], 12, RED)

def minute_blocks(ctx, x, y, w, n, cur, work=.6, labels=True, rest_lab='RECUPERO'):
    """EMOM: ogni minuto = lavoro (rosso) + recupero (verde). cur = minuti trascorsi (float)"""
    bw = w / n
    for i in range(n):
        bx = x + i * bw
        rrect(ctx, bx + 6, y, bw - 12, 140, 16); fill_stroke(ctx, PAPERL, 5)
        f = clamp(cur - i)
        if f > 0:
            ww = (bw - 24) * min(f, work) / 1
            ctx.rectangle(bx + 12, y + 8, ww, 124); col(ctx, RED); ctx.fill()
            if f > work: ctx.rectangle(bx + 12 + (bw - 24) * work, y + 8, (bw - 24) * (f - work), 124); col(ctx, GREEN); ctx.fill()
        if labels: text(ctx, f'{i + 1}\'', bx + bw / 2, y + 180, 34, FONT, INK)
    poly(ctx, [(x + cur * bw, y - 30), (x + cur * bw, y + 170)], 8, INK) if 0 < cur < n else None

def lap_counter(ctx, c, n, k=1.0, label='GIRI', cc=RED):
    ctx.save(); ctx.translate(*c)
    rrect(ctx, -170, -150, 340, 300, 40); fill_stroke(ctx, WHITE, 9)
    text(ctx, label, 0, -95, 40, FONT, GRAY)
    ctx.save(); ctx.translate(0, 30); sscale(ctx, 1 + .25 * math.sin(math.pi * clamp(k))); text(ctx, str(n), 0, 0, 160, FONT, cc); ctx.restore()
    ctx.restore()

def paper_stack(ctx, c, n, t=0.0, s=1.0):
    ctx.save(); ctx.translate(*c); sscale(ctx, s)
    for i in range(n):
        ctx.save(); ctx.translate(math.sin(i * 2.3) * 10, -i * 14); ctx.rotate(math.sin(i * 1.7) * .08)
        ctx.rectangle(-110, -140, 220, 280); fill_stroke(ctx, PAPERL, 5)
        for j in range(4): poly(ctx, [(-80, -100 + j * 40), (60, -100 + j * 40)], 3, INK, .3)
        ctx.restore()
    ctx.restore()

def balloon(ctx, c, size, t=0.0, wob=0.0, cc=RED, txt=''):
    x, y = c
    r = 120 * size
    ctx.save(); ctx.translate(x + wob * math.sin(t * 30) * 8, y); ctx.rotate(wob * .3 * math.sin(t * 17))
    ell(ctx, 0, 0, r * .85, r); fill_stroke(ctx, cc, 7)
    ell(ctx, -r * .35, -r * .45, r * .16, r * .24); col(ctx, WHITE, .5); ctx.fill()
    ctx.move_to(-10, r); ctx.line_to(10, r); ctx.line_to(0, r + 18); ctx.close_path(); fill_stroke(ctx, cc, 5)
    if txt and size > .4: text(ctx, txt, 0, 0, 40 * size / .9, FONT, WHITE)
    ctx.restore()
    pts = [(x + math.sin(t * 3 + i * .5) * 10 * (i / 8), y + r + 18 + i * 30) for i in range(9)]
    poly(ctx, pts, 4)

def kitchen_timer(ctx, c, ang, s=1.0, ring=0.0):
    ctx.save(); ctx.translate(*c); sscale(ctx, s)
    if ring > 0: ctx.rotate(.12 * math.sin(ring * 60))
    ctx.arc(0, 0, 130, 0, 2 * math.pi); fill_stroke(ctx, (.95, .4, .3), 9)
    ctx.arc(0, 0, 95, 0, 2 * math.pi); fill_stroke(ctx, WHITE, 6)
    for i in range(12):
        a = i / 12 * 2 * math.pi + ang
        poly(ctx, [(math.sin(a) * 70, -math.cos(a) * 70), (math.sin(a) * 88, -math.cos(a) * 88)], 6 if i % 3 == 0 else 3)
    ctx.move_to(0, -130); ctx.line_to(-16, -158); ctx.line_to(16, -158); ctx.close_path(); col(ctx, INK); ctx.fill()
    rrect(ctx, -24, -180, 48, 26, 8); fill_stroke(ctx, (.95, .4, .3), 5)
    ctx.restore()

def step_bars(ctx, x, g, vals, ks, hl=-1, unit='"', w=260):
    """scalini di progressione 30 -> 40 -> 50"""
    for i, v in enumerate(vals):
        k = clamp(ks[i])
        if k <= 0: continue
        h = 180 + i * 150
        bx = x + i * (w + 30)
        hh = h * eout(k)
        rrect(ctx, bx, g - hh, w, hh, 18); fill_stroke(ctx, LIGHT_RED if i == hl else PAPERL, 7, RED if i == hl else INK)
        if k > .5:
            text(ctx, f'{v}{unit}', bx + w / 2, g - hh + 70, 72, FONT, RED if i == hl else INK)
            text(ctx, f'SETT. {i + 1}', bx + w / 2, g - hh + 130, 28, FONTB, GRAY)

def plate_stack(ctx, c, n, s=1.0):
    ctx.save(); ctx.translate(*c); sscale(ctx, s)
    for i in range(n):
        ell(ctx, 0, -i * 34, 130, 34); fill_stroke(ctx, DARK, 6)
        ell(ctx, 0, -i * 34 - 6, 26, 8); col(ctx, (.5, .5, .5)); ctx.fill()
    ctx.restore()
