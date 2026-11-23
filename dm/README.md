# Messaggi automatici in DM

Quando un reel chiede «Scrivi PAROLA nei commenti», l'attività programmata «iki — risposte automatiche ai commenti» manda il messaggio di `PAROLA.md` in privato a chi commenta con quella parola (risposta privata di Instagram al commento), e risponde al commento con «Ti ho scritto in DM 📩».

- Un file per parola: `dm/PAROLA.md` (maiuscolo, senza accenti), testo semplice, massimo 900 caratteri, solo funzioni verificate nel codice di gestionale-pt. Lo scrive l'attività dei reel nello stesso commit del reel.
- Chiude sempre con il link alla prova gratuita (iki-app.com/personaltrainer) e la firma di Riccardo.
- `dm/inviati.json`: id dei commenti a cui è già stato mandato il messaggio (solo id, niente nomi utente: il repository è pubblico).
- Instagram permette una sola risposta privata per commento, entro 7 giorni dal commento.
