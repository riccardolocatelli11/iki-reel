"""Copertine dei reel pubblicati prima che il motore le facesse da solo (fino al reel 30).

    python3 copertine_archivio.py            # tutte, in out/copertine/
    python3 copertine_archivio.py 2026-10-09 # solo quella di quel giorno

Instagram non permette di cambiare la copertina di un reel già pubblicato via API:
queste si caricano a mano dall'app (reel > ... > Modifica > Modifica copertina > Aggiungi dalla galleria).
"""
import sys, os, math, importlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from props4 import *

OUT = os.path.join(HERE, 'out', 'copertine')

def face(e='open', m='smile', b='neutral', look=(0, 0)):
    return dict(eyes=e, mouth=m, brows=b, look=look)

def stand(**kw):
    return lambda t: P(**kw)

def pt(ctx, x, f, pose=None, s=.9, fx=0.0):
    return fig(ctx, 'pt', pose or stand(), f, x, .4, fx=fx, seed=1, U_=U * s)

def cli(ctx, x, f, pose=None, s=.9, fx=0.0):
    return fig(ctx, 'client', pose or stand(), f, x, .4, fx=fx, seed=2, U_=U * s)

def from_script(path, fn='s1', tau=.8):
    spec = importlib.util.spec_from_file_location(os.path.basename(path)[:-3], os.path.join(HERE, path))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return lambda ctx: m.SCENES[fn](ctx, tau, 3.0, {})

ARMS_UP = dict(la1=-150, la2=-170, ra1=150, ra2=170)
SHRUG = dict(la1=-60, la2=-120, ra1=60, ra2=120, h=-6)
POINT = dict(ra1=95, ra2=95)

# --------------------------------------------------------------- scene
def c_foto(ctx):
    floor(ctx, G)
    phone(ctx, 690, 1060, 470, 860, gallery_screen(.6), rot=.05)
    pt(ctx, 250, face('wide', 'wavy', 'worried', (1, 0)), stand(**SHRUG), s=.95)

def c_primo_giorno(ctx):
    floor(ctx, G)
    calendar(ctx, 620, 640, 2, 1.0, w=300, h=320, head='GIORNO')
    pt(ctx, 300, face('open', 'flat', 'worried', (1, 0)), s=1.0)
    cli(ctx, 830, face('tired', 'flat', 'neutral', (-1, 0)), s=.7)

def c_dropset(ctx):
    floor(ctx, G)
    halo(ctx, (540, 1150), 520, RED, .12)
    A = fig(ctx, 'client', curl(.6, .9), face('wince', 'shout', 'angry'), 540, .9, fx=.15, seed=2, U_=U * 1.0)
    hold_dumbbell(ctx, A, 'R', 8, .95)
    plate_label(ctx, (250, 760), 'DROP SET', 1, bg=INK, tc=WHITE, size=50, rot=-.06)
    plate_label(ctx, (840, 700), 'DI NUOVO?!', 1, bg=RED, tc=WHITE, size=46, rot=.07)

def c_sonno(ctx):
    floor(ctx, G)
    digital_clock(ctx, (760, 800), '02:47', 1.0, .6)
    cli(ctx, 360, face('tired', 'wavy', 'worried', (1, -1)), s=1.05)
    zzz(ctx, (560, 860), .5)

def c_chat23(ctx):
    floor(ctx, G)
    digital_clock(ctx, (800, 760), '23:04', .8, .5)
    phone(ctx, 690, 1180, 380, 640, wa_screen([('Domani che faccio?', 'l'), ('Posso saltare le gambe?', 'l'), ('Ci sei??', 'l')], 3.0), rot=.05)
    pt(ctx, 270, face('tired', 'wavy', 'worried', (1, 0)), s=1.0)

def c_squat(ctx):
    floor(ctx, G)
    A = fig(ctx, 'client', squat_bar(.4, .7), face('wince', 'wavy', 'worried'), 560, .6, fx=.1, seed=2, U_=U * 1.0)
    draw_bar_on(ctx, A, 560, .6, plates=1.2, s=1.05)
    plate_label(ctx, (290, 700), 'SQUAT 4×8', 1, bg=INK, tc=WHITE, size=50, rot=-.06)
    xmark(ctx, (850, 1000), 1.0)

