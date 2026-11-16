"""Oggetti aggiuntivi per i reel 08-14."""
from engine import *

MUSCLES = ['Petto', 'Schiena', 'Spalle', 'Braccia', 'Gambe', 'Glutei']

def callout(ctx, src, c, r, content, k=1.0, r0=46):
    if k <= 0: return
    c = src + (c - src) * eout(k); r = r * eback(k)
    d = c - src; L_ = np.linalg.norm(d); u = d / L_; n = np.array([-u[1], u[0]])
    ang = math.asin(clamp((r - r0) / L_, -1, 1))
    for sgn in (-1, 1):
        dd = np.array([-u[0] * math.sin(ang) + sgn * n[0] * math.cos(ang), -u[1] * math.sin(ang) + sgn * n[1] * math.cos(ang)])
        poly(ctx, [src + dd * r0, c + dd * r], 5, INK, .8)
    ctx.arc(*src, r0, 0, 2 * math.pi); col(ctx, INK); ctx.set_line_width(6); ctx.stroke()
    ctx.arc(*(c + np.array([10, 14])), r + 10, 0, 2 * math.pi); col(ctx, INK, .18); ctx.fill()
    ctx.save(); ctx.arc(*c, r, 0, 2 * math.pi); ctx.clip()
    col(ctx, (.97, .93, .9)); ctx.paint(); content(ctx, c, r)
    ctx.restore()
    ctx.arc(*c, r, 0, 2 * math.pi); col(ctx, INK); ctx.set_line_width(12); ctx.stroke()

def radar(ctx, c, r, vals, p=1.0, labels=MUSCLES, lo=10, hi=20, vmax=26, label_size=30, show_zone=True):
    n = len(labels)
    angs = [-math.pi / 2 + i * 2 * math.pi / n for i in range(n)]
    def pt(i, v): return np.array(c) + np.array([math.cos(angs[i]), math.sin(angs[i])]) * r * v / vmax
    if show_zone:
        ctx.move_to(*pt(0, hi))
        for i in range(1, n): ctx.line_to(*pt(i, hi))
        ctx.close_path()
        ctx.move_to(*pt(0, lo))
        for i in range(n - 1, 0, -1): ctx.line_to(*pt(i, lo))
        ctx.close_path()
        ctx.set_fill_rule(cairo.FILL_RULE_EVEN_ODD); col(ctx, GREEN, .16); ctx.fill(); ctx.set_fill_rule(cairo.FILL_RULE_WINDING)
    for lev in (.33, .66, 1.0):
        ctx.move_to(*pt(0, vmax * lev))
        for i in range(1, n): ctx.line_to(*pt(i, vmax * lev))
        ctx.close_path(); col(ctx, INK, .18); ctx.set_line_width(2.5); ctx.stroke()
    for i in range(n):
        poly(ctx, [c, pt(i, vmax)], 2.5, INK, .18)
        q = np.array(c) + np.array([math.cos(angs[i]), math.sin(angs[i])]) * (r + label_size * 1.3)
        text(ctx, labels[i], q[0], q[1], label_size, FONTB, INK)
    if p > 0:
        ctx.move_to(*pt(0, vals[0] * p))
        for i in range(1, n): ctx.line_to(*pt(i, vals[i] * p))
        ctx.close_path(); col(ctx, RED, .25); ctx.fill_preserve(); col(ctx, RED); ctx.set_line_width(6); ctx.stroke()
        for i in range(n):
            ctx.arc(*pt(i, vals[i] * p), 9, 0, 2 * math.pi); fill_stroke(ctx, WHITE, 4, RED)

