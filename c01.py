from carosello import *

TITLE = 'Primo colloquio: 5 cose da sapere'
CAPTION = """Il primo colloquio lo fai a memoria? ❌

Prima di scrivere la prima scheda ti servono 5 risposte: da quanto si allena, infortuni passati, salute e farmaci, che lavoro fa, quanto dorme. Il resto viene dopo.

📩 Mandalo al collega che parte ancora con «allora, che obiettivo hai?»

iki · L'app del personal trainer — prova gratuita, link in bio

#personaltrainer #personaltraineritalia #anamnesi #coaching #ikiapp"""

def cover_art(ctx):
    floor(ctx, 1220)
    fig(ctx, 'pt', lambda t: P(t=0, la1=-40, la2=-150, ra1=20, ra2=10), dict(eyes='open', mouth='smile', brows='raised', look=(1, 0)),
        330, .5, seed=1, U_=U * .78, g=1220)
    notebook(ctx, (420, 960), .55, -.15, 4, '?')
    fig(ctx, 'client', lambda t: P(t=0), dict(eyes='open', mouth='smile', look=(-1, 0)), 760, .5, seed=2, U_=U * .74, g=1220)
    bubble(ctx, 730, 700, 330, 110, '«Tonificare!»', 1, tail=(0, 1), size=40)

def anamnesi_pt_screen(ctx, w, h):
    """Schermata reale di iki, lato PT: pagina cliente, sezione «Dati e anamnesi» (etichette da App.jsx)."""
    app_head(ctx, w, '')
    text(ctx, 'Marco', 40, 200, 40, FONT, INK, anchor='l')
    text(ctx, 'Dati e anamnesi', 40, 250, 26, FONTB, RED, anchor='l')
    secs = (('ALLENAMENTO E STILE DI VITA', (('Da quanto si allena', '1-3 anni'), ('Tipo di lavoro', 'Sedentario (ufficio)'), ('Ore di sonno medie', '5-6 ore'))),
            ('SALUTE', (('Infortuni passati', 'Sì'), ('Dettagli infortuni', 'Distorsione caviglia dx, 2023'))))
    y = 300
    for tit, rows in secs:
        text(ctx, tit, 40, y, 18, FONT, GRAY, anchor='l'); y += 20
        for k, (lab, v) in enumerate(rows):
            rrect(ctx, 30, y, w - 60, 78, 12); col(ctx, (.95, .94, .92)); ctx.fill()
            text(ctx, lab, 50, y + 24, 19, FONTB, GRAY, anchor='l')
            text(ctx, v, 50, y + 55, 23, FONTB, RED if lab == 'Dettagli infortuni' else INK, anchor='l')
            y += 86
        y += 26

SLIDES = [
    {'kind': 'cover', 'hook': 'PRIMO COLLOQUIO\nA MEMORIA?', 'sub': 'Le 5 cose da sapere prima di scrivere la prima scheda', 'art': cover_art},
    {'kind': 'point', 'n': 1, 'title': 'Da quanto si allena', 'icon': 'dumbbell',
     'body': "«Mai», «da qualche mese» e «da anni» sono tre schede diverse. Chiedi anche cosa faceva: pesi, corsi, sport. Ti dice da che carichi e da che esercizi partire."},
    {'kind': 'point', 'n': 2, 'title': 'Infortuni passati', 'icon': 'cross',
     'body': "Non solo «hai dolori?»: chiedi cosa si è fatto negli anni, anche se ora sta bene. Una vecchia distorsione o un mal di schiena tornano fuori proprio con i primi carichi."},
    {'kind': 'point', 'n': 3, 'title': 'Salute e farmaci', 'icon': 'pill',
     'body': "Problemi di salute attuali, farmaci, allergie. Non per fare il medico: per sapere quando serve il suo via libera prima di iniziare."},
    {'kind': 'point', 'n': 4, 'title': 'Che lavoro fa', 'icon': 'clock',
     'body': "Otto ore seduto o in piedi tutto il giorno cambiano la scheda: mobilità, volume, scelta degli esercizi. E ti dice quanto tempo ha davvero."},
    {'kind': 'point', 'n': 5, 'title': 'Quanto dorme', 'icon': 'moon',
     'body': "Con poche ore di sonno di solito il recupero è più lento. Meglio saperlo prima, che scoprirlo quando i carichi non salgono."},
    {'kind': 'iki', 'title': 'In iki la compila lui', 'screen': anamnesi_pt_screen,
     'body': "Al primo accesso il cliente compila l'anamnesi prima di vedere la scheda. Tu la trovi nella sua pagina, in «Dati e anamnesi»."},
    {'kind': 'end'},
]

if __name__ == '__main__':
    main_carosello(sys.modules[__name__], '01')