def c_frequenza(ctx):
    floor(ctx, G)
    calendar(ctx, 560, 640, 1, 1.0, w=320, h=330, head='VOLTA A SETT.')
    pt(ctx, 300, face('open', 'flat', 'neutral', (1, 0)), stand(**POINT), s=1.0)

def c_cardio(ctx):
    floor(ctx, G)
    bike(ctx, 540, G, .5, face('wide', 'wavy', 'worried'), s=1.1)

def c_primo_esercizio(ctx):
    list_card(ctx, 250, 600, 580, ['1. HIP THRUST', '2. Squat', '3. Affondi', '4. Leg curl'], hl=0, title='SCHEDA')
    floor(ctx, G)
    pt(ctx, 900, face('happy', 'smile', 'neutral', (-1, 0)), stand(**POINT), s=.6, fx=-.2)

def c_pesante_leggero(ctx):
    scale_balance(ctx, (540, 640), 0, '6 REP', '30 REP', s=1.4)

def c_progressione(ctx):
    floor(ctx, G)
    halo(ctx, (540, 1150), 520, RED, .10)
    A = fig(ctx, 'client', curl(.9, .3), face('open', 'smile', 'neutral'), 540, .7, fx=.15, seed=2, U_=U * 1.05)
    hold_dumbbell(ctx, A, 'R', 8, .95)
    plate_label(ctx, (250, 740), '8-12 REP', 1, bg=INK, tc=WHITE, size=50, rot=-.06)
    plate_label(ctx, (830, 700), '+2,5 KG', 1, bg=RED, tc=WHITE, size=50, rot=.07)

def c_recupero(ctx):
    floor(ctx, G)
    stopwatch_big(ctx, (760, 860), 170, '1:00', .2)
    cli(ctx, 330, face('tired', 'shout', 'worried', (1, 0)), stand(t=10, h=12, la1=-30, la2=-60, ra1=30, ra2=60), s=1.0)

def c_serie_petto(ctx):
    radar(ctx, (540, 1050), 330, [6, 14, 12, 15, 13, 11], label_size=34)

def c_specchio(ctx):
    floor(ctx, G)
    mirror(ctx, 720, G)
    cli(ctx, 330, face('open', 'flat', 'worried', (1, 0)), s=1.0)

def c_bilancia(ctx):
    floor(ctx, G)
    cli(ctx, 540, face('wide', 'wavy', 'worried', (0, 1)), s=1.0)
    plate_label(ctx, (540, 640), '= 80 KG', 1, bg=INK, tc=WHITE, size=64, rot=-.04)

def c_pigro(ctx):
    floor(ctx, G)
    cli(ctx, 540, face('tired', 'flat', 'neutral'), stand(t=-6, h=8), s=1.0)
    plate_label(ctx, (260, 760), 'STESSO PESO', 1, bg=INK, tc=WHITE, size=46, rot=-.06)
    plate_label(ctx, (830, 700), 'DA MESI', 1, bg=RED, tc=WHITE, size=46, rot=.07)

def c_tutto_fatto(ctx):
    floor(ctx, G)
    pt(ctx, 300, face('open', 'flat', 'angry', (1, 0)), s=1.0)
    cli(ctx, 780, face('happy', 'smile', 'neutral', (-1, 0)), stand(**ARMS_UP), s=.95)
    bubble(ctx, 780, 650, 420, 150, 'TUTTO FATTO!', tail=(0, 1))

def c_doms(ctx):
    floor(ctx, G)
    cli(ctx, 540, face('wince', 'wavy', 'worried'), stand(t=18, h=10, la1=-40, la2=-90, ra1=40, ra2=90, ll1=-14, rl1=14), s=1.0)
    for sd in (-1, 1): shake_lines(ctx, (540 + sd * 230, 1150), sd)
    plate_label(ctx, (540, 650), 'DOMS', 1, bg=RED, tc=WHITE, size=60, rot=-.05)

def c_terza_settimana(ctx):
    floor(ctx, G)
    calendar(ctx, 170, 650, 3, 1.0, w=300, h=320, head='SETTIMANA')
    fig(ctx, 'client', lambda t: walk(t * 2 * math.pi * 1.2, 1, .2, 1.2), face('tired', 'flat', 'worried', (1, 0)), 760, .6, fx=.6, seed=2, U_=U * .85)

def c_brand(ctx):
    halo(ctx, (540, 1100), 560, RED, .25)
    logo(ctx, 540, 1130, 600, 'bianco')

