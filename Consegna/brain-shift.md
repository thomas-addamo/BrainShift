
# Brain Shift: cambia regola, non cambia tasto

:::prereq Prerequisiti

- Tutti i laboratori pygame precedenti, in particolare [Breakout](../04-breakout/asset-2026-013-pygame-breakout.md)
- OOP in Python: classi, `__init__`, metodi
- Import tra moduli, organizzazione di un progetto su più file
- Git di base: clone, add, commit, push

:::

:::learn Cosa imparerai con questo esercizio

- Progettare un gioco pygame dividendo chiaramente **logica** e **presentazione**
- Usare `@dataclass` per rappresentare i dati del gioco (`Trial`)
- Gestire un timer di sessione e una schermata risultati
- Costruire un progetto software dalla specifica al prodotto funzionante
- Lavorare in coppia con git: commit piccoli, messaggi significativi, cronologia leggibile

:::

:::new Concetti nuovi

- Separazione fra moduli "puri" (logica) e moduli "pygame" (rendering)
- `@dataclass` per dati strutturati
- Generatore pseudorandom con seed configurabile
- Lancio di test pytest automatici forniti dal docente

:::

---

## Il gioco

**Brain Shift** è un gioco di *rapid task-switching*. Ogni trial mostra una carta in posizione alta o bassa sullo schermo. La carta contiene una lettera e un numero. La regola da applicare dipende dalla **posizione** della carta:

- carta in alto → «il numero è pari?»
- carta in basso → «la lettera è una vocale?»

La risposta è sempre binaria: **SÌ / NO**. La partita dura un minuto. Il giocatore deve rispondere più velocemente e più accuratamente possibile.

La difficoltà non sta nelle regole, che sono banali. Sta nel fatto che **la posizione della carta cambia imprevedibilmente** trial dopo trial: non puoi automatizzare una sola risposta, devi cambiare regola in testa a ogni carta.

---

## Specifica funzionale — versione base

Questa è la specifica del **gioco minimo**. Tutto quello che c'è qui è richiesto per la sufficienza. Nella sezione «Obiettivi avanzati» più sotto ci sono le estensioni per chi vuole di più.

### Trial

Ogni trial è un dato strutturato con almeno questi campi:

| campo             | tipo              | descrizione                                            |
| ----------------- | ----------------- | ------------------------------------------------------ |
| `position`        | `TOP` \| `BOTTOM` | dove appare la carta                                   |
| `letter`          | `str`             | una lettera maiuscola (A-Z, o sottoinsieme bilanciato) |
| `number`          | `int`             | un numero 1-9                                          |
| `expected_answer` | `bool`            | risposta corretta, derivata da `position`              |
| `user_answer`     | `bool \| None`    | risposta data dal giocatore                            |
| `is_correct`      | `bool`            | risultato della valutazione                            |

La `expected_answer` si calcola **solo** da `position`:

- `position == TOP` → `expected_answer = is_even(number)`
- `position == BOTTOM` → `expected_answer = is_vowel(letter)`

:::tip Cos'è una `dataclass`

Una `dataclass` è un modo rapido per creare una classe che serve solo a contenere dati. Invece di scrivere:

```python
class Trial:
    def __init__(self, position, letter, number, expected_answer):
        self.position = position
        self.letter = letter
        self.number = number
        self.expected_answer = expected_answer
```

scrivi:

```python
from dataclasses import dataclass

@dataclass
class Trial:
    position: str
    letter: str
    number: int
    expected_answer: bool
```

Python aggiunge automaticamente `__init__`, `__repr__` e `__eq__`. Lo crei così:

```python
t = Trial(position="TOP", letter="A", number=4, expected_answer=True)
print(t)  # Trial(position='TOP', letter='A', number=4, expected_answer=True)
```

I campi possono anche avere un **valore di default**:

```python
@dataclass
class Trial:
    position: str
    letter: str
    number: int
    expected_answer: bool
    user_answer: bool | None = None
    is_correct: bool = False
```

