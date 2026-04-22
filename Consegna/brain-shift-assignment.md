# Assignment — Brain Shift

Questo documento descrive **come** il laboratorio Brain Shift va svolto, consegnato e valutato. Il testo del problema è in [brain-shift.md](brain-shift.md) e va letto per primo.

---

## Tempi e consegna

- **Assegnazione**: martedì 22 aprile 2026
- **Consegna**: domenica 17 maggio 2026, ore 23:59
- **Durata effettiva**: circa 3 settimane e mezza di lavoro

La consegna avviene inviando al docente **il link al repository GitHub pubblico** del progetto. Non si consegnano zip, non si consegnano allegati via mail, non si consegnano cartelle su Drive. Link a GitHub e basta.

Dopo le 23:59 di domenica 17 maggio il repo **non deve più ricevere commit** fino al termine dell'orale. Commit post-consegna vengono considerati come consegna tardiva (vedi rubrica).

---

## Gruppi

- **Composizione standard**: coppie (2 persone).
- **Trii**: ammessi, ma **solo su richiesta esplicita e concordata con il docente**. Chi sceglie il trio si impegna a realizzare **almeno una delle estensioni bonus** come requisito aggiuntivo, per giustificare l'aumento di forze.
- **Formazione**: libera. Ciascuno sceglie i compagni.
- **Cambio composizione in corsa**: solo in casi eccezionali, parlando prima con il docente. Non è una scelta da fare la seconda settimana perché «non ci troviamo».

Ogni studente consegna il link al repository del proprio gruppo. Il voto è **individuale** (non di gruppo): dipende dal codice prodotto dal gruppo, ma anche dalla capacità personale di difenderlo all'orale.

---

## Repository GitHub

### Requisiti strutturali

- Il repository è **pubblico** (il docente deve poterlo clonare senza autorizzazioni).
- Contiene almeno:
  - il codice sorgente del gioco
  - un `README.md` che spiega come installarlo e giocarlo
  - un file `requirements.txt` con le dipendenze
  - una cartella `docs/` con la documentazione (vedi sotto)
  - una cartella `tests/` con i test pytest
- Il gioco deve partire da clone pulito con una sequenza semplice tipo:

  ```bash
  git clone <URL>
  cd <repo>
  pip install -r requirements.txt
  python main.py
  ```

  Se il docente, clonando il repository, non riesce a giocare entro cinque minuti, la voce «Esecuzione» della rubrica ne risente.

### Git: come va usato

Git non è un backup da usare a fine progetto con un solo commit. Deve raccontare la storia dello sviluppo. Nello specifico:

- **Commit frequenti e significativi**: piccoli, atomici, con messaggi che descrivono *cosa cambia e perché*. Un messaggio come «update» o «fix» non dice nulla ed è considerato lavoro incompleto. Preferite messaggi come «aggiunge test per scoring con moltiplicatore saturo» o «corregge bilanciamento YES/NO nel generatore».
- **Contributo bilanciato dei membri**: entrambi (o tutti e tre) i membri devono avere commit a proprio nome. Un progetto in cui il 90% dei commit è di un solo membro è considerato un progetto svolto da una persona sola, con le conseguenze del caso sulla valutazione individuale.
- **Cronologia coerente**: lo sviluppo deve essere distribuito nel tempo. Duecento commit schiacciati nelle ultime 24 ore prima della consegna sono un segnale pessimo e ridurranno il punteggio indipendentemente dalla qualità del codice.
- **Configurazione nome/email**: ciascuno configura git con **nome e cognome reali** e un'email stabile. Niente `user.name = "admin"` o email fittizie: dal `git log` il docente deve capire chi ha scritto cosa.

Branch e pull request non sono obbligatori. Se li usate (ottima pratica), bene. Altrimenti lavorare su `main` va accettato, ma attenzione ai conflitti quando committate in parallelo.

---

## Uso dell'IA

L'IA (ChatGPT, Claude, Copilot, Gemini, qualsiasi assistente di coding) è **consentita come assistente, non come risolutore automatico**.

### Cosa è ammesso

- Chiedere chiarimenti su funzioni pygame, su sintassi Python, su errori di esecuzione.
- Farsi spiegare un concetto (es. «come funziona `dataclass`?»).
- Farsi suggerire una struttura o un approccio, da valutare criticamente e riscrivere.
- Farsi suggerire codice *di dettaglio* (es. come si disegna un rettangolo con angoli arrotondati) e integrarlo dopo averlo capito.
- Usarla per generare test aggiuntivi oltre quelli minimi.