# --------------------------------------------------------------- reel pubblicati (data, permalink, gancio, scena)
REELS = [
    ('2026-11-18', 'Df4jQTQiPwp', None, None),          # reel 30: python3 r30.py cover
    ('2026-11-16', 'DfzqEHDEZb4', None, None),          # reel 29: python3 r29.py cover
    ('2026-10-28', 'DfCRqrAiNL0', "DOV'È LA FOTO\nDEL PRIMA?", c_foto),
    ('2026-10-20', 'DeuLEXbCpPm', 'LA SCHEDA\nIL GIORNO DOPO?', c_primo_giorno),
    ('2026-10-19', 'DerQqREi2WE', 'DROP SET\nA TUTTI?', c_dropset),
    ('2026-10-18', 'DeorxCeC5EZ', 'NON DIMAGRISCE?\nGUARDA IL SONNO', c_sonno),
    ('2026-10-17', 'DemEuTtCP_2', 'RISPONDI AI\nCLIENTI ALLE 23?', c_chat23),
    ('2026-10-16', 'DejgxpEi_ck', 'BASTA SCRIVERE\n"SQUAT 4×8"?', c_squat),
    ('2026-10-15', 'Deg7gtxCwuX', 'MI MANDI\nIL BONIFICO?', 'esempi/v15.py'),
    ('2026-10-14', 'DeeN6Wls40e', "IL TUO LAVORO\nÈ ALLENARE.", 'brand'),
    ('2026-10-13', 'DebwlEyCk-N', 'OGNI MUSCOLO UNA\nVOLTA A SETTIMANA?', c_frequenza),
    ('2026-10-12', 'DeZL1tbgeeq', 'IL CARDIO FA\nPERDERE MUSCOLI?', c_cardio),
    ('2026-10-11', 'DeWnB5Pjooe', 'IL PRIMO\nESERCIZIO CONTA', c_primo_esercizio),
    ('2026-10-10', 'DeT74BPFJRd', 'PESANTE O\nLEGGERO?', c_pesante_leggero),
    ('2026-10-09', 'DeRddZ0jCW8', 'QUANDO AUMENTARE\nIL CARICO?', c_progressione),
    ('2026-10-08', 'DeO4paiAXZO', 'UN MINUTO\nDI RECUPERO?', c_recupero),
    ('2026-10-07', 'DeMT3zbj-7U', 'QUANTE SERIE\nPER IL PETTO?', c_serie_petto),
    ('2026-10-06', 'DeJvCdCjMC8', 'ALLO SPECCHIO\nNON CAMBI?', c_specchio),
    ('2026-10-05', 'DeHKRWOmcuG', 'LA BILANCIA\nMENTE', c_bilancia),
    ('2026-10-04', 'DeEldUyFAWN', 'IL CORPO\nÈ PIGRO', c_pigro),
    ('2026-10-03', 'DeBr8YeCbOC', "L'APP DEL\nPERSONAL TRAINER", 'brand'),
    ('2026-10-02', 'Dd_b4dbkX6N', '«TUTTO FATTO,\nTUTTO BENE»', c_tutto_fatto),
    ('2026-10-01', 'Dd83HXYEcbA', 'DOLORI\nDUE GIORNI DOPO?', c_doms),
    ('2026-09-30', 'Dd6SUPUj27t', 'MOLLA ALLA\nTERZA SETTIMANA?', c_terza_settimana),
    ('2026-09-29', 'Dd3oU9yiCEB', "L'APP DEL\nPERSONAL TRAINER", 'brand'),
    ('2026-09-28', 'Dd12fYsC3Yv', "L'APP DEL\nPERSONAL TRAINER", 'brand'),
]

def make(day, code, hook, scene):
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, f'{day}_{code}.jpg')
    if scene == 'brand':
        return render_cover(hook, c_brand, path, dark=True)
    draw = from_script(scene) if isinstance(scene, str) else scene
    return render_cover(hook, draw, path)

if __name__ == '__main__':
    os.chdir(HERE)
    if sys.argv[1:2] == ['brand']:                 # copertina scura per i promo: brand "GANCIO\nRIGA 2" out/cover_pNN.jpg
        print('scritto', render_cover(sys.argv[2].replace('\\n', '\n'), c_brand, sys.argv[3], dark=True)); sys.exit()
    only = sys.argv[1:]
    for day, code, hook, scene in REELS:
        if scene is None or (only and day not in only): continue
        print('scritto', make(day, code, hook, scene))
