"""Il Narratore: conduttore di documentari pieno di sé (personaggio originale iki).
Mezzo busto in stile cartoon a contorno spesso: ciuffo argento, mascella quadrata con fossetta,
sopracciglio alzato, sorriso a 32 denti con scintilla, camicia da safari con fazzoletto rosso e binocolo.
Stati: 'smug' (legge il telefono compiaciuto), 'cough' (pugno alla bocca), 'sorry' (sorriso forzato, sudore),
'panic' (scappa)."""
import math
from engine import INK, WHITE, RED, col

SKIN = (.93, .72, .55); SKIN_D = (.80, .56, .40); HAIR = (.86, .87, .90); HAIR_D = (.62, .64, .70)
BROW = (.30, .29, .32); KHAKI = (.78, .68, .46); KHAKI_D = (.62, .52, .33); BLUSH = (.95, .45, .42)
LW = 8


def _fs(ctx, fillc, w=LW):
    col(ctx, fillc); ctx.fill_preserve(); col(ctx, INK); ctx.set_line_width(w)
    ctx.set_line_join(1); ctx.set_line_cap(1); ctx.stroke()


def _line(ctx, pts, w=LW, c=INK):
    ctx.move_to(*pts[0])
    for p in pts[1:]: ctx.line_to(*p)
    col(ctx, c); ctx.set_line_width(w); ctx.set_line_cap(1); ctx.set_line_join(1); ctx.stroke()


def _curve(ctx, a, b, c, d, w=LW, cc=INK):
    ctx.move_to(*a); ctx.curve_to(*b, *c, *d); col(ctx, cc); ctx.set_line_width(w); ctx.set_line_cap(1); ctx.stroke()


def _limb(ctx, pts, width, fillc):
    """Braccio a tubo: contorno nero + riempimento."""
    for w, c in ((width + 2 * LW, INK), (width, fillc)):
        ctx.move_to(*pts[0])
        if len(pts) == 3:
            ctx.curve_to(*pts[1], *pts[1], *pts[2])
        else:
            for p in pts[1:]: ctx.line_to(*p)
        col(ctx, c); ctx.set_line_width(w); ctx.set_line_cap(1); ctx.set_line_join(1); ctx.stroke()


def _hand(ctx, x, y, r=46, fist=False):
    ctx.save(); ctx.translate(x, y)
    if fist:
        ctx.move_to(-r, -r * .5); ctx.curve_to(-r, -r * 1.1, r, -r * 1.1, r, -r * .4)
        ctx.curve_to(r * 1.1, r * .7, -r, r * .9, -r, -r * .5); ctx.close_path(); _fs(ctx, SKIN)
        for i in range(3): _curve(ctx, (-r * .6 + i * r * .55, -r * .55), (-r * .6 + i * r * .55, -r * .2), (-r * .6 + i * r * .55, -r * .2), (-r * .55 + i * r * .55, 0), 5)
    else:
        ctx.arc(0, 0, r, 0, 2 * math.pi); _fs(ctx, SKIN)
    ctx.restore()


def _phone(ctx, x, y, rot, glow):
    ctx.save(); ctx.translate(x, y); ctx.rotate(rot)
    if glow:
        col(ctx, (.6, .8, 1), .25 * glow); ctx.arc(0, 0, 150, 0, 2 * math.pi); ctx.fill()
    ctx.rectangle(-55, -105, 110, 210); _fs(ctx, (.15, .15, .18))
    ctx.rectangle(-44, -90, 88, 175); col(ctx, (.75, .87, 1)); ctx.fill()
    ctx.restore()


