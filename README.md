# iki-reel

Reel automatici di **@ikiapp.it** (iki, l'app del personal trainer — iki-app.com). Qui stanno il motore degli omini, gli script dei reel, lo storico dei temi e i video pubblicati.

Pubblicazione: **lunedì, mercoledì, venerdì** (reel con gli omini), **martedì** (carosello, vedi sotto) e **un giovedì ogni due settimane** (promo, vedi sotto). Tutto viene fatto da Claude in un'attività programmata; Riccardo non approva i singoli reel.

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

0. **Misure dei reel passati.** Prima di tutto aggiorna `metriche.md` (vedi la sezione «Metriche» sotto) per i reel pubblicati da almeno 7 giorni che non ci sono ancora. Leggila: i temi e le CTA che portano più **invii** (shares) e follower vanno ripetuti, quelli con skip alto evitati.
1. **Tema.** Leggi `storico.md` e scegli un tema nuovo. Formato che rende di più: un mito o un errore tecnico dell'allenamento o della gestione dei clienti, smentito, con una regola pratica che il PT può usare domani. Dai numeri del profilo (vedi «Cosa dicono i numeri» sotto): meglio i temi **tecnici di programmazione** con una regola **concreta e riutilizzabile, possibilmente con un numero** (quando aumentare il carico, quante serie, quanto recupero, quante ripetizioni in riserva): sono quelli che vengono salvati e condivisi. Evita i temi emotivi o generici (bilancia, specchio, motivazione) e i reel che parlano dell'app fin dall'inizio: l'app arriva solo nella frase su iki.
   **Due aree, alternate.** I temi di solo allenamento attirano anche chi va in palestra e non fa il PT (il 98% della copertura è di non follower, ma non diventano follower). Quindi alterna, guardando la colonna «Area» dell'ultima riga di `storico.md`:
   - **Mestiere** (se l'ultimo era Allenamento): un errore nella gestione dei clienti o del lavoro da PT, sempre come mito smentito con una regola pratica. Esempi: disdette all'ultimo minuto, clienti che spariscono dopo un mese, prezzi e pacchetti, rate e solleciti, primo colloquio, messaggi a tutte le ore, check settimanali, rinnovi. Sono i temi che un PT **manda a un collega**, e li guarda solo chi fa il PT (i due di prova, «Rispondi ai clienti alle 23?» e «Al cliente nuovo mandi la scheda il giorno dopo?», sono tra i primi 6 per copertura).
   - **Allenamento** (se l'ultimo era Mestiere): programmazione tecnica con una regola numerica, detta dal punto di vista del PT che la applica ai clienti («Il tuo cliente…»), non del palestrato.
2. **Fedeltà all'app.** Clona `riccardolocatelli11/gestionale-pt` (è sempre in aggiornamento) e cerca nel codice (`src/`) la funzione di iki da mostrare. Cita solo ciò che trovi nel codice; la schermata disegnata deve avere etichette e struttura reali. Se non trovi una funzione adatta, cambia tema.
3. **Testo.** 7-9 frasi, 380-480 caratteri, 25-35 secondi. Struttura:
   - frase 1: domanda tecnica (è anche il gancio rosso `HOOK`, tutto maiuscolo, 2 righe);
   - frase 2: smentita secca («Sbagliato.», «Quasi mai.») con il timbro ❌ (`stamp_x`);
   - 2-3 frasi con la spiegazione e la regola pratica;
   - 1 frase su iki (dopo metà video);
   - ultima frase: la CTA, **alternata** da un reel all'altro. Guarda la colonna «Parola CTA» dell'ultima riga di `storico.md`:
     - se l'ultimo reel aveva una parola da commentare → questo è un reel **«invia»**: ultima frase «Mandalo al collega che lo fa ancora.» (o una variante adatta al tema, sempre con «manda/mandalo a un collega») con `send_card(ctx, k, 660, tau)` al posto di `cta_card`; nello storico, nella colonna «Parola CTA», scrivi `— (invia)`. Gli invii in DM sono il segnale che Instagram premia di più per gli account nuovi;
     - se l'ultimo reel era un reel «invia» (o «salva») → questo ha la parola: «Scrivi «PAROLA» nei commenti, e ti mando come funziona.» con `cta_card`. **Scrivi anche `dm/PAROLA.md`** (vedi `dm/README.md`): è il messaggio che parte da solo in DM a chi commenta. Solo funzioni verificate nel codice, link iki-app.com/personaltrainer, firma «Riccardo».
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
11. **Chiusura.** Aggiungi una riga a `storico.md` (con l'Area), fai commit di `rNN.py`, `audio_in/NN.*`, `storico.md`, `metriche.md` e dell'eventuale `dm/PAROLA.md` su `main`.

## Didascalia

Prima riga = la domanda del gancio + la smentita con ❌. Poi 2-3 righe con la regola. Poi la CTA dello stesso tipo del video: «Scrivi PAROLA nei commenti e ti mando come funziona in DM 👇» per i reel con la parola, oppure «📩 Mandalo al collega che lo fa ancora.» per i reel «invia» (in questi aggiungi anche una riga «iki · L'app del personal trainer — prova gratuita, link in bio»). Penultima riga, sempre: «🎙️ Voce IA» (breve, ma non toglierla: Meta e TikTok chiedono di dichiarare l'audio realistico generato con l'IA; su TikTok va attivata anche l'etichetta «Contenuto generato dall'IA» al caricamento). In fondo 5 hashtag: `#personaltrainer #personaltraineritalia #allenamento #coaching #ikiapp` (cambiane 1-2 in base al tema).

## Cosa dicono i numeri (analisi del 23/11/2026)

Dati di Instagram sui contenuti dal 28/09 al 23/11/2026. Da ricontrollare ogni tanto con `INSTAGRAM_GET_IG_MEDIA_INSIGHTS` (views, reach, saved, shares, ig_reels_avg_watch_time, reels_skip_rate).

- I reel «mito tecnico smentito» con gli omini fanno di solito 1.000-1.700 visualizzazioni, con il 33-45% che scorre via subito e 9-12 s di visione media. Il migliore in assoluto è la doppia progressione (4.720 visualizzazioni, 61 salvataggi, 19 condivisioni): una regola concreta da riusare.
- I reel emotivi o generici (bilancia, specchio, «il corpo è pigro») e quelli che partono dall'app: 75-80% scorre via subito, 250-800 visualizzazioni.
- I promo e i video di marchio: 85-92% scorre via subito e la visione media è di 2-3 s, perché il problema compare solo dopo il logo.
- I vecchi post nel feed (immagini e caroselli pubblicitari sull'app) arrivavano a circa 25 persone. I caroselli **educativi** del martedì sono un test diverso: Instagram dice che oggi i caroselli portano più coinvolgimento e salvataggi; misurali in `metriche.md` come i reel.
- La CTA «scrivi PAROLA nei commenti» ha portato 2 commenti in tutto: per questo ora si alterna con la CTA «invia» (passo 3), e chi commenta riceve subito il messaggio in DM (`dm/`). Quando ci saranno almeno 4 reel per tipo, confronta in `metriche.md` invii, salvataggi, commenti e follower e scrivi qui quale rende di più.
- Il 98% della copertura (3.854 su 3.920 in 30 giorni) è di non follower, ma i follower non crescono: il pubblico raggiunto dai temi di allenamento è in buona parte fatto di non PT. Per questo l'alternanza Mestiere / Allenamento (passo 1).
- Il segnale più legato alla copertura nei nostri dati è la quota di chi scorre via (correlazione −0,56): il gancio a domanda + smentita funziona, non cambiarlo.

## Metriche

`metriche.md` ha una riga per reel, misurata **7 giorni dopo** la pubblicazione con `INSTAGRAM_GET_IG_MEDIA_INSIGHTS` (`metric`: views, reach, likes, comments, saved, shares, ig_reels_avg_watch_time, reels_skip_rate). L'id del media si trova con `INSTAGRAM_GET_IG_USER_MEDIA` confrontando il permalink. Colonne: N, data, area, CTA, views, copertura, skip %, visione media (s), invii, salvataggi, commenti, invii ogni 1.000 di copertura. A ogni nuovo reel aggiungi le righe mancanti, poi rileggi la tabella per scegliere tema e area.

## Regole fisse

- Pubblico: i **personal trainer**, non i clienti. Payoff: «L'app del personal trainer».
- Mai «schede in 30 secondi». Il timer è una funzione del cliente. Non parlare di app store né della pagina vetrina.
- Non inventare funzioni, numeri di clienti o risultati. I dati nelle schermate sono esempi (cliente «Marco»).
- Le affermazioni tecniche sull'allenamento devono essere prudenti e condivise («quasi», «di solito»), mai consigli medici.
- Se un passaggio fallisce (voce, render, hosting, Instagram), **non pubblicare a metà e non ritentare all'infinito**: scrivi cosa è successo e fermati. Mai due reel nello stesso giorno.

## Carosello del martedì (ogni settimana)

Formato fisso, 1080×1350, stesso stile dei reel (fondo carta, gancio rosso, omini). Motore `carosello.py`, uno script `cNN.py` per carosello (modello: `c01.py`), storico in `caroselli.md`.

1. **Tema.** Un contenuto **da salvare e mandare a un collega**: checklist, «le N cose da…», errori da evitare, con regole pratiche. Area **Mestiere** quasi sempre (gestione clienti, colloqui, pagamenti, rinnovi, comunicazione), ogni tanto Allenamento dal punto di vista del PT. Non ripetere i temi di `caroselli.md` né quelli dei reel delle ultime 2 settimane.
2. **Fedeltà all'app.** La slide `iki` mostra una funzione trovata nel codice di gestionale-pt (`src/`), con etichette reali. Se nessuna funzione c'entra davvero, cambia tema.
3. **Struttura.** 1 copertina (`cover`: gancio a domanda, 2 righe, + sottotitolo con la promessa), 4-6 slide `point` (titolo breve, testo di 2-5 righe, un'icona), 1 slide `iki`, 1 slide `end` (Mandalo a un collega). Affermazioni prudenti («di solito»), mai consigli medici.
4. **Controllo.** `python3 cNN.py sheet` → guarda `build/csheet_NN.png`: niente testo tagliato o sovrapposto, schermata leggibile. Poi `python3 cNN.py` → `out/carosello_NN/01.jpg …`.
5. **Immagini online.** Ramo `carosello` (NON il ramo `video`, che deve tenere il reel del giorno prima per TikTok):
   ```bash
   rm -rf /tmp/car && mkdir /tmp/car && cd /tmp/car && git init -q -b carosello
   for f in <repo>/out/carosello_NN/*.jpg; do cp "$f" "cNN_$(basename $f)"; done
   git add . && git commit -q -m "Carosello NN" && git remote add origin https://github.com/riccardolocatelli11/iki-reel && git push -f origin carosello
   ```
   Indirizzi: `https://raw.githubusercontent.com/riccardolocatelli11/iki-reel/carosello/cNN_01.jpg` …
6. **Pubblicazione.** Per ogni immagine `INSTAGRAM_POST_IG_USER_MEDIA` con `image_url` e `is_carousel_item: true` (senza caption); poi il contenitore del carosello con `children` (gli id, in ordine) e `caption` (`INSTAGRAM_CREATE_CAROUSEL_CONTAINER`, oppure `INSTAGRAM_POST_IG_USER_MEDIA` con `media_type: CAROUSEL`); poi `INSTAGRAM_POST_IG_USER_MEDIA_PUBLISH` e permalink con `INSTAGRAM_GET_IG_MEDIA`.
7. **Didascalia.** Prima riga: il gancio + ❌. Poi 2-3 righe che riassumono le regole. Poi «📩 Mandalo al collega che…», la riga «iki · L'app del personal trainer — prova gratuita, link in bio» e 5 hashtag.
8. **Chiusura.** Riga in `caroselli.md` (numero, data, tema, funzione iki, permalink); commit su `main` di `cNN.py` e `caroselli.md`.

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

1. **Primo secondo.** Il promo 01 ha perso l'86% delle persone nel primo secondo, perché il gancio compariva solo dopo il logo (circa 3 s). Dal 23/11/2026 il modello parte con il gancio già al primo fotogramma (`coldOpen`, predefinito; `"coldOpen": false` nel json rimette il logo in apertura, da non usare). Scegli `hook.lines` brevissime e d'impatto: la prima riga è quella che decide se restano.
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