Per approfondire: [docs.python.org/3/library/dataclasses.html](https://docs.python.org/3/library/dataclasses.html).

:::

### Loop di gioco

1. Genera un nuovo trial.
2. Disegna la carta nella posizione corretta.
3. Attendi l'input del giocatore (tastiera o mouse).
4. Valuta la risposta, aggiorna il punteggio.
5. Mostra feedback breve (verde/rosso).
6. Vai subito al trial successivo.

La partita dura **60 secondi** dal primo trial. Allo scadere del timer mostra la schermata risultati.

### Input e controlli

Input binario veloce:

- `← freccia sinistra` = NO, `→ freccia destra` = SÌ

Basta la tastiera. Il mouse è un'estensione avanzata.

### Scoring base (lineare)

Molto semplice:

- risposta corretta: `+10 punti`
- risposta errata: nessun punto (o `-5`, a vostra scelta — documentatela)

Il sistema con **meter** e **moltiplicatore** del gioco originale è un obiettivo avanzato.

### Fading istruzioni — versione base

All'inizio della partita lo schermo mostra esplicitamente le due regole («TOP: numero pari?», «BOTTOM: vocale?»). Dopo che il giocatore ha dato **N risposte corrette** (es. 10), il testo delle regole scompare **di colpo**.

Il fading graduale con soglie progressive è un obiettivo avanzato.

### Generazione trial

Il generatore deve:

- alternare `TOP` e `BOTTOM` in modo casuale
- accettare un **seed** configurabile: lo stesso seed deve produrre la stessa sequenza di trial (serve per i test)

Il bilanciamento fine YES/NO e l'evitamento delle streak lunghe sono obiettivi avanzati.

### Stati di gioco — versione base

Per la versione base bastano **due stati**:

| stato     | funzione                                                              |
| --------- | --------------------------------------------------------------------- |
| `PLAYING` | timer attivo, trial, input, scoring                                   |
| `RESULTS` | score finale, numero risposte corrette/errate, pulsante per rigiocare |

Schermata introduttiva (`INTRO`) e pausa (`PAUSED`) sono obiettivi avanzati. Il gioco può partire direttamente quando lanci `python main.py`.

### Schermata risultati — versione base

Deve mostrare almeno:

- punteggio totale
- numero risposte corrette / errate
- accuratezza percentuale
- pulsante o tasto per rigiocare

---

## Architettura suggerita

La decomposizione in moduli è un suggerimento forte, ma siete liberi di organizzare diversamente purché la **separazione logica / pygame** sia rispettata.

```
brain_shift/
├── main.py          ← bootstrap, main loop, macchina a stati
├── config.py        ← costanti: colori, font, timing, punteggi
├── models.py        ← dataclass: Trial (e altri dati strutturati)
├── rules.py         ← is_even, is_vowel, compute_expected_answer
├── scoring.py       ← funzione che aggiorna il punteggio
├── generator.py     ← genera trial casuali con seed
├── ui.py            ← rendering HUD, carta, pulsanti
├── assets/          ← immagini, font, suoni (se usati)
└── tests/           ← test pytest forniti (li ricevete già pronti)
```

:::tip La regola che conta

I moduli `rules.py`, `scoring.py`, `generator.py`, `models.py` **non devono importare pygame**. Sono logica pura. Se lo fanno, non sono più testabili senza aprire una finestra, e la parte architetturalmente più interessante del progetto salta.

Regola pratica: se hai scritto `import pygame` in uno di questi quattro file, hai sbagliato qualcosa.

:::

---

## Test forniti

Non dovete scrivere test per la versione base: vi forniamo noi una piccola batteria in `tests/`. Sono **parte del progetto**: il voto sulla voce «Test» della rubrica dipende dal fatto che questi test **passino**.

Per lanciarli:

```bash
pip install pytest
pytest tests/
```

Imparare a leggere i test forniti è utilissimo: sono la specifica formale di cosa devono fare `rules.py` e `scoring.py`. Se un test fallisce, leggete il nome del test e il messaggio di errore: vi dice esattamente cosa non torna.

Scrivere i **vostri** test aggiuntivi è un obiettivo avanzato.

:::tip Facciamo una lezione insieme

Prima della consegna faremo una lezione apposita su come funzionano i test pytest, come leggerli, come lanciarli, come scriverne di nuovi. Nel frattempo potete usare quelli forniti senza averli studiati a fondo: `pytest tests/` vi dice rosso o verde, e basta per iniziare.

:::

---

## Guida operativa passo-passo

Questa è la parte più importante di questo documento. Seguitela nell'ordine: ogni fase costruisce su quelle precedenti. Non saltate avanti.

### Fase 0 — Setup (giorno 1)

1. Create un repository pubblico su GitHub (uno dei due lo crea, invita l'altro come collaboratore).
2. Clonatelo entrambi in locale.
3. Create questa struttura di cartelle vuote:

   ```
   brain_shift/
   ├── main.py
   ├── config.py
   ├── models.py
   ├── rules.py
   ├── scoring.py
   ├── generator.py
   ├── ui.py
   ├── requirements.txt
   ├── README.md
   └── tests/        ← copiate qui i test forniti
   ```

4. In `requirements.txt`:

   ```
   pygame
   pytest
   ```

5. Copiate i file `tests/test_rules.py` e `tests/test_scoring_base.py` forniti dal docente nella cartella `tests/`.
6. Fate il primo commit («initial project structure»).

### Fase 1 — Le regole (giorno 1-2)

In `rules.py` scrivete due funzioni pure:

```python
def is_even(number: int) -> bool:
    ...

def is_vowel(letter: str) -> bool:
    ...
```

Poi una terza che combina le prime due:

```python
def compute_expected_answer(position: str, letter: str, number: int) -> bool:
    ...
```

Lanciate `pytest tests/test_rules.py`. Deve essere tutto verde prima di andare avanti.

### Fase 2 — I dati (giorno 2)

In `models.py` definite la `dataclass` `Trial` (vedi sopra il callout su dataclass). Mettete tutti i campi che vi servono. Per ora `is_correct` e `user_answer` possono avere default `False` e `None`.

### Fase 3 — Il generatore (giorno 2-3)

In `generator.py` scrivete una funzione:

```python
def generate_trial(rng) -> Trial:
    ...
```

`rng` è un oggetto `random.Random` passato da fuori. **Non usate `random.choice` direttamente**: create sempre l'oggetto `rng` in `main.py` con un seed (anche fisso, es. `42`) e passatelo al generatore. Così potete riprodurre le partite.

Il generatore sceglie:

- `position` fra `TOP` e `BOTTOM`
- `letter` fra le lettere maiuscole
- `number` fra 1 e 9
- calcola `expected_answer` chiamando `compute_expected_answer`

### Fase 4 — Lo scoring (giorno 3)

In `scoring.py` scrivete una funzione:

```python
def apply_answer(score: int, is_correct: bool) -> int:
    ...
```

Restituisce il nuovo punteggio: `score + 10` se corretto, altrimenti `score` (o `score - 5`, a vostra scelta).

Lanciate `pytest tests/test_scoring_base.py`. Verde.

### Fase 5 — La finestra pygame (giorno 3-4)

In `main.py`:

1. Inizializzate pygame (`pygame.init()`).
2. Create una finestra di dimensioni ragionevoli (es. 800×600).
3. Create un `Clock` e scrivete il main loop base: gestione eventi, `pygame.display.flip()`, `clock.tick(60)`.
4. Fate in modo che il gioco si chiuda premendo ESC o X.

**Non** disegnate ancora niente. Fate solo la finestra nera.

### Fase 6 — Disegnare la carta (giorno 4-5)

In `ui.py` scrivete una funzione che disegna una carta:

```python
def draw_card(surface, trial, config):
    ...
```

La carta è un rettangolo (usate `pygame.draw.rect`) con dentro lettera e numero. La `y` dipende da `trial.position`: in alto se `TOP`, in basso se `BOTTOM`.

In `main.py` generate un trial all'inizio e chiamate `draw_card` nel loop. Lanciate il gioco: dovete vedere la carta.

### Fase 7 — Input e risposta (giorno 5-6)

In `main.py`, nel gestore eventi:

- se l'utente preme `→`, `user_answer = True`
- se preme `←`, `user_answer = False`
- calcolate `is_correct = (user_answer == trial.expected_answer)`
- aggiornate lo score con `apply_answer`
- generate un nuovo trial
- tenete un contatore di corrette e sbagliate

A questo punto il gioco è già giocabile senza feedback visivo. Provatelo.

### Fase 8 — Timer e schermata risultati (giorno 6-8)

1. Al primo trial salvate `start_time = time.time()`.
2. A ogni frame calcolate `elapsed = time.time() - start_time`.
3. Se `elapsed >= 60`, passate allo stato `RESULTS`.
4. Aggiungete una variabile `state` che può valere `"PLAYING"` o `"RESULTS"`.
5. In `PLAYING` eseguite il loop normale. In `RESULTS` disegnate il riepilogo.
6. Mostrate il timer in alto sullo schermo durante il gioco (conto alla rovescia).
7. Nella schermata risultati mostrate: punteggio, corrette, sbagliate, accuratezza, «premi R per rigiocare».
8. Premendo `R` reimpostate tutto e tornate in `PLAYING`.

### Fase 9 — Feedback visivo (giorno 8-9)

Quando l'utente risponde:

- per 100-150 ms la carta diventa verde (corretta) o rossa (errata)
- poi appare subito la carta successiva

Attenzione: non usate `pygame.time.wait` perché blocca il loop. Tenete un `feedback_until = time.time() + 0.15` e controllate ad ogni frame se il feedback è ancora attivo.

### Fase 10 — Fading istruzioni base (giorno 9)

Aggiungete il testo delle due regole in alto/basso, grigio chiaro. Quando `corrette >= 10` (o una soglia a vostra scelta), smettete di disegnarlo.

### Fase 11 — Polish, documentazione, consegna (giorno 9-finale)

- aggiungete colori decenti, font leggibili
- scrivete il README e riempite `docs/`
- controllate che `pytest tests/` passi
- controllate che `python main.py` funzioni da clone pulito
- scrivete il devlog con tutte le entry settimanali

A questo punto il gioco base è finito. Chi vuole passa agli **obiettivi avanzati**.

---

## Obiettivi minimi (sufficienza)

Elenco completo di cosa serve per la sufficienza:

- macchina a stati con `PLAYING` e `RESULTS`
- generazione trial con seed configurabile
- input da tastiera (frecce) funzionante
- scoring lineare (+10 corretto, 0 o -5 errato)
- timer di sessione a 60 secondi
- schermata risultati con score, corrette/errate, accuratezza
- feedback visivo verde/rosso non bloccante
- istruzioni delle regole che scompaiono dopo N corrette
- separazione fra logica e pygame rispettata
- **i test forniti passano** (`pytest tests/` tutto verde)
- repository GitHub con storia git leggibile e contributo di entrambi i membri
- documentazione compilata (`docs/`)

---

## Obiettivi avanzati

Quelli che vogliono puntare in alto aggiungono cose in questa lista, progressivamente. Non servono tutte, ma più ne fate meglio è.

### Scoring con meter e moltiplicatore

Il sistema di scoring del gioco originale è più ricco e interessante.

**Stato**: `score`, `multiplier` (parte da 1), `meter` (parte da 0).

**Ogni risposta corretta**:

- `score += 50 * multiplier`
- `meter += 1`
- se `meter == 4`: `multiplier = min(multiplier + 1, 10)` e `meter = 0`

**Ogni risposta errata**:

- se `meter > 0`: `meter = 0`
- altrimenti: `multiplier = max(multiplier - 1, 1)`

**A fine partita**: `score += 250 * multiplier` (bonus finale).

:::tip Cosa sono meter e multiplier, con un esempio

Pensateli come due barre sovrapposte:

- il **meter** è una barra piccola che si riempie di uno ogni risposta corretta (da 0 a 3). Quando arriva a 4, si svuota e il moltiplicatore sale di un livello. È la «barra della streak».
- il **multiplier** è il moltiplicatore dei punti. Al livello 1 ogni corretta vale 50 punti, al livello 2 vale 100, al livello 3 vale 150, fino a 500 al livello 10.

Esempio di sei trial consecutivi, partendo da `score=0, multiplier=1, meter=0`:

| trial | esito    | score dopo | multiplier | meter |
| ----- | -------- | ---------- | ---------- | ----- |
| 1     | corretta | 50         | 1          | 1     |
| 2     | corretta | 100        | 1          | 2     |
| 3     | corretta | 150        | 1          | 3     |
| 4     | corretta | 200        | 2          | 0     | ← level up! meter si resetta                |
| 5     | corretta | 300        | 2          | 1     | ← +100 perché multiplier=2                  |
| 6     | errata   | 300        | 2          | 0     | ← meter era >0: si azzera, multiplier resta |

Se fosse venuta una settima errata con meter=0, allora `multiplier` sarebbe sceso a 1.

Questo scoring premia la **costanza** più della velocità: fare streak lunghe vale molto più che rispondere tanto a caso. Perdere una streak quando il moltiplicatore è alto fa più male che sbagliare all'inizio.

:::

### Fading progressivo

Sostituite il fading «on/off» con una transizione graduale:

| risposte corrette cumulative | opacità istruzioni |
| ---------------------------- | ------------------ |
| 0-3                          | 100%               |
| 4-7                          | 70%                |
| 8-11                         | 40%                |
| 12+                          | 0%                 |

Se il giocatore sbaglia molte risposte consecutive, le istruzioni possono riapparire parzialmente.

### Inter-trial interval

Invece di passare immediatamente al trial successivo, aspettate 100-250 ms dopo il feedback. Serve a dare ritmo al gioco ed evita che una sequenza di risposte rapidissime risulti confusa.

### Stato `INTRO`

Schermata iniziale con titolo, istruzioni esplicite, controlli e pulsante/tasto per iniziare. Il gioco non parte finché l'utente non preme «Start».

### Stato `PAUSED`

Premendo `P` il timer si ferma, viene mostrata una schermata di pausa, premendo di nuovo `P` si riprende. Non banale: il `start_time` va «congelato» correttamente.

### Input mouse e normalizzazione

Aggiungete due pulsanti cliccabili YES/NO sullo schermo. Internamente normalizzate tutto in un unico evento logico (`ANSWER_YES`, `ANSWER_NO`), così scoring e statistiche non sanno se l'utente ha usato tastiera o mouse.

### Generatore migliorato

- evitare streak di `position` oltre una lunghezza massima (es. 3)
- bilanciare attivamente `YES`/`NO` sul medio periodo
- documentare come lo verificate

### Test unitari scritti da voi

In aggiunta ai test forniti, scrivete i vostri. Esempi di cosa testare:

- saturazione del moltiplicatore a 10
- decremento del moltiplicatore quando il meter è vuoto e si sbaglia
- applicazione del bonus finale
- invarianza del seed: due generatori con lo stesso seed producono la stessa sequenza

### Metriche estese nella schermata risultati

- moltiplicatore massimo raggiunto
- moltiplicatore finale
- tempo medio di risposta
- best streak
- bonus finale applicato

### Personalizzazione del gioco

Potete personalizzare tema grafico, asset visivi, suoni, e varianti di gameplay — **a patto di mantenere invariato il core cognitivo**:

- due regole contestuali diverse a seconda della posizione della carta
- risposta binaria
- durata 60 secondi

Se personalizzate, documentate le vostre scelte in `docs/personalizzazioni.md`: quali regole avete scelto, perché, come avete verificato che il gioco resti equilibrato. È lavoro in più — per chi ha tempo e voglia.

---

## Estensioni bonus (non obbligatorie)

Poche e mirate. Scegline al massimo due, se le fate.

- **Audio**: effetti sonori brevi per risposta corretta/errata e level-up. Usate `pygame.mixer`.
- **Leaderboard locale persistente**: salva i top 5 score in un file JSON locale. Mostra la classifica nella schermata risultati. Attento a dove salvi il file (path relativo al progetto).

---

## Consiglio finale

L'errore più comune in un progetto così è partire da `main.py` con pygame e cercare di far funzionare subito «qualcosa che si vede». Questo approccio porta a un codice in cui scoring, regole e rendering sono intrecciati, impossibili da debuggare quando qualcosa non torna.

Seguite la guida operativa nell'ordine: le prime quattro fasi non coinvolgono pygame. Sembrano noiose, ma danno un fondamento solido. Quando nella fase 5 aprite la finestra, avete già metà del lavoro alle spalle — e la parte più facile davanti.