def _head(ctx, mood, t, blink):
    # orecchie
    for sx in (-1, 1):
        ctx.save(); ctx.scale(sx, 1); ctx.arc(150, 10, 36, 0, 2 * math.pi); _fs(ctx, SKIN); ctx.restore()
    # collo
    ctx.rectangle(-62, 140, 124, 150); _fs(ctx, SKIN)
    # viso: mascella quadrata con fossetta
    ctx.move_to(-135, -130); ctx.curve_to(-150, -20, -150, 80, -118, 150)
    ctx.curve_to(-95, 195, -40, 212, -10, 214); ctx.line_to(0, 200); ctx.line_to(10, 214)
    ctx.curve_to(40, 212, 95, 195, 118, 150); ctx.curve_to(150, 80, 150, -20, 135, -130)
    ctx.curve_to(80, -175, -80, -175, -135, -130); ctx.close_path(); _fs(ctx, SKIN)
    _curve(ctx, (0, 200), (-3, 185), (3, 180), (0, 172), 5)                     # fossetta sul mento
    # guance rosse quando tossisce o si vergogna
    if mood in ('cough', 'sorry', 'panic'):
        for sx in (-1, 1):
            col(ctx, BLUSH, .55); ctx.save(); ctx.translate(sx * 85, 70); ctx.scale(1.4, .8); ctx.arc(0, 0, 26, 0, 2 * math.pi); ctx.restore(); ctx.fill()
    # ciuffo argento a onda (vanitoso)
    ctx.move_to(-150, -20); ctx.curve_to(-175, -170, -110, -255, -10, -262)
    ctx.curve_to(90, -270, 175, -235, 168, -170); ctx.curve_to(160, -130, 120, -150, 95, -175)
    ctx.curve_to(60, -150, 0, -150, -60, -160); ctx.curve_to(-100, -150, -120, -110, -128, -40)
    ctx.close_path(); _fs(ctx, HAIR)
    for a, b, c, d in (((-120, -150), (-90, -230), (20, -245), (110, -215)), ((-60, -190), (-20, -225), (60, -230), (130, -195))):
        _curve(ctx, a, b, c, d, 5, HAIR_D)
    _curve(ctx, (95, -180), (130, -150), (120, -110), (95, -105), 6)              # ciocca ribelle
    # basette
    for sx in (-1, 1):
        ctx.save(); ctx.scale(sx, 1); ctx.move_to(-140, -60); ctx.line_to(-128, 20); ctx.line_to(-118, 20); ctx.line_to(-122, -60); ctx.close_path(); _fs(ctx, HAIR, 5); ctx.restore()
    # sopracciglia
    if mood == 'smug':
        _line(ctx, [(-100, -62), (-35, -58)], 18, BROW); _line(ctx, [(30, -78), (100, -100)], 18, BROW)   # uno alzato
    elif mood == 'cough':
        _line(ctx, [(-100, -55), (-35, -45)], 18, BROW); _line(ctx, [(35, -45), (100, -55)], 18, BROW)
    else:
        _line(ctx, [(-100, -55), (-35, -75)], 18, BROW); _line(ctx, [(35, -75), (100, -55)], 18, BROW)   # preoccupate
    # occhi
    for sx, ex in ((-1, -65), (1, 65)):
        if mood == 'cough' or blink:
            _curve(ctx, (ex - 32, -15), (ex - 15, -5 if blink else 5), (ex + 15, -5 if blink else 5), (ex + 32, -15), 7)
            continue
        h = 30 if mood == 'panic' else 24
        ctx.save(); ctx.translate(ex, -15); ctx.scale(1, h / 30); ctx.arc(0, 0, 30, 0, 2 * math.pi); ctx.restore(); _fs(ctx, WHITE, 6)
        px = {'smug': 6, 'sorry': 0, 'panic': 12}[mood]; py = {'smug': 10, 'sorry': 2, 'panic': 0}[mood]
        ctx.arc(ex + px, -15 + py, 10 if mood == 'panic' else 12, 0, 2 * math.pi); col(ctx, INK); ctx.fill()
        if mood == 'smug':                                                         # palpebra a mezz'asta: sguardo compiaciuto
            ctx.save(); ctx.translate(ex, -15); ctx.scale(1, h / 30)
            ctx.rectangle(-36, -36, 72, 34); ctx.restore(); col(ctx, SKIN); ctx.fill()
            _line(ctx, [(ex - 32, -18), (ex + 32, -16)], 7)
    # naso
    _curve(ctx, (-5, 0), (-25, 55), (-15, 70), (12, 66), 6)
    # bocca
    if mood == 'smug':
        ctx.move_to(-82, 98); ctx.curve_to(-40, 110, 40, 110, 88, 88); ctx.curve_to(70, 150, -60, 158, -82, 98)
        ctx.close_path(); _fs(ctx, WHITE, 7)
        _curve(ctx, (-76, 112), (-30, 122), (30, 120), (80, 104), 4)
        for x in (-45, -15, 15, 45): _line(ctx, [(x, 106), (x, 130)], 3)
        # scintilla sui denti
        k = (t * 2.2) % 1.0
        if k < .35:
            s = math.sin(k / .35 * math.pi) * 28
            ctx.save(); ctx.translate(95, 70)
            for a in range(4):
                ctx.rotate(math.pi / 4); ctx.move_to(0, -s); ctx.line_to(4, 0); ctx.line_to(0, s); ctx.line_to(-4, 0); ctx.close_path()
                col(ctx, WHITE); ctx.fill_preserve(); col(ctx, INK); ctx.set_line_width(2); ctx.stroke()
            ctx.restore()
    elif mood == 'sorry':                                                         # sorriso forzato a denti stretti
        ctx.rectangle(-70, 100, 140, 36); _fs(ctx, WHITE, 7)
        _line(ctx, [(-70, 118), (70, 118)], 4)
        for x in (-35, 0, 35): _line(ctx, [(x, 100), (x, 136)], 3)
    elif mood == 'panic':
        ctx.save(); ctx.translate(0, 120); ctx.scale(1, 1.2); ctx.arc(0, 0, 28, 0, 2 * math.pi); ctx.restore(); _fs(ctx, (.45, .12, .12), 7)
    else:  # cough: bocca nascosta dal pugno
        _curve(ctx, (-40, 115), (-15, 130), (15, 100), (40, 115), 7)


