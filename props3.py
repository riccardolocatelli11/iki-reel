"""Oggetti per i reel 15-21 (gancio, CTA, loop)."""
from props2 import *

LIGHT_RED = (1, .9, .88); SOFT = (.97, .94, .9); LGREEN = (.86, .95, .88)

# ---------------------------------------------------------------- CTA
def cta_card(ctx, word, k, y=640, t=0.0):
    """Scheda finale: Scrivi «PAROLA» nei commenti."""
    if k <= 0: return
    ctx.save(); ctx.translate(540, y); sscale(ctx, eback(clamp(k)))
    ctx.rotate(-.02 + .008 * math.sin(t * 3))
    w, h = 900, 300
    rrect(ctx, -w / 2 + 10, -h / 2 + 14, w, h, 46); col(ctx, INK, .18); ctx.fill()
    rrect(ctx, -w / 2, -h / 2, w, h, 46); fill_stroke(ctx, WHITE, 9)
    text(ctx, 'SCRIVI', -60, -88, 46, FONT, INK)
    ctx.select_font_face(FONT); ctx.set_font_size(104); tw = ctx.text_extents(f'«{word}»').width
    sz = 104 * min(1, 540 / max(tw, 1))
    text(ctx, f'«{word}»', -60, 6, sz, FONT, RED, stroke=INK, sw=10)
    text(ctx, 'NEI COMMENTI', -60, 98, 46, FONT, INK)
    # icona commento che rimbalza
    bx, by = 330, -10 + 10 * math.sin(t * 6)
    ctx.move_to(bx - 70, by - 60); ctx.line_to(bx + 70, by - 60); ctx.curve_to(bx + 95, by - 60, bx + 95, by - 60, bx + 95, by - 35)
    ctx.line_to(bx + 95, by + 30); ctx.curve_to(bx + 95, by + 55, bx + 95, by + 55, bx + 70, by + 55)
    ctx.line_to(bx - 20, by + 55); ctx.line_to(bx - 55, by + 92); ctx.line_to(bx - 50, by + 55); ctx.line_to(bx - 70, by + 55)
    ctx.curve_to(bx - 95, by + 55, bx - 95, by + 55, bx - 95, by + 30); ctx.line_to(bx - 95, by - 35)
    ctx.curve_to(bx - 95, by - 60, bx - 95, by - 60, bx - 70, by - 60); ctx.close_path()
    fill_stroke(ctx, RED, 7)
    for i in range(3):
        ctx.arc(bx - 40 + i * 40, by - 2 - 8 * max(0, math.sin(t * 8 - i * .8)), 11, 0, 2 * math.pi); col(ctx, WHITE); ctx.fill()
    ctx.restore()

# ---------------------------------------------------------------- schermate telefono
def app_head(ctx, w, title, sub=None):
    ctx.rectangle(0, 0, w, 150); col(ctx, RED); ctx.fill()
    logo(ctx, 115, 78, 118, 'bianco'); text(ctx, title, w - 40, 92, 30, FONTB, WHITE, anchor='r')

def status_chip(ctx, x, y, txt, cc, k=1.0, size=26):
    if k <= 0: return
    ctx.save(); ctx.translate(x, y); sscale(ctx, eback(clamp(k)))
    ctx.select_font_face(FONTB); ctx.set_font_size(size); w = ctx.text_extents(txt).width + 36
    rrect(ctx, -w / 2, -size * .85, w, size * 1.7, size * .85); col(ctx, cc); ctx.fill()
    text(ctx, txt, 0, 1, size, FONTB, WHITE); ctx.restore()

def chat_screen(msgs, shown, title='Chat'):
    """msgs: (testo, lato 'r'/'l', colore sfondo, colore testo)."""
    def content(ctx, w, h):
        ctx.rectangle(0, 0, w, 150); col(ctx, (.2, .2, .22)); ctx.fill()
        ctx.arc(80, 78, 38, 0, 2 * math.pi); fill_stroke(ctx, (.75, .8, .9), 4)
        text(ctx, title, 140, 80, 34, FONTB, WHITE, anchor='l')
        y = 200
        for i, m in enumerate(msgs):
            k = clamp(shown - i)
            if k <= 0: continue
            txt, side, bg, tc = m
            ctx.select_font_face(FONTB); ctx.set_font_size(32); bw = ctx.text_extents(txt).width + 60
            bx = w - 30 - bw if side == 'r' else 30
            ctx.save(); ctx.translate(bx + bw / 2, y + 40); sscale(ctx, eback(k)); ctx.translate(-bw / 2, -40)
            rrect(ctx, 0, 0, bw, 80, 30); fill_stroke(ctx, bg, 3, INK)
            text(ctx, txt, bw / 2, 41, 32, FONTB, tc)
            if side == 'r': text(ctx, '✓✓', bw - 22, 66, 18, FONTB, GRAY)
            ctx.restore()
            y += 104
    return content

