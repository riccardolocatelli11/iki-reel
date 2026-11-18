# iki-reel

Reel automatici di **@ikiapp.it** (iki, l'app del personal trainer — iki-app.com). Qui stanno il motore degli omini, gli script dei reel, lo storico dei temi e i video pubblicati.

Pubblicazione: **lunedì, mercoledì, venerdì** (reel con gli omini) e **un giovedì ogni due settimane** (promo, vedi sotto). Tutto viene fatto da Claude in un'attività programmata; Riccardo non approva i singoli reel.

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
| `copertine_archivio.py` | Copertine dei reel pubblicati prima del 18/11/2026 (da caricare a mano dall'app) e copertina scura dei promo |
| ramo `video` | Solo l'mp4 e la copertina (jpg) dell'ultimo reel, da cui Instagram li scarica |

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
   **Copertina.** `python3 rNN.py cover` → `out/cover_NN.jpg`: fondo carta, gancio grande e la prima scena a 0,8 s, impaginati perché il gancio resti intero nel ritaglio 3:4 della griglia del profilo (si vede solo la fascia y 240-1680). Guardala: gancio leggibile, niente testo sotto il gancio. Se la prima scena non rende, definisci nello script `COVER = lambda ctx: s2(ctx, 1.0, 3.0, {})` (o una scena apposta); `COVER_HOOK` cambia il testo se il gancio del video è troppo lungo.
9. **Video online.** Ramo orfano `video` con il solo file, spinto con `--force`:
   ```bash
   rm -rf /tmp/vid && mkdir /tmp/vid && cd /tmp/vid && git init -q -b video
   cp "<mp4>" rNN.mp4 && cp out/cover_NN.jpg rNN.jpg && git add rNN.mp4 rNN.jpg && git commit -q -m "Reel NN"
   git remote add origin https://github.com/riccardolocatelli11/iki-reel && git push -f origin video
   ```
   Indirizzi: `https://raw.githubusercontent.com/riccardolocatelli11/iki-reel/video/rNN.mp4` e, per la copertina, `.../video/rNN.jpg`
10. **Pubblicazione.** Composio, account `instagram_orthis-postil`, `ig_user_id 29071061522583210`:
    `INSTAGRAM_POST_IG_USER_MEDIA` (`video_url`, `cover_url` = l'indirizzo di `rNN.jpg`, `media_type: REELS`, `caption`, `share_to_feed: true`), poi attendi `FINISHED` con `INSTAGRAM_GET_POST_STATUS` (servono circa 4 minuti: riprova ogni 30-40 secondi, fino a 8 minuti), poi `INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH`. Prendi il permalink con `INSTAGRAM_GET_IG_MEDIA`.
11. **Chiusura.** Aggiungi una riga a `storico.md`, fai commit di `rNN.py`, `audio_in/NN.*` e `storico.md` su `main`.

## Didascalia

Prima riga = la domanda del gancio + la smentita con ❌. Poi 2-3 righe con la regola. Poi «Scrivi PAROLA nei commenti e ti mando come funziona 👇». In fondo 5 hashtag: `#personaltrainer #personaltraineritalia #allenamento #coaching #ikiapp` (cambiane 1-2 in base al tema).

## Regole fisse

- Pubblico: i **personal trainer**, non i clienti. Payoff: «L'app del personal trainer».
- Mai «schede in 30 secondi». Il timer è una funzione del cliente. Non parlare di app store né della pagina vetrina.
- Non inventare funzioni, numeri di clienti o risultati. I dati nelle schermate sono esempi (cliente «Marco»).
- Le affermazioni tecniche sull'allenamento devono essere prudenti e condivise («quasi», «di solito»), mai consigli medici.
- Se un passaggio fallisce (voce, render, hosting, Instagram), **non pubblicare a metà e non ritentare all'infinito**: scrivi cosa è successo e fermati. Mai due reel nello stesso giorno.

## Promo del giovedì (ogni due settimane)

Secondo formato, separato dai reel: il promo nello stile «Il tuo lavoro è allenare. Al resto ci pensa iki.». Telefono 3D che fluttua su fondo nero con bagliori rossi, le **schermate vere dell'app**, card che escono dal telefono, il PT dei reel che salta nello schermo e lancia le card, la cliente che festeggia nell'ultima scena, chiusura con «Concentrati su ciò che conta.» e il logo. 30 secondi, nessuna voce, con la colonna sonora sintetizzata di `promo/music.py` (epica/trap, sincronizzata con i tempi del modello: non serve toccarla).

| Percorso | Cosa contiene |
|---|---|
| `promo/template.html` | Il modello: tempi, telefono, card, omini (non toccarlo per un singolo promo) |
| `promo/omino.js` | Gli omini dei reel portati su canvas (stesse proporzioni di `engine.py`) |
| `promo/make.py` | Costruisce `build/pNN.html` da `promo/pNN.json`; `grid NOME` fa la griglia per i ritagli |
| `promo/music.py` | Colonna sonora (aggiunta in automatico da `render.mjs video`) |
| `promo/render.mjs` | `sheet` (12 fotogrammi), `still t…`, `video` (mp4 1080×1920, 30 fps, circa 10-15 minuti) |
| `promo/pNN.json` | Un file per promo. `p01.json` è il modello da seguire |
| `promo/logo/`, `promo/fonts/` | Logo, simbolo (senza capellini), Unbounded, Geist, Geist Mono |
| `promo/storico.md` | Promo già pubblicati: **leggerlo sempre, non ripetere un tema** |

Serve anche `npm`/Playwright (già installato nell'ambiente: `require('playwright')`).

### Procedura

1. **Quando.** Si pubblica un giovedì sì e uno no. Se in `promo/storico.md` c'è un promo di meno di 10 giorni fa, oggi non tocca: fermati e dillo in una riga. Mai due video nello stesso giorno.
2. **Tema.** Se in `promo/` c'è già un `pNN.json` pronto che non compare in `promo/storico.md` (preparato in anticipo), usa quello: ricontrolla solo che schermate e frasi siano ancora fedeli all'app e vai al passo 5. Altrimenti scegli una sola area di iki per promo (pagamenti, schede, clienti e anamnesi, progressi e check, dashboard e incassi, allenamento del cliente con timer e video esercizi, chat, novità rilasciate da poco). Non ripetere quelle di `promo/storico.md`; le novità recenti dell'app hanno la precedenza.
3. **Fedeltà all'app.** Clona `riccardolocatelli11/gestionale-pt`. Le schermate sono `public/pt-vetrina-<NOME>.png` (aggiornate da Riccardo): usa solo quelle. Ogni frase e ogni card deve corrispondere a qualcosa che **trovi nel codice** di `src/` (etichette, testi dei bottoni, comportamento). Se una funzione non c'è nelle schermate o nel codice, non mostrarla. Se le schermate disponibili non bastano per un tema, scegli un altro tema.
4. **Configurazione `promo/pNN.json`** (copia `p01.json`):
   - `hook.lines`: 3 righe «problema» (parola bianca + parola grigia), barrate in rosso; `hook.end`: la risposta su 2 righe (la seconda è al neon, 1-3 parole).
   - `scenes`: esattamente 4. Ognuna ha `screen` (nome dopo `pt-vetrina-`), `eb` (occhiello), `t1`/`t2` (titolo su 2 righe, la seconda al neon, massimo ~18 caratteri per riga), `sub` (una frase), `cards` (3 card) e facoltativo `tap` ([x, y] nelle coordinate della griglia) per il tocco sullo schermo.
   - Card: `img` (ritaglio definito in `crops`: `[schermata, x0, y0, x1, y1]`, coordinate della griglia, larghezza 832), `txt` (`ic`, `ck` occhiello, `cv` valore, `cs` sotto), `chips` (`ck` e lista), `vid` (video esercizio da `public/video/NOME.mp4`).
   - Icone `ic`: check, trend, euro, bell, cam, users, flame, clock, card, play, doc, chat, star.
   - `intro`: alterna `wordmark` e `symbol`; `mirror`: alterna `false` e `true`; `seed`: un numero qualsiasi diverso dal precedente.
   - `omini` facoltativo: `{"pt": true, "cliente": true, "ptX": 350, "clX": 330, "ground": 900}` (posizioni nello schermo, 474 px di larghezza). Sposta `clX`/`ptX` se l'omino copre una card o un dato importante.
   - `caption`: la didascalia (vedi sotto).
   - Per scegliere i ritagli: `python3 promo/make.py grid NOME` e guarda `build/grid_NOME.png`.
5. **Controllo.** `IKI_APP=../gestionale-pt python3 promo/make.py promo/pNN.json`, poi `node promo/render.mjs build/pNN.html sheet` e guarda `build/sheet_pNN.png`; per una scena `still 11 15.2 20.4 25.2`. Controlla: ritagli giusti (niente pezzi di altre righe), testi interi e non sovrapposti, omini che non coprono le card. Correggi e ripeti.
6. **Render.** `node promo/render.mjs build/pNN.html video "out/Promo iki - NN - TITOLO.mp4"`. Controlla durata (30 s) e due fotogrammi con ffmpeg.
7. **Video online e pubblicazione.** Come per i reel (passi 9-10 sopra), ma con i file `pNN.mp4` e `pNN.jpg` sul ramo `video`. `share_to_feed: true`. Copertina scura: `python3 copertine_archivio.py brand 'GANCIO\nRIGA DUE' out/cover_pNN.jpg` con la frase principale del promo (es. «IL TUO LAVORO\nÈ ALLENARE.»), poi `cover_url`.
8. **Chiusura.** Riga in `promo/storico.md` (numero, data, tema, schermate, permalink); commit su `main` di `promo/pNN.json` e `promo/storico.md`.

### Didascalia del promo

Prima riga: i tre problemi del gancio + ❌. Poi 2-3 righe su cosa fa iki per quel tema (solo funzioni verificate). Poi «Concentrati su ciò che conta.», «👉 Prova gratuita su iki-app.com/personaltrainer (link in bio)», «iki · L'app del personal trainer» e 5 hashtag. Nessuna parola CTA da commentare.