def radar_screen(vals, p, title='Volume settimanale', hl=None):
    def content(ctx, w, h):
        ctx.rectangle(0, 0, w, 150); col(ctx, RED); ctx.fill()
        logo(ctx, 115, 78, 118, 'bianco'); text(ctx, title, w - 40, 92, 30, FONTB, WHITE, anchor='r')
        radar(ctx, (w / 2, 560), 210, vals, p)
        for i, (m, v) in enumerate(zip(MUSCLES, vals)):
            y = 900 + (i // 2) * 70; x = 40 + (i % 2) * (w - 80) / 2
            ok = 10 <= v <= 20
            rrect(ctx, x, y - 26, (w - 100) / 2, 52, 26); col(ctx, (1, .93, .92) if not ok else (.9, .97, .92), clamp(p * 2)); ctx.fill()
            text(ctx, f'{m} {int(round(v * p))}', x + 24, y, 28, FONTB, INK, anchor='l')
            if hl == i and p > .9:
                rrect(ctx, x - 4, y - 30, (w - 100) / 2 + 8, 60, 30); col(ctx, RED); ctx.set_line_width(5); ctx.stroke()
    return content

def week_strip(ctx, x, y, w, labels=('LUN', 'MAR', 'MER', 'GIO', 'VEN', 'SAB', 'DOM'), fills=None, a=1.0, h=150):
    n = len(labels); cw = w / n
    for i, lab in enumerate(labels):
        cx = x + i * cw
        rrect(ctx, cx + 6, y + 6, cw - 12, h, 18); col(ctx, INK, .12 * a); ctx.fill()
        rrect(ctx, cx, y, cw - 12, h, 18); col(ctx, PAPERL, a); ctx.fill_preserve(); col(ctx, INK, a); ctx.set_line_width(5); ctx.stroke()
        rrect(ctx, cx, y, cw - 12, 46, 18); col(ctx, RED, a); ctx.fill()
        ctx.rectangle(cx, y + 28, cw - 12, 18); col(ctx, RED, a); ctx.fill()
        text(ctx, lab, cx + (cw - 12) / 2, y + 24, 24, FONT, WHITE)
        if fills and fills.get(i):
            txt, k = fills[i]
            if k > 0:
                ctx.save(); ctx.translate(cx + (cw - 12) / 2, y + 98); sscale(ctx, eback(k))
                text(ctx, txt, 0, 0, 26 if len(txt) > 3 else 34, FONT, INK); ctx.restore()

def list_card(ctx, x, y, w, items, row_h=96, hl=None, a=1.0, title='SCHEDA', ypos=None):
    """items = lista di stringhe; ypos = posizioni (in righe) per animare il riordino"""
    h = 110 + row_h * len(items) + 30
    rrect(ctx, x + 8, y + 10, w, h, 22); col(ctx, INK, .15 * a); ctx.fill()
    rrect(ctx, x, y, w, h, 22); col(ctx, PAPERL, a); ctx.fill_preserve(); col(ctx, INK, a); ctx.set_line_width(6); ctx.stroke()
    rrect(ctx, x, y, w, 90, 22); col(ctx, RED, a); ctx.fill(); ctx.rectangle(x, y + 60, w, 30); ctx.fill()
    text(ctx, title, x + w / 2, y + 46, 40, FONT, WHITE)
    for i, it in enumerate(items):
        row = ypos[i] if ypos else i
        yy = y + 120 + row * row_h
        on = hl is not None and i == hl
        rrect(ctx, x + 20, yy, w - 40, row_h - 16, 18)
        col(ctx, (1, .9, .88) if on else WHITE, a); ctx.fill_preserve(); col(ctx, RED if on else INK, a); ctx.set_line_width(5 if on else 3); ctx.stroke()
        text(ctx, str(int(round(row)) + 1 if ypos else i + 1), x + 70, yy + (row_h - 16) / 2, 40, FONT, RED if on else GRAY)
        text(ctx, it, x + 120, yy + (row_h - 16) / 2, 36, FONTB, INK, anchor='l')

def range_bar(ctx, x, y, w, vmax=30, zone=(10, 20), marker=None, mk_label=None, a=1.0, ticks=(0, 10, 20, 30)):
    h = 56
    rrect(ctx, x, y, w, h, h / 2); col(ctx, (.92, .9, .86), a); ctx.fill()
    z0 = x + w * zone[0] / vmax; z1 = x + w * zone[1] / vmax
    rrect(ctx, z0, y, z1 - z0, h, 14); col(ctx, GREEN, .85 * a); ctx.fill()
    rrect(ctx, x, y, w, h, h / 2); col(ctx, INK, a); ctx.set_line_width(5); ctx.stroke()
    for tv in ticks:
        tx = x + w * tv / vmax
        text(ctx, str(tv), tx, y + h + 40, 34, FONTB, INK)
    if marker is not None:
        mx = x + w * clamp(marker / vmax)
        ctx.move_to(mx, y - 8); ctx.line_to(mx - 26, y - 52); ctx.line_to(mx + 26, y - 52); ctx.close_path()
        fill_stroke(ctx, RED, 4)
        if mk_label: text(ctx, mk_label, mx, y - 90, 40, FONT, RED, stroke=WHITE, sw=8)

def battery(ctx, c, level, s=1.0):
    ctx.save(); ctx.translate(*c); sscale(ctx, s)
    rrect(ctx, -90, -45, 180, 90, 16); fill_stroke(ctx, WHITE, 7)
    rrect(ctx, 90, -18, 16, 36, 6); fill_stroke(ctx, INK, 4)
    lv = clamp(level); cc = GREEN if lv > .5 else (YELLOW if lv > .25 else RED)
    if lv > 0: rrect(ctx, -78, -33, 156 * lv, 66, 10); col(ctx, cc); ctx.fill()
    ctx.restore()

def bike(ctx, x, g, t, rider_face=None, s=1.0, pedal=True):
    """bici di lato con omino che pedala (verso destra)"""
    ctx.save(); ctx.translate(x, g); sscale(ctx, s)
    rw = 95
    for wx in (-170, 170):
        ctx.arc(wx, -rw, rw, 0, 2 * math.pi); col(ctx, INK); ctx.set_line_width(12); ctx.stroke()
        ctx.arc(wx, -rw, 14, 0, 2 * math.pi); col(ctx, INK); ctx.fill()
        for k in range(6):
            a = t * 6 + k * math.pi / 3
            poly(ctx, [(wx, -rw), (wx + math.cos(a) * (rw - 8), -rw + math.sin(a) * (rw - 8))], 2.5, INK, .5)
    bb = np.array([0, -rw]); seat = np.array([-60, -300]); head = np.array([130, -330])
    poly(ctx, [(-170, -rw), bb, (170, -rw)], 10, RED); poly(ctx, [bb, seat], 10, RED); poly(ctx, [seat, head], 10, RED); poly(ctx, [(170, -rw), head], 10, RED)
    poly(ctx, [seat + np.array([-40, -10]), seat + np.array([40, -10])], 16, INK)
    poly(ctx, [head, head + np.array([10, -50]), head + np.array([-40, -60])], 9, INK)
    # omino
    U_ = 150
    hip = seat + np.array([0, -20]); sh = hip + np.array([90, -150]); hd = sh + np.array([40, -95])
    pa = t * 2 * math.pi * 1.4 if pedal else 0
    for ph, al in ((0, .55), (math.pi, 1)):
        foot = bb + np.array([math.cos(pa + ph), math.sin(pa + ph)]) * 55
        d = foot - hip; L_ = np.linalg.norm(d); l1 = .72 * U_; l2 = .74 * U_
        cosk = clamp((l1 * l1 + L_ * L_ - l2 * l2) / (2 * l1 * L_), -1, 1)
        base = math.atan2(d[1], d[0]); kang = base - math.acos(cosk)
        knee = hip + np.array([math.cos(kang), math.sin(kang)]) * l1
        poly(ctx, [hip, knee, foot], .085 * U_, INK, al)
        ell(ctx, foot[0] + 10, foot[1], 22, 10); col(ctx, INK, al); ctx.fill()
    poly(ctx, [hip, sh], .085 * U_)
    poly(ctx, [sh, head + np.array([-30, -55])], .085 * U_)
    ctx.arc(*(head + np.array([-30, -55])), .085 * U_, 0, 2 * math.pi); col(ctx, INK); ctx.fill()
    R = .46 * U_
    ctx.save(); ctx.translate(*hd); ctx.arc(0, 0, R, 0, 2 * math.pi); fill_stroke(ctx, WHITE, .085 * U_)
    draw_face(ctx, R, rider_face or dict(eyes='happy', mouth='grin', brows='raised'), t, .5, .085 * U_, 5)
    hair(ctx, R, .085 * U_, t, 5)
    ctx.save(); ctx.arc(0, 0, R - 5, 0, 2 * math.pi); ctx.clip()
    ctx.move_to(-R, -.72 * R); ctx.curve_to(-.3 * R, -.62 * R, .3 * R, -.62 * R, R, -.72 * R)
    ctx.line_to(R, -.53 * R); ctx.curve_to(.3 * R, -.43 * R, -.3 * R, -.43 * R, -R, -.53 * R); ctx.close_path(); fill_stroke(ctx, BLUE, 4)
    ctx.restore(); ctx.restore()
    ctx.restore()

def timer_screen(frac, label='RECUPERO', big='2:00', done=False):
    def content(ctx, w, h):
        ctx.rectangle(0, 0, w, 150); col(ctx, RED); ctx.fill()
        logo(ctx, 115, 78, 118, 'bianco'); text(ctx, 'Timer', w - 40, 92, 30, FONTB, WHITE, anchor='r')
        c = (w / 2, 560); r = 220
        ctx.arc(*c, r, 0, 2 * math.pi); col(ctx, (.93, .91, .88)); ctx.set_line_width(36); ctx.stroke()
        if frac > 0:
            ctx.arc(*c, r, -math.pi / 2, -math.pi / 2 + 2 * math.pi * frac); col(ctx, GREEN if done else RED); ctx.set_line_width(36); ctx.stroke()
        text(ctx, big, c[0], c[1] - 10, 110, FONT, GREEN if done else INK)
        text(ctx, label, c[0], c[1] + 90, 36, FONTB, GRAY)
    return content

def scale_balance(ctx, c, tilt, left_lab, right_lab, left_c=YELLOW, right_c=RED, s=1.0):
    x, y = c
    ctx.save(); ctx.translate(x, y); sscale(ctx, s)
    poly(ctx, [(0, 460), (0, 0)], 16); rrect(ctx, -130, 450, 260, 30, 10); fill_stroke(ctx, DARK, 6)
    a = math.radians(tilt); d = np.array([math.cos(a), math.sin(a)]) * 320
    Lp, Rp = -d, d
    poly(ctx, [Lp, Rp], 18); ctx.arc(0, 0, 22, 0, 2 * math.pi); fill_stroke(ctx, RED, 6)
    for p, lab, cc in ((Lp, left_lab, left_c), (Rp, right_lab, right_c)):
        poly(ctx, [p, p + np.array([-110, 210])], 4); poly(ctx, [p, p + np.array([110, 210])], 4)
        ctx.move_to(p[0] - 150, p[1] + 210); ctx.curve_to(p[0] - 110, p[1] + 280, p[0] + 110, p[1] + 280, p[0] + 150, p[1] + 210); ctx.close_path()
        fill_stroke(ctx, (.8, .8, .8), 6)
        plate_label(ctx, p + np.array([0, 160]), lab, 1, bg=cc, tc=WHITE if cc != YELLOW else INK, size=36)
    ctx.restore()

def stamp(ctx, c, txt, k, cc=RED, size=110, rot=-.12):
    if k <= 0: return
    s_ = 1 + 1.4 * (1 - eout(k))
    ctx.save(); ctx.translate(*c); ctx.rotate(rot); sscale(ctx, s_)
    ctx.select_font_face(FONT); ctx.set_font_size(size); w = ctx.text_extents(txt).width + 70
    rrect(ctx, -w / 2, -size * .8, w, size * 1.6, 24)
    col(ctx, cc, clamp(k * 2)); ctx.set_line_width(14); ctx.stroke()
    text(ctx, txt, 0, 0, size, FONT, cc)
    ctx.restore()

def fig(ctx, kind, pose, face, x, tau, fx=0.0, seed=0, U_=None, g=None, **kw):
    return draw_anim(ctx, kind, pose, face, x, g or G, U_ or U, tau, fx=fx, seed=seed, **kw)

def hold_dumbbell(ctx, A, side='R', ang=8, s=.95):
    h = A['h' + side]
    dumbbell(ctx, h, ang, s); ctx.arc(*h, .085 * U, 0, 2 * math.pi); col(ctx, INK); ctx.fill()

def curl(freq, strain=0.0):
    def pose(t):
        c = .5 - .5 * math.cos(2 * math.pi * freq * max(t, 0))
        sh = math.sin(t * 45) * 3 * strain
        return P(t=-2 + 5 * strain, h=-5 + 10 * strain, ra1=18 + sh, ra2=15 + 150 * c + sh, la1=-14, la2=-8)
    return pose

def squat_bar(freq, depth=1.0):
    """squat col bilanciere dietro il collo (vista frontale)"""
    def pose(t):
        sq = (.5 - .5 * math.cos(2 * math.pi * freq * max(t, 0))) * depth
        return P(t=0, h=-4 * sq, la1=-40, la2=-150, ra1=40, ra2=150,
                 ll1=lerp(-12, -78, sq), ll2=lerp(-6, -8, sq), rl1=lerp(12, 78, sq), rl2=lerp(6, 8, sq))
    return pose

def draw_bar_on(ctx, A, x, pose_t, plates=1.0, s=1.1, shake=0.0):
    """bilanciere sulle spalle: A dai joints posizionati (draw_anim)"""
    y = (A['hL'][1] + A['hR'][1]) / 2 + 4
    ctx.save(); ctx.translate(x + shake, y); sscale(ctx, s)
    poly(ctx, [(-300, 0), (300, 0)], 10)
    for sx in (-1, 1):
        n = max(1, int(round(3 * plates)))
        for i in range(n):
            px = sx * (205 + i * 24)
            rrect(ctx, px - 11, -75 + i * 6, 22, 150 - i * 12, 7); fill_stroke(ctx, DARK, 5)
    ctx.restore()