def payments_screen(p, paid):
    """Pagamenti -> Gestisci pagamenti: Stripe collegato + rate."""
    rows = [('Rata 1', '1 ott', '120 €'), ('Rata 2', '1 nov', '120 €'), ('Rata 3', '1 dic', '120 €')]
    def content(ctx, w, h):
        app_head(ctx, w, 'Pagamenti')
        text(ctx, 'Gestisci pagamenti', 40, 215, 38, FONT, INK, anchor='l')
        rrect(ctx, 30, 260, w - 60, 90, 24); col(ctx, LGREEN); ctx.fill()
        ctx.arc(80, 305, 22, 0, 2 * math.pi); col(ctx, GREEN); ctx.fill(); check(ctx, (80, 305), .32, WHITE)
        text(ctx, 'Stripe collegato', 120, 306, 32, FONTB, GREEN, anchor='l')
        for i, (a, b, c) in enumerate(rows):
            k = clamp(p * 3 - i)
            if k <= 0: continue
            y = 390 + i * 170
            rrect(ctx, 26, y, w - 52, 145, 24); col(ctx, SOFT, k); ctx.fill()
            text(ctx, a, 60, y + 50, 36, FONT, INK, anchor='l'); text(ctx, b + ' · ' + c, 60, y + 102, 28, FONTB, GRAY, anchor='l')
            pk = clamp(paid[i]) if i < len(paid) else 0
            if pk > 0: status_chip(ctx, w - 130, y + 72, 'Pagata', GREEN, pk)
            else: status_chip(ctx, w - 140, y + 72, 'In arrivo', (.85, .6, .1), 1)
    return content