def draw_host(ctx, t, mood='smug', x=540, base=1790, lean=0.0, jolt=0.0, phone_glow=1.0, sweat=0.0):
    """Mezzo busto. (x, base) = centro in basso; lean in radianti."""
    blink = mood in ('smug', 'sorry') and (t % 3.7) < .1
    bob = math.sin(t * 2.4) * 4
    ctx.save(); ctx.translate(x + jolt, base); ctx.rotate(lean); ctx.translate(0, bob)
    # busto: camicia da safari
    ctx.move_to(-300, 0); ctx.curve_to(-300, -330, -280, -560, -200, -590); ctx.line_to(200, -590)
    ctx.curve_to(280, -560, 300, -330, 300, 0); ctx.close_path(); _fs(ctx, KHAKI)
    for sx in (-1, 1):                                                            # spalline
        ctx.save(); ctx.scale(sx, 1); ctx.rectangle(-255, -585, 110, 34); _fs(ctx, KHAKI_D, 6); ctx.restore()
        ctx.save(); ctx.scale(sx, 1); ctx.rectangle(-210, -410, 120, 130); _fs(ctx, KHAKI, 6)   # taschini
        ctx.rectangle(-218, -420, 136, 42); _fs(ctx, KHAKI_D, 6); ctx.restore()
    _line(ctx, [(0, -520), (0, 0)], 6)
    for y in (-450, -330, -210, -90): ctx.arc(14, y, 8, 0, 2 * math.pi); _fs(ctx, WHITE, 4)
    # colletto + fazzoletto rosso
    ctx.move_to(-90, -600); ctx.line_to(0, -470); ctx.line_to(90, -600); ctx.line_to(60, -610); ctx.line_to(0, -540); ctx.line_to(-60, -610); ctx.close_path(); _fs(ctx, RED)
    for sx in (-1, 1):
        ctx.save(); ctx.scale(sx, 1); ctx.move_to(-60, -610); ctx.line_to(-190, -585); ctx.line_to(-110, -510); ctx.line_to(-25, -560); ctx.close_path(); _fs(ctx, KHAKI_D, 6); ctx.restore()
    # binocolo al collo
    _curve(ctx, (-110, -590), (-120, -420), (120, -420), (110, -590), 5)
    for sx in (-1, 1):
        ctx.save(); ctx.translate(sx * 42, -330); ctx.rectangle(-30, -60, 60, 100); _fs(ctx, (.2, .2, .22), 6)
        ctx.arc(0, 40, 26, 0, 2 * math.pi); _fs(ctx, (.45, .55, .65), 5); ctx.restore()
    # testa
    ctx.save(); ctx.translate(0, -880); ctx.scale(1.12, 1.12)
    if mood == 'cough': ctx.rotate(.08)
    _head(ctx, mood, t, blink)
    if sweat > 0:
        ctx.save(); ctx.translate(150, -150); ctx.scale(1.4 * sweat, 1.4 * sweat)
        ctx.move_to(0, -24); ctx.curve_to(8, -8, 14, 0, 14, 8); ctx.arc(0, 8, 14, 0, math.pi); ctx.curve_to(-14, 0, -8, -8, 0, -24)
        ctx.restore(); _fs(ctx, (.72, .87, .98), 5)
    ctx.restore()
    # braccio destro (a sinistra dello schermo) col telefono
    if mood == 'panic':
        _limb(ctx, [(-250, -520), (-420, -620), (-330, -760)], 92, KHAKI); _phone(ctx, -330, -850, -.4, phone_glow); _hand(ctx, -330, -770)
    else:
        _limb(ctx, [(-250, -520), (-330, -230), (-170, -380)], 92, KHAKI); _phone(ctx, -150, -500, -.25, phone_glow); _hand(ctx, -160, -395)
    # braccio sinistro: pugno alla bocca quando tossisce
    if mood == 'cough':
        _limb(ctx, [(250, -520), (330, -300), (60, -730)], 92, KHAKI); _hand(ctx, 20, -755, 50, fist=True)
    elif mood == 'panic':
        _limb(ctx, [(250, -520), (420, -600), (360, -760)], 92, KHAKI); _hand(ctx, 360, -770)
    ctx.restore()