### Cosa non è ammesso

- Consegnare codice generato dall'IA e non compreso. Se il docente durante l'orale chiede «spiegami questa funzione» e non sai rispondere, il verdetto è immediato.
- Delegare all'IA la **scrittura della documentazione e del devlog**. La documentazione è il luogo dove voi spiegate *il vostro ragionamento*. Se la delega all'IA, non è vostra. Potete usare l'IA come correttore bozze (tipo/grammatica), non come autore.
- Delegare all'IA le **parti di metacognizione**: riflessione sulle scelte progettuali, devlog, autovalutazione. Questa è la parte formativa del progetto; farla scrivere all'IA significa rinunciare a ciò che il progetto deve insegnarvi.

### Trasparenza obbligatoria

Nel file `docs/uso-ia.md` (canovaccio fornito) dovete dichiarare, in modo granulare:

- per **quali parti** del codice avete usato l'IA
- **cosa avete chiesto** (prompt o sintesi della richiesta)
- **cosa avete accettato, modificato, rifiutato** e perché

Onestà: se il docente legge il codice e trova uno stile chiaramente da IA mentre in `uso-ia.md` dichiarate di non averla usata, la discrepanza pesa molto di più dell'uso stesso. Dichiarare è sempre meglio che nascondere.

---

## Documentazione

Una cartella `docs/` con più file. Un canovaccio è fornito nella cartella `docs-template/` del laboratorio: copiatela nel vostro repository e compilatela.

File attesi:

- `docs/README-progetto.md` — overview, cosa fa il gioco, come giocarlo
- `docs/architettura.md` — decomposizione in moduli, macchina a stati, diagramma
- `docs/scelte.md` — scelte implementative non ovvie, compromessi, alternative scartate
- `docs/uso-ia.md` — trasparenza sull'uso dell'IA
- `docs/devlog.md` — diario di bordo settimanale del gruppo
- `docs/personalizzazioni.md` — solo se avete personalizzato il gioco oltre il core

Ogni file ha domande-guida nel canovaccio. Non sono un quiz: sono *spunti di riflessione*. Se non hanno senso per il vostro progetto specifico, saltatele e spiegate perché.

---

## Orale

Peso: **40%** del voto finale.

L'orale si svolge in aula nella settimana successiva alla consegna. Durata per gruppo: 15-20 minuti circa.

Durante l'orale il docente:

- fa partire il gioco da clone pulito e lo prova
- chiede di **navigare il codice** mentre pone domande su parti specifiche
- chiede di **spiegare scelte progettuali** (perché avete strutturato così scoring, perché quel generatore, ecc.)
- chiede di **spiegare la storia git**: chi ha fatto cosa, perché quel commit
- può chiedere di **modificare qualcosa al volo** (aggiungere un test, cambiare un parametro, rispondere a un cambio di requisito)

L'orale è **individuale**: ciascun membro deve saper rispondere su tutto, non solo sulla propria parte. Se avete scritto solo lo scoring e non sapete come funziona il generatore del vostro compagno, quella parte del progetto per voi non esiste, e il voto individuale ne risente.

Questa è la ragione pratica per cui **conviene fare code review reciproca** man mano che si sviluppa, anche senza usare branch/PR formali: alla fine tutti devono capire tutto.

---

## Rubrica di valutazione del codice