def gallery_screen(scroll, found=-1.0, tidy=0.0):
    kinds = ['meme', 'cat', 'receipt', 'shot', 'selfie', 'food', 'meme', 'shot', 'cat', 'selfie', 'receipt', 'food']
    def content(ctx, w, h):
        ctx.rectangle(0, 0, w, 150); col(ctx, (.2, .2, .22)); ctx.fill()
        text(ctx, 'Galleria · 4.012', w / 2, 80, 34, FONTB, WHITE)
        cs = (w - 40) / 3
        off = (scroll * 900) % (cs * 4)
        for r in range(-1, 9):
            for c in range(3):
                idx = (r * 3 + c + int((scroll * 900) // (cs * 4)) * 12) % 12
                x = 20 + c * cs; y = 170 + r * cs - off
                if y > h or y + cs < 150: continue
                kd = kinds[idx]
                if tidy > 0 and r == 1 and c == 1: kd = 'before'
                thumb(ctx, x + 6, y + 6, cs - 12, kd)
        if found >= 0:
            k = eback(clamp(found))
            ctx.save(); ctx.translate(w / 2, h / 2); sscale(ctx, k)
            rrect(ctx, -170, -170, 340, 340, 20); col(ctx, RED); ctx.set_line_width(14); ctx.stroke()
            ctx.restore()
    return content

def thumb(ctx, x, y, s, kind):
    ctx.save(); ctx.rectangle(x, y, s, s); ctx.clip()
    bg = {'meme': (.95, .95, .9), 'cat': (.9, .8, .65), 'receipt': (.85, .85, .88), 'shot': (.75, .82, .95),
          'selfie': (.95, .8, .78), 'food': (.95, .88, .6), 'before': (.88, .9, .95)}[kind]
    ctx.rectangle(x, y, s, s); col(ctx, bg); ctx.fill()
    cx, cy = x + s / 2, y + s / 2
    if kind == 'meme':
        text(ctx, 'LOL', cx, y + s * .25, s * .2, FONT, INK); ctx.arc(cx, cy + s * .15, s * .2, 0, 2 * math.pi); fill_stroke(ctx, YELLOW, 4)
    elif kind == 'cat':
        ctx.arc(cx, cy + 8, s * .28, 0, 2 * math.pi); fill_stroke(ctx, (.95, .6, .3), 4)
        for sx in (-1, 1):
            ctx.move_to(cx + sx * s * .25, cy - s * .1); ctx.line_to(cx + sx * s * .18, cy - s * .38); ctx.line_to(cx + sx * s * .05, cy - s * .18); fill_stroke(ctx, (.95, .6, .3), 4)
    elif kind == 'receipt':
        ctx.rectangle(cx - s * .22, y + s * .12, s * .44, s * .76); fill_stroke(ctx, WHITE, 3)
        for i in range(5): poly(ctx, [(cx - s * .15, y + s * (.25 + i * .11)), (cx + s * .15, y + s * (.25 + i * .11))], 3, INK, .5)
    elif kind == 'shot':
        rrect(ctx, x + s * .15, y + s * .15, s * .7, s * .18, 6); col(ctx, (.3, .45, .8)); ctx.fill()
        for i in range(3): poly(ctx, [(x + s * .2, y + s * (.5 + i * .13)), (x + s * .8, y + s * (.5 + i * .13))], 5, INK, .35)
    elif kind in ('selfie', 'before'):
        ctx.arc(cx, cy - s * .08, s * .18, 0, 2 * math.pi); fill_stroke(ctx, WHITE, 4)
        poly(ctx, [(cx, cy + s * .1), (cx, cy + s * .5)], 6)
        if kind == 'selfie': text(ctx, ':)', cx, cy - s * .07, s * .14, FONT, INK)
        else: text(ctx, 'PRIMA', cx, y + s * .88, s * .14, FONT, RED)
    elif kind == 'food':
        ctx.arc(cx, cy, s * .32, 0, 2 * math.pi); fill_stroke(ctx, WHITE, 4)
        ctx.arc(cx, cy, s * .18, 0, 2 * math.pi); col(ctx, (.85, .35, .2)); ctx.fill()
    ctx.restore()
    ctx.rectangle(x, y, s, s); col(ctx, INK, .5); ctx.set_line_width(2); ctx.stroke()

def body_photo(ctx, cx, cy, iw, light=1.0, side=False, label=''):
    """contenuto polaroid: omino in posa, luce variabile."""
    col(ctx, (lerp(.25, .93, light), lerp(.25, .9, light), lerp(.3, .82, light))); ctx.paint()
    U_ = iw * .2; g = cy + iw * .42
    face = dict(eyes='open', mouth='flat', brows='neutral', look=(1 if side else 0, 0))
    draw_fig(ctx, 'client', P(t=0, la1=-25, la2=-15, ra1=25, ra2=15), face, cx, g, U_, 0, fx=.8 if side else 0, seed=3, shadow=False)
    if light < .6:
        ctx.rectangle(cx - iw, cy - iw, iw * 2, iw * 2); col(ctx, INK, .35 * (1 - light)); ctx.fill()

def photos_screen(p, hl=0.0):
    """andamento del cliente: foto affiancate con data."""
    def content(ctx, w, h):
        app_head(ctx, w, 'Andamento')
        text(ctx, 'Giulia · Foto di check', 40, 215, 34, FONT, INK, anchor='l')
        for i, (lab, dt) in enumerate((('PRIMA', '1 set'), ('DOPO', '29 set'))):
            k = clamp(p * 2 - i)
            if k <= 0: continue
            x = 40 + i * (w - 80) / 2; pw = (w - 120) / 2
            ctx.save(); ctx.translate(x + pw / 2, 560); sscale(ctx, eback(k)); ctx.translate(-(x + pw / 2), -560)
            rrect(ctx, x, 270, pw, 520, 20); fill_stroke(ctx, WHITE, 4)
            ctx.save(); rrect(ctx, x + 14, 284, pw - 28, 400, 14); ctx.clip()
            body_photo(ctx, x + pw / 2, 484, pw - 28, 1.0)
            if i == 1:
                pass
            ctx.restore()
            text(ctx, lab, x + pw / 2, 720, 32, FONT, RED if i else INK); text(ctx, dt, x + pw / 2, 762, 26, FONTB, GRAY)
            ctx.restore()
        if p > .9:
            for j, t_ in enumerate(('Stessa luce', 'Stessa posa', 'Stessa ora')):
                kk = clamp(hl * 3 - j)
                if kk > 0:
                    check(ctx, (70, 860 + j * 80), .5 * eback(kk)); text(ctx, t_, 110, 862 + j * 80, 32, FONTB, INK, anchor='l')
    return content

def measures_screen(p):
    def content(ctx, w, h):
        app_head(ctx, w, 'Misure')
        for i, (lab, data, lo, hi, unit) in enumerate((('Peso', [72, 72.6, 71.8, 72.4, 72.1, 72.5], 70, 74, 'kg'),
                                                      ('Vita', [84, 83.2, 82.6, 81.9, 81.1, 80.4], 79, 85, 'cm'))):
            y = 190 + i * 450
            rrect(ctx, 26, y, w - 52, 420, 24); col(ctx, SOFT); ctx.fill()
            text(ctx, lab, 56, y + 50, 38, FONT, INK, anchor='l')
            txt = f'{data[-1]:.1f} {unit}'.replace('.', ',')
            text(ctx, txt, w - 56, y + 50, 32, FONTB, RED if i else GRAY, anchor='r')
            chart(ctx, 90, y + 110, w - 160, 260, clamp(p * 1.3 - i * .3), lw=7, labels=False, data=data, lo=lo, hi=hi)
        for j, (ic, lab) in enumerate((('moon', 'Sonno 7h'), ('plate', '1.950 kcal'))):
            x = 40 + j * (w - 60) / 2
            rrect(ctx, x, 1110 - 220, (w - 100) / 2, 90, 24); col(ctx, SOFT); ctx.fill()
            icon(ctx, ic, (x + 50, 935), .4); text(ctx, lab, x + 95, 936, 28, FONTB, INK, anchor='l')
    return content

def slider_screen(v, ex='Panca piana', serie='Serie 3'):
    def content(ctx, w, h):
        app_head(ctx, w, 'Allenamento')
        text(ctx, ex, 40, 220, 42, FONT, INK, anchor='l'); text(ctx, serie + ' · 60 kg × 8', 40, 275, 30, FONTB, GRAY, anchor='l')
        text(ctx, 'Quanto è stata dura?', w / 2, 420, 34, FONTB, INK)
        text(ctx, f'RPE {v:.0f}', w / 2, 540, 96, FONT, RED)
        x0, x1, y = 70, w - 70, 680
        rrect(ctx, x0, y - 14, x1 - x0, 28, 14); col(ctx, (.9, .88, .85)); ctx.fill()
        fx_ = x0 + (x1 - x0) * clamp((v - 1) / 9)
        rrect(ctx, x0, y - 14, fx_ - x0, 28, 14); col(ctx, RED); ctx.fill()
        ctx.arc(fx_, y, 40, 0, 2 * math.pi); fill_stroke(ctx, WHITE, 8, RED)
        for i in range(1, 11): text(ctx, str(i), x0 + (x1 - x0) * (i - 1) / 9, y + 80, 26, FONTB, GRAY)
        rrect(ctx, 60, 880, w - 120, 110, 55); col(ctx, RED); ctx.fill(); text(ctx, 'Salva serie', w / 2, 936, 38, FONT, WHITE)
    return content

def loads_screen(p):
    def content(ctx, w, h):
        app_head(ctx, w, 'Progressi')
        text(ctx, 'Panca piana · carico', 40, 220, 36, FONT, INK, anchor='l')
        chart(ctx, 90, 300, w - 150, 420, p, lw=9, data=[50, 52.5, 52.5, 55, 57.5, 57.5, 60, 62.5], lo=45, hi=65)
        for i, (a, b) in enumerate((('RPE medio', '7,5'), ('Ultimo carico', '62,5 kg'))):
            y = 820 + i * 110
            rrect(ctx, 30, y, w - 60, 90, 24); col(ctx, SOFT); ctx.fill()
            text(ctx, a, 60, y + 46, 30, FONTB, GRAY, anchor='l'); text(ctx, b, w - 60, y + 46, 34, FONT, RED, anchor='r')
    return content

def rest_setting_screen(k):
    def content(ctx, w, h):
        app_head(ctx, w, 'Scheda')
        text(ctx, 'Squat', 40, 220, 42, FONT, INK, anchor='l'); text(ctx, '4 × 6 · 100 kg', 40, 275, 30, FONTB, GRAY, anchor='l')
        for i, (lab, val, on) in enumerate((('Serie', '4', 0), ('Ripetizioni', '6', 0), ('Recupero', "2' 30\"", 1))):
            y = 340 + i * 150
            rrect(ctx, 30, y, w - 60, 125, 24); col(ctx, LIGHT_RED if on and k > 0 else SOFT); ctx.fill()
            if on and k > 0: rrect(ctx, 30, y, w - 60, 125, 24); col(ctx, RED, k); ctx.set_line_width(7); ctx.stroke()
            text(ctx, lab, 60, y + 62, 34, FONTB, INK, anchor='l')
            ctx.save(); ctx.translate(w - 110, y + 62)
            if on: sscale(ctx, 1 + .2 * math.sin(clamp(k) * math.pi))
            text(ctx, val, 0, 0, 44, FONT, RED if on else INK); ctx.restore()
        text(ctx, 'Curl manubri · recupero 75"', w / 2, 860, 28, FONTB, GRAY)
    return content

def anamnesi_form_screen(p, filled):
    fields = ['Infortuni e dolori', 'Farmaci', 'Patologie', 'Esperienza', 'Obiettivi', 'Tempo disponibile']
    vals = ['Ernia L5-S1', 'Nessuno', 'Nessuna', '2 anni', 'Tonificare', '3 × 1 h']
    def content(ctx, w, h):
        app_head(ctx, w, 'Iscrizione')
        text(ctx, 'Anamnesi', 40, 215, 42, FONT, INK, anchor='l')
        for i, f in enumerate(fields):
            k = clamp(p * 6 - i)
            if k <= 0: continue
            y = 260 + i * 132
            text(ctx, f, 44, y + 20, 26, FONTB, GRAY, anchor='l')
            rrect(ctx, 30, y + 40, w - 60, 72, 18); fill_stroke(ctx, WHITE, 3)
            fk = clamp(filled * 6 - i)
            if fk > 0:
                n = int(len(vals[i]) * fk); text(ctx, vals[i][:n], 54, y + 77, 30, FONTB, RED if i == 0 else INK, anchor='l')
    return content

def client_card_screen(hl):
    def content(ctx, w, h):
        app_head(ctx, w, 'Clienti')
        ctx.arc(110, 260, 60, 0, 2 * math.pi); fill_stroke(ctx, (.75, .8, .9), 5)
        text(ctx, 'Marco Rossi', 200, 245, 40, FONT, INK, anchor='l'); text(ctx, 'Cliente da 3 giorni', 200, 292, 26, FONTB, GRAY, anchor='l')
        for i, (lab, on) in enumerate((('Schede', 0), ('Anamnesi', 1), ('Misure', 0), ('Pagamenti', 0))):
            y = 370 + i * 130
            rrect(ctx, 30, y, w - 60, 110, 24); col(ctx, LIGHT_RED if on and hl > 0 else SOFT); ctx.fill()
            if on and hl > 0: rrect(ctx, 30, y, w - 60, 110, 24); col(ctx, RED, hl); ctx.set_line_width(7); ctx.stroke()
            text(ctx, lab, 60, y + 56, 36, FONT, INK, anchor='l')
            if on: status_chip(ctx, w - 170, y + 56, 'Ernia L5-S1', RED, hl, 24)
    return content

WEEKS = [('S1', '3×8', '60'), ('S2', '3×10', '60'), ('S3', '4×10', '60'), ('S4', '3×8', '62,5')]
def editor_screen(p, hl=-1):
    def content(ctx, w, h):
        app_head(ctx, w, 'Editor scheda')
        text(ctx, 'Panca piana · progressione', 40, 215, 32, FONT, INK, anchor='l')
        cw = (w - 60) / 4
        for i, (s_, sr, kg) in enumerate(WEEKS):
            k = clamp(p * 4 - i)
            x = 30 + i * cw
            rrect(ctx, x + 6, 260, cw - 12, 520, 22); col(ctx, LIGHT_RED if i == hl else SOFT); ctx.fill()
            if i == hl: rrect(ctx, x + 6, 260, cw - 12, 520, 22); col(ctx, RED); ctx.set_line_width(6); ctx.stroke()
            text(ctx, s_, x + cw / 2, 310, 36, FONT, RED)
            if k > 0:
                ctx.save(); ctx.translate(x + cw / 2, 0); sscale(ctx, eback(k), 1)
                text(ctx, sr, 0, 440, 40, FONT, INK); text(ctx, 'serie×rip', 0, 490, 20, FONTB, GRAY)
                text(ctx, kg, 0, 610, 40, FONT, RED if kg != '60' else INK); text(ctx, 'kg', 0, 660, 20, FONTB, GRAY)
                ctx.restore()
        rrect(ctx, 60, 850, w - 120, 110, 55); col(ctx, RED); ctx.fill(); text(ctx, 'Salva progressione', w / 2, 906, 34, FONT, WHITE)
    return content

def client_week_screen(wk):
    s_, sr, kg = WEEKS[wk]
    def content(ctx, w, h):
        app_head(ctx, w, 'Oggi')
        rrect(ctx, 30, 190, w - 60, 90, 45); col(ctx, LIGHT_RED); ctx.fill()
        text(ctx, f'Settimana {wk + 1} di 4', w / 2, 236, 34, FONT, RED)
        text(ctx, 'Panca piana', 40, 350, 42, FONT, INK, anchor='l')
        text(ctx, sr, w / 2 - 120, 520, 110, FONT, INK); text(ctx, kg + ' kg', w / 2 + 150, 520, 70, FONT, RED)
        text(ctx, 'serie × ripetizioni', w / 2 - 120, 600, 26, FONTB, GRAY)
        rrect(ctx, 60, 860, w - 120, 110, 55); col(ctx, RED); ctx.fill(); text(ctx, 'Inizia', w / 2, 916, 38, FONT, WHITE)
    return content

def circuit_like_timer(frac, big, done=False):
    return timer_screen(frac, 'RECUPERO', big, done)

# ---------------------------------------------------------------- icone e oggetti
def icon(ctx, kind, c, s=1.0, k=1.0):
    if k <= 0: return
    ctx.save(); ctx.translate(*c); sscale(ctx, s * eback(clamp(k)))
    if kind == 'bulb':
        ctx.arc(0, -20, 70, 0, 2 * math.pi); fill_stroke(ctx, YELLOW, 8)
        rrect(ctx, -32, 45, 64, 50, 10); fill_stroke(ctx, GRAY, 6)
        for a in range(5):
            an = math.pi + a * math.pi / 4; poly(ctx, [(math.cos(an) * 95, -20 + math.sin(an) * 95), (math.cos(an) * 125, -20 + math.sin(an) * 125)], 7)
    elif kind == 'pose':
        draw_fig(ctx, 'client', P(la1=-40, la2=-30, ra1=40, ra2=30), dict(eyes='open', mouth='smile', brows='neutral'), 0, 110, 60, 0, seed=2, shadow=False)
    elif kind == 'dist':
        poly(ctx, [(-100, 60), (100, 60)], 8); poly(ctx, [(-100, 40), (-100, 80)], 8); poly(ctx, [(100, 40), (100, 80)], 8)
        text(ctx, '2 m', 0, 10, 56, FONT, RED)
    elif kind == 'clock':
        clock(ctx, (0, 0), 90, 1.2)
    elif kind == 'sun':
        ctx.arc(0, 20, 70, math.pi, 2 * math.pi); fill_stroke(ctx, YELLOW, 8); poly(ctx, [(-120, 20), (120, 20)], 8)
        for a in range(5):
            an = math.pi + (a + .5) * math.pi / 5; poly(ctx, [(math.cos(an) * 90, 20 + math.sin(an) * 90), (math.cos(an) * 125, 20 + math.sin(an) * 125)], 7)
    elif kind == 'mug':
        rrect(ctx, -60, -50, 120, 130, 16); fill_stroke(ctx, WHITE, 8); ctx.arc(70, 15, 32, -math.pi / 2, math.pi / 2); col(ctx, INK); ctx.set_line_width(10); ctx.stroke()
        text(ctx, '0', 0, 18, 50, FONT, GRAY)
    elif kind == 'moon':
        ctx.arc(0, 0, 80, 0, 2 * math.pi); fill_stroke(ctx, YELLOW, 8)
        ctx.arc(38, -24, 70, 0, 2 * math.pi); col(ctx, PAPERL); ctx.fill()
        text(ctx, 'z', 80, -70, 50, FONT, INK)
    elif kind == 'plate':
        ctx.arc(0, 0, 90, 0, 2 * math.pi); fill_stroke(ctx, WHITE, 8); ctx.arc(0, 0, 55, 0, 2 * math.pi); col(ctx, INK, .3); ctx.set_line_width(4); ctx.stroke()
        text(ctx, 'kcal', 0, 2, 40, FONT, RED)
    elif kind == 'pill':
        ctx.save(); ctx.rotate(-.6); rrect(ctx, -90, -38, 180, 76, 38); fill_stroke(ctx, WHITE, 8)
        ctx.save(); rrect(ctx, -90, -38, 180, 76, 38); ctx.clip(); ctx.rectangle(0, -40, 92, 80); col(ctx, RED); ctx.fill(); ctx.restore()
        rrect(ctx, -90, -38, 180, 76, 38); col(ctx, INK); ctx.set_line_width(8); ctx.stroke(); ctx.restore()
    elif kind == 'cross':
        rrect(ctx, -90, -90, 180, 180, 30); fill_stroke(ctx, WHITE, 8)
        ctx.rectangle(-22, -62, 44, 124); col(ctx, RED); ctx.fill(); ctx.rectangle(-62, -22, 124, 44); ctx.fill()
    elif kind == 'bolt':
        ctx.move_to(20, -100); ctx.line_to(-50, 10); ctx.line_to(0, 10); ctx.line_to(-20, 100); ctx.line_to(55, -20); ctx.line_to(5, -20); ctx.close_path()
        fill_stroke(ctx, YELLOW, 8)
    elif kind == 'dumbbell':
        dumbbell(ctx, (0, 0), 0, 1.3)
    elif kind == 'target':
        for i, cc in enumerate((RED, WHITE, RED, WHITE, RED)):
            ctx.arc(0, 0, 90 * (1 - i * .19), 0, 2 * math.pi); fill_stroke(ctx, cc, 5)
    elif kind == 'euro':
        ctx.arc(0, 0, 80, 0, 2 * math.pi); fill_stroke(ctx, YELLOW, 8); text(ctx, '€', 0, 4, 100, FONT, INK)
    ctx.restore()

def collector_cap(ctx, head, R, k=1.0):
    """berretto da esattore"""
    if k <= 0: return
    hx, hy = head; y = hy - R * .55 - (1 - eout(k)) * 260
    ctx.save(); ctx.translate(hx, y)
    rrect(ctx, -R * 1.0, -R * .62, R * 2.0, R * .62, R * .2); fill_stroke(ctx, (.18, .2, .3), 7)
    ell(ctx, R * .35, 0, R * .9, R * .18); fill_stroke(ctx, (.12, .13, .2), 6)
    rrect(ctx, -R * .3, -R * .5, R * .6, R * .38, 8); fill_stroke(ctx, YELLOW, 4)
    text(ctx, '€', 0, -R * .3, R * .32, FONT, INK)
    ctx.restore()

def money_bag(ctx, c, s=1.0):
    ctx.save(); ctx.translate(*c); sscale(ctx, s)
    ctx.move_to(-30, -70); ctx.curve_to(-100, -20, -110, 90, 0, 95); ctx.curve_to(110, 90, 100, -20, 30, -70); ctx.close_path()
    fill_stroke(ctx, (.78, .66, .45), 7)
    poly(ctx, [(-34, -70), (34, -70)], 10); text(ctx, '€', 0, 22, 80, FONT, INK)
    ctx.restore()

def whistle(ctx, c, s=1.0):
    ctx.save(); ctx.translate(*c); sscale(ctx, s)
    rrect(ctx, -60, -25, 80, 50, 22); fill_stroke(ctx, (.8, .82, .86), 6)
    ctx.arc(20, 10, 34, 0, 2 * math.pi); fill_stroke(ctx, (.8, .82, .86), 6)
    ctx.arc(20, 10, 12, 0, 2 * math.pi); col(ctx, INK); ctx.fill()
    ctx.restore()

def register(ctx, c, s=1.0, t=0.0):
    ctx.save(); ctx.translate(*c); sscale(ctx, s)
    rrect(ctx, -120, -40, 240, 130, 16); fill_stroke(ctx, (.55, .6, .7), 7)
    rrect(ctx, -90, -120, 180, 80, 12); fill_stroke(ctx, (.2, .25, .22), 6)
    text(ctx, '120 €', 0, -80, 38, FONT, (.5, 1, .6))
    for i in range(3):
        for j in range(4): rrect(ctx, -95 + j * 50, -20 + i * 32, 38, 22, 5); fill_stroke(ctx, WHITE, 3)
    ctx.restore()

def rope(ctx, a, b, fray, t=0.0):
    a = np.array(a, float); b = np.array(b, float)
    pts = []
    for i in range(31):
        u = i / 30; q = a + (b - a) * u; q[1] += math.sin(u * math.pi) * (40 + 40 * fray) + math.sin(t * 3 + u * 5) * 4
        pts.append(q)
    mid = 15
    if fray < .85:
        w = 18 * (1 - fray * .8)
        poly(ctx, pts, w + 8, INK); poly(ctx, pts, w, (.82, .65, .4))
    else:
        poly(ctx, pts[:mid - 1], 18, INK); poly(ctx, pts[:mid - 1], 10, (.82, .65, .4))
        poly(ctx, pts[mid + 1:], 18, INK); poly(ctx, pts[mid + 1:], 10, (.82, .65, .4))
    # fili sfilacciati
    m = pts[mid]
    for k in range(int(fray * 8)):
        ang = -math.pi / 2 + (k - 4) * .35
        poly(ctx, [m, m + np.array([math.cos(ang), math.sin(ang)]) * (25 + 30 * fray)], 3, (.6, .45, .25))

def month_card(ctx, x, y, w, circles, k=1.0, title='OTTOBRE', ck=None):
    """Calendario mensile con giorni cerchiati."""
    if k <= 0: return
    h = w * .95
    ctx.save(); ctx.translate(x + w / 2, y + h / 2); sscale(ctx, eback(clamp(k))); ctx.translate(-w / 2, -h / 2)
    rrect(ctx, 10, 12, w, h, 22); col(ctx, INK, .15); ctx.fill()
    rrect(ctx, 0, 0, w, h, 22); fill_stroke(ctx, PAPERL, 7)
    ctx.save(); rrect(ctx, 0, 0, w, h, 22); ctx.clip(); ctx.rectangle(0, 0, w, 100); col(ctx, RED); ctx.fill(); ctx.restore()
    text(ctx, title, w / 2, 52, 46, FONT, WHITE)
    cw = (w - 40) / 7; ch = (h - 140) / 5
    for d in range(1, 32):
        i = d - 1 + 2; r, c = divmod(i, 7)
        cx = 20 + c * cw + cw / 2; cy = 120 + r * ch + ch / 2
        text(ctx, str(d), cx, cy, 30, FONTB, INK)
        if d in circles:
            kk = 1.0 if ck is None else clamp(ck[circles.index(d)])
            if kk > 0:
                ctx.arc(cx, cy, 34, -math.pi / 2, -math.pi / 2 + 2 * math.pi * kk); col(ctx, RED); ctx.set_line_width(7); ctx.stroke()
    ctx.restore()

def flip_calendar(ctx, x, y, w, label, sub, flip, head='SETTIMANA'):
    """calendario a strappo: flip in [0,1) fa volare la pagina corrente"""
    h = w * 1.1
    rrect(ctx, x + 10, y + 12, w, h, 18); col(ctx, INK, .15); ctx.fill()
    rrect(ctx, x, y, w, h, 18); fill_stroke(ctx, PAPERL, 7)
    ctx.save(); rrect(ctx, x, y, w, h, 18); ctx.clip(); ctx.rectangle(x, y, w, 80); col(ctx, RED); ctx.fill(); ctx.restore()
    text(ctx, head, x + w / 2, y + 42, 32, FONT, WHITE)
    text(ctx, label, x + w / 2, y + h * .48, w * .36, FONT, INK)
    text(ctx, sub, x + w / 2, y + h * .8, w * .12, FONT, RED)
    if 0 < flip < 1:
        ctx.save(); ctx.translate(x + w / 2 + flip * 300, y + h / 2 - flip * 400); ctx.rotate(flip * 1.4)
        ctx.rectangle(-w / 2, -h / 2 + 80, w, h - 80); col(ctx, PAPERL, 1 - flip); ctx.fill_preserve(); col(ctx, INK, 1 - flip); ctx.set_line_width(5); ctx.stroke()
        ctx.restore()

def mixer(ctx, x, y, labels, vals, hl=-1):
    n = len(labels); w = 860; cw = w / n
    rrect(ctx, x - 20, y - 40, w + 40, 560, 30); fill_stroke(ctx, (.3, .3, .33), 8)
    for i, (lab, v) in enumerate(zip(labels, vals)):
        cx = x + i * cw + cw / 2
        rrect(ctx, cx - 10, y + 20, 20, 360, 10); col(ctx, INK); ctx.fill()
        ky = y + 20 + 360 * (1 - clamp(v))
        rrect(ctx, cx - 60, ky - 28, 120, 56, 14); fill_stroke(ctx, RED if i == hl else WHITE, 6)
        text(ctx, lab, cx, y + 450, 30 if len(lab) < 10 else 24, FONT, YELLOW if i == hl else WHITE)

def checklist(ctx, x, y, w, items, ks, row=110):
    h = 40 + row * len(items)
    rrect(ctx, x + 8, y + 10, w, h, 24); col(ctx, INK, .15); ctx.fill()
    rrect(ctx, x, y, w, h, 24); fill_stroke(ctx, PAPERL, 7)
    for i, (ic, lab) in enumerate(items):
        yy = y + 20 + i * row + row / 2
        k = clamp(ks[i]) if i < len(ks) else 0
        rrect(ctx, x + 30, yy - 32, 64, 64, 14); fill_stroke(ctx, WHITE, 5)
        if k > 0: check(ctx, (x + 62, yy), .55 * eback(k))
        icon(ctx, ic, (x + 150, yy), .38, 1 if k > 0 else .0001)
        text(ctx, lab, x + 220, yy, 40, FONT, INK if k > 0 else GRAY, anchor='l')

def table_cols(ctx, x, y, w, h, cols, ks, hl=-1):
    """Colonne S1..S4 per la progressione."""
    cw = w / len(cols)
    for i, (head, a, b) in enumerate(cols):
        k = clamp(ks[i])
        cx = x + i * cw
        rrect(ctx, cx + 8, y, cw - 16, h, 24); fill_stroke(ctx, LIGHT_RED if i == hl else PAPERL, 6, RED if i == hl else INK)
        text(ctx, head, cx + cw / 2, y + 50, 44, FONT, RED)
        if k > 0:
            ctx.save(); ctx.translate(cx + cw / 2, y + h * .48); sscale(ctx, eback(k)); text(ctx, a, 0, 0, 52, FONT, INK); ctx.restore()
            ctx.save(); ctx.translate(cx + cw / 2, y + h * .78); sscale(ctx, eback(k)); text(ctx, b, 0, 0, 40, FONT, RED if '62' in b else GRAY); ctx.restore()

def euro_crossed(ctx, c, s=1.0):
    icon(ctx, 'euro', c, s); xmark(ctx, c, .9 * s)

def stopwatch_big(ctx, c, r, txt, sweep, cc=INK):
    """orologio da muro con lancetta e cifra"""
    clock(ctx, c, r, sweep)
    plate_label(ctx, (c[0], c[1] + r + 60), txt, 1, bg=RED, tc=WHITE, size=46)

def vibrate_lines(ctx, c, w, h, t, a=1.0):
    for sx in (-1, 1):
        for i in range(3):
            k = (t * 4 + i * .3) % 1
            x = c[0] + sx * (w / 2 + 20 + i * 22)
            poly(ctx, [(x, c[1] - 40 + 6 * math.sin(t * 40)), (x, c[1] + 40 + 6 * math.sin(t * 40))], 6, INK, a * (1 - k))
