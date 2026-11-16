# iki-reel

Reel automatici di **@ikiapp.it** (iki, l'app del personal trainer — iki-app.com). Qui stanno il motore degli omini, gli script dei reel, lo storico dei temi e i video pubblicati.

Pubblicazione: **lunedì, mercoledì, venerdì**. Tutto viene fatto da Claude in un'attività programmata; Riccardo non approva i singoli reel.

## Cartelle

| Percorso | Cosa contiene |
|---|---|
| `engine.py` | Motore: omini, fondo carta, gancio, parole a tempo, regia, audio, render |
| `props2.py`, `props3.py`, `props4.py` | Oggetti e schermate di iki già disegnati (importare `from props4 import *`) |
| `assets/` | Logo e font Montserrat (Black, ExtraBold) |
| `rNN.py` | Uno script per reel (NN = numero progressivo). `r29.py` è il modello da seguire |
| `esempi/` | Script dei reel 15, 19, 21, 24 originali, come riferimento di scene e oggetti |
| `audio_in/NN.mp3`, `NN.json` | Voce del reel e parole con i tempi (trascrizione) |
| `storico.md` | Temi già pubblicati: **leggerlo sempre, non ripetere un tema** |
| ramo `video` | Solo l'mp4 dell'ultimo reel, da cui Instagram lo scarica |

## Preparare l'ambiente

```bash
pip install --break-system-packages pycairo numpy scipy pillow
mkdir -p ~/.fonts && cp assets/Montserrat-*.ttf ~/.fonts/ && fc-cache -f
```

Serve `ffmpeg`.

## Procedura per un reel

1. **Tema.** Leggi `storico.md` e scegli un tema nuovo. Formato che rende di più: un mito o un errore tecnico dell'allenamento o della gestione dei clienti, smentito, con una regola pratica che il PT può usare domani.
2. **Fedeltà all'app.** Clona `riccardolocatelli11/gestionale-pt` (è sempre in aggiornamento) e cerca nel codice (`src/`) la funzione di iki da mostrare. Cita solo ciò che trovi nel codice; la schermata disegnata deve avere etichette e struttura reali. Se non trovi una funzione adatta, cambia tema.
3. **Testo.** 7-9 frasi, 380-480 caratteri, 25-35 secondi. Struttura:
   - frase 1: domanda tecnica (è anche il gancio rosso `HOOK`, tutto maiuscolo, 2 righe);
   - frase 2: smentita secca («Sbagliato.», «Quasi mai.») con il timbro ❌ (`stamp_x`);
   - 2-3 frasi con la spiegazione e la regola pratica;
   - 1 frase su iki (dopo metà video);
   - ultima frase: «Scrivi «PAROLA» nei commenti, e ti mando come funziona.» con `cta_card`.
4. **Script `rNN.py`.** Copia la struttura di `r29.py`: `TITLE`, `HOOK`, `LOOP`, `TAIL`, `SENT`, una funzione di scena per frase, `SCENES`, `SFX`. Ogni voce di `SENT` è `(frase, 'sN', {PAROLE ROSSE}, pausa)`. In ogni scena deve muoversi qualcosa ogni 1-2 secondi e l'oggetto principale occupa almeno un terzo dello schermo. Zona utile: y da 560 a 1500 (in alto ci sono gancio e parole, in basso l'interfaccia di Instagram).
5. **Controllo prima della voce.** `python3 rNN.py sheet` e guarda `build/sheet_NN.png`: niente sovrapposizioni, niente testo tagliato, facce giuste. Correggi finché è pulito. Così non si sprecano crediti.
6. **Voce.** ElevenLabs, voce «Riccardo» `voice_id KoYZY2uFp4KixfrIYJPt`, modello `eleven_v4`, **una sola generazione** (`generations_count: 1`). Tag di tono tra parentesi quadre (`[incredulous]`, `[confident]`, `[serious]`, `[excited]`, `[cheerfully]`): energica ed esplosiva nei punti giusti, **mai urlata**. Scarica l'mp3 in `audio_in/NN.mp3`.
7. **Tempi.** Trascrivi l'audio (`creative_transcribe_audio`) e salva le parole in `audio_in/NN.json` (lista di `{text, start, end}`). Poi `python3 rNN.py times` e di nuovo `sheet`: le parole chiave devono cadere nella scena giusta. Senza json il motore si aggancia alle pause, meno preciso.
8. **Render.** `python3 rNN.py` → `out/Reel iki - NN - TITOLO.mp4` (1080×1920, 30 fps, circa 30 secondi di calcolo). Controlla durata e alcuni fotogrammi con `still`.
9. **Video online.** Ramo orfano `video` con il solo file, spinto con `--force`:
   ```bash
   rm -rf /tmp/vid && mkdir /tmp/vid && cd /tmp/vid && git init -q -b video
   cp "<mp4>" rNN.mp4 && git add rNN.mp4 && git commit -q -m "Reel NN"
   git remote add origin https://github.com/riccardolocatelli11/iki-reel && git push -f origin video
   ```
   Indirizzo: `https://raw.githubusercontent.com/riccardolocatelli11/iki-reel/video/rNN.mp4`
10. **Pubblicazione.** Composio, account `instagram_orthis-postil`, `ig_user_id 29071061522583210`:
    `INSTAGRAM_POST_IG_USER_MEDIA` (`video_url`, `media_type: REELS`, `caption`, `share_to_feed: true`), poi attendi `FINISHED` con `INSTAGRAM_GET_POST_STATUS` (servono circa 4 minuti: riprova ogni 30-40 secondi, fino a 8 minuti), poi `INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH`. Prendi il permalink con `INSTAGRAM_GET_IG_MEDIA`.
11. **Chiusura.** Aggiungi una riga a `storico.md`, fai commit di `rNN.py`, `audio_in/NN.*` e `storico.md` su `main`.

## Didascalia

Prima riga = la domanda del gancio + la smentita con ❌. Poi 2-3 righe con la regola. Poi «Scrivi PAROLA nei commenti e ti mando come funziona 👇». In fondo 5 hashtag: `#personaltrainer #personaltraineritalia #allenamento #coaching #ikiapp` (cambiane 1-2 in base al tema).

## Regole fisse

- Pubblico: i **personal trainer**, non i clienti. Payoff: «L'app del personal trainer».
- Mai «schede in 30 secondi». Il timer è una funzione del cliente. Non parlare di app store né della pagina vetrina.
- Non inventare funzioni, numeri di clienti o risultati. I dati nelle schermate sono esempi (cliente «Marco»).
- Le affermazioni tecniche sull'allenamento devono essere prudenti e condivise («quasi», «di solito»), mai consigli medici.
- Se un passaggio fallisce (voce, render, hosting, Instagram), **non pubblicare a metà e non ritentare all'infinito**: scrivi cosa è successo e fermati. Mai due reel nello stesso giorno.