Punteggio massimo: **30 punti**. Il voto in decimi si ottiene dividendo per 3 e arrotondando allo 0,25 più vicino. Il 30 sul codice pesa poi il 60% della valutazione complessiva del laboratorio (il restante 40% è l'orale).

### Voci e pesi

| voce                                       | punti max |
| ------------------------------------------ | --------- |
| Consegna e repo                            | 2         |
| Esecuzione                                 | 6         |
| Architettura e separazione                 | 5         |
| Leggibilità                                | 3         |
| Documentazione e devlog                    | 4         |
| Test unitari                               | 3         |
| Qualità git (storia, contributi, messaggi) | 3         |
| Uso dichiarato dell'IA                     | 1         |
| Obiettivi avanzati raggiunti               | 3         |
| Bonus/extra a discrezione del docente      | [-3, +3]  |

### Descrizione dei criteri

**Consegna e repo (2)**

- 2: consegnato nei tempi, repo pubblico, chiaro, tutte le istruzioni di setup funzionano.
- 1: consegna leggermente tardiva (entro 48 ore) o setup con piccole difficoltà.
- 0: non consegnato, consegna oltre 10 giorni di ritardo, repo privato/inaccessibile.

**Esecuzione (6)**

- 6: il gioco fa esattamente quello che richiede la specifica, nessun crash, input gestiti bene.
- 4-5: piccole discrepanze rispetto alla specifica o comportamenti scorretti in edge case.
- 1-3: molte specifiche non rispettate, crash su input plausibili, il gioco funziona solo in condizioni particolari.
- 0: non parte o non fa ciò che dovrebbe.

**Architettura e separazione (5)**

- 5: separazione netta fra logica pura e pygame. I moduli `rules`, `scoring`, `generator` non importano pygame. Macchina a stati chiara. Moduli con responsabilità ben definita.
- 3-4: separazione parziale, qualche accoppiamento evitabile, macchina a stati presente ma un po' confusa.
- 1-2: logica e presentazione intrecciate, moduli sovraccarichi, difficile dire dove sta cosa.
- 0: tutto in `main.py`.

**Leggibilità (3)**

- 3: naming significativo, indentazione consistente, a capo usati bene, codice organizzato.
- 2: problemi minori (qualche variabile con nome poco chiaro, qualche blocco da rompere).
- 1: almeno un problema grosso di leggibilità.
- 0: codice difficile da leggere in più punti.

**Documentazione e devlog (4)**

- 4: tutti i file `docs/` compilati con cura, devlog con entry settimanali sostanziose, spiegazioni chiare e onesti ragionamenti sulle scelte.
- 2-3: documentazione presente ma superficiale, devlog scarno o solo formale.
- 1: documentazione quasi assente o solo README minimale.
- 0: nessuna documentazione.

**Test unitari (3)**

- 3: i test forniti passano tutti **e** avete scritto test aggiuntivi (obiettivo avanzato) con copertura ragionevole di edge case.
- 2: i test forniti passano tutti, nessun test aggiuntivo scritto.
- 1: alcuni test forniti falliscono ma il gioco funziona comunque.
- 0: i test forniti non passano, oppure non sono stati integrati nel repository.

**Qualità git (3)**

- 3: storia coerente e distribuita nel tempo, messaggi chiari e significativi, contributo bilanciato dei membri, nessun commit assurdo.
- 2: storia ok ma con qualche problema (messaggi vaghi in diversi commit, sbilanciamento moderato fra i membri).
- 1: molti commit «update», cronologia concentrata negli ultimi giorni, forte sbilanciamento fra i membri.
- 0: un solo commit finale, un solo membro committa, nome/email non configurati.

**Uso dichiarato dell'IA (1)**

- 1: dichiarazione presente, granulare, coerente con quanto si vede nel codice.
- 0: dichiarazione assente, generica («abbiamo usato ChatGPT»), o palesemente incoerente con il codice.

**Obiettivi avanzati (3)**

Una scala morbida: il docente valuta quanto il progetto va oltre il minimo per la sufficienza. Fading completo, input multipli, stato PAUSED, metriche finali complete, seed funzionante, generatore ben bilanciato. Eventuale personalizzazione documentata. Massimo 3 punti, distribuiti a giudizio.

**Bonus/extra (-3, +3)**

A discrezione insindacabile del docente. Possono andare a premio di un'estensione particolarmente curata (audio, leaderboard), di un'idea originale, di un codice di qualità inusualmente alta. Possono anche essere sottratti per comportamento poco serio durante le tre settimane o per copia fra gruppi.

---

## Tabella di sintesi: cosa serve per la sufficienza

Per arrivare al **6** serve che siano veri contemporaneamente:

- il gioco è giocabile e rispetta il **core base** della specifica (stati `PLAYING`/`RESULTS`, scoring lineare, fading a soglia)
- timer, scoring base, generazione trial funzionano
- la separazione logica/pygame è rispettata (anche se non perfetta)
- i **test forniti** (`tests/test_rules.py` e `tests/test_scoring_base.py`) passano
- la documentazione minima c'è (README, un devlog anche stringato)
- la storia git mostra contributo di entrambi i membri
- l'uso dell'IA è dichiarato

Se manca anche solo uno di questi pezzi, è difficile raggiungere la sufficienza.

Per arrivare all'**8** o più, oltre al minimo serve che emergano almeno la maggior parte degli obiettivi avanzati e che la documentazione sia sostanziosa, non solo formale.

Per il **10** servono qualità uniforme alta su tutte le voci, almeno un'estensione bonus fatta bene, e un orale convincente.
