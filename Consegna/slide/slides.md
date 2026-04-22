---
theme: slidev-theme-cyberpunk-ide
title: "Brain Shift — Laboratorio valutato 4A Info"
transition: none
lineNumbers: false
themeConfig:
  tabsShowAll: false
---

# Brain *Shift*

Laboratorio valutato di pygame — 4A Informatica

Marco Farina — aprile/maggio 2026

---
layout: section
section: Capitolo 1
---

# Il *gioco*

---
filename: cose-brain-shift.md
language: Markdown
branch: brain-shift/gioco
repo: paideia-os
---

# Cos'è *Brain Shift*

Un gioco di **rapid task-switching** che dura esattamente un minuto.

Sullo schermo compare una carta con **una lettera e un numero**. A seconda di dove appare, cambia la regola che devi applicare.

Tu rispondi **SÌ o NO**. Il gioco conta quante ne azzecchi prima che scada il tempo.

:::info La sfida cognitiva
Le regole sono banali. Difficile è **cambiarle in testa** carta dopo carta, senza esitare.
:::

---
filename: le-due-regole.md
language: Markdown
branch: brain-shift/gioco
repo: paideia-os
---

# Le due *regole*

La posizione della carta determina la domanda implicita.

- Carta in **alto** → *«il numero è pari?»*
- Carta in **basso** → *«la lettera è una vocale?»*

Risposta sempre binaria: `←` NO, `→` SÌ.

Dopo alcune risposte corrette, le istruzioni **spariscono**. A quel punto le regole devi ricordartele.

---
filename: esempio-trial.md
language: Markdown
branch: brain-shift/gioco
repo: paideia-os
---

# Un *esempio*

<img src="/assets/brain-shift.svg" alt="testo" style="width: 70%; max-width: 100%; margin: 0 auto;" />


---
layout: section
section: Capitolo 2
---

# Cosa *costruite*

---
filename: specifica-base.md
language: Markdown
branch: brain-shift/base
repo: paideia-os
---

# Specifica *base*

Questo è il gioco minimo. Tutto qui è richiesto per la sufficienza.

- Finestra pygame, carta in alto/in basso con lettera e numero
- Input tastiera: `←` NO, `→` SÌ
- **Scoring lineare**: +10 se corretta, 0 o -5 se errata (scegliete)
- Timer di **60 secondi**
- Due stati: `PLAYING` e `RESULTS`
- Istruzioni che **scompaiono dopo N corrette**
- Feedback verde/rosso non bloccante

:::info Il resto è avanzato
Moltiplicatore, fading graduale, pausa, INTRO: tutto bonus.
:::

---
filename: trial-dataclass.py
language: Python
branch: brain-shift/base
repo: paideia-os
---

# Il dato: `Trial`

Usate `@dataclass` per rappresentare ogni singolo trial.

```python
from dataclasses import dataclass

@dataclass
class Trial:
    position: str           # "TOP" o "BOTTOM"
    letter: str             # "A"-"Z"
    number: int             # 1-9
    expected_answer: bool   # calcolato da position
    user_answer: bool | None = None
    is_correct: bool = False
```

Python aggiunge automaticamente `__init__`, `__repr__`, `__eq__`.

---
filename: scoring-base.py
language: Python
branch: brain-shift/base
repo: paideia-os
---

# Scoring *lineare*

La firma attesa dai test forniti.

```python
# scoring.py

def apply_answer(score: int, is_correct: bool) -> int:
    """Restituisce il nuovo punteggio."""
    if is_correct:
        return score + 10
    return score          # oppure: return score - 5
```

Funzione **pura**: stessi argomenti → stesso risultato, nessun side effect.

:::info Coerenza
Se scegliete `-5` per le errate, applicatelo sempre. I test lo verificano.
:::

---
layout: section
section: Capitolo 3
---

# *Architettura*

---
filename: separazione.md
language: Markdown
branch: brain-shift/architettura
repo: paideia-os
---

# Separazione *logica / pygame*

La scelta architetturale più importante del progetto.

- Moduli **puri** (niente pygame): `rules`, `scoring`, `generator`, `models`
- Moduli **pygame**: `main`, `ui`, `states`

La logica pura è testabile senza aprire una finestra. È anche più semplice da debuggare: se il gioco non torna, sai dove guardare.

:::warning Regola di controllo
Se hai scritto `import pygame` in `rules.py`, `scoring.py`, `generator.py` o `models.py`, hai sbagliato qualcosa.
:::

---
layout: two-columns
cols: 2-2
filename: struttura-moduli.md
language: Markdown
branch: brain-shift/architettura
repo: paideia-os
---

# Struttura *consigliata*

::left::

**Moduli puri**

- `rules.py` — `is_even`, `is_vowel`
- `models.py` — dataclass `Trial`
- `generator.py` — crea trial con seed
- `scoring.py` — `apply_answer`

Niente import di pygame qui dentro.

::right::

**Moduli pygame**

- `main.py` — loop, stati
- `ui.py` — disegno carta, HUD
- `config.py` — colori, font, costanti

E poi: `tests/`, `docs/`, `assets/`, `requirements.txt`, `README.md`.

---
layout: section
section: Capitolo 4
---

# Guida *operativa*

---
filename: fasi-logica.md
language: Markdown
branch: brain-shift/guida
repo: paideia-os
---

# Prima la *logica* (1-4)

Quattro fasi prima di aprire pygame.

- **Fase 0** — setup repo, struttura cartelle, `requirements.txt`
- **Fase 1** — `rules.py` (`is_even`, `is_vowel`, `compute_expected_answer`) + test
- **Fase 2** — `models.py` con la dataclass `Trial`
- **Fase 3** — `generator.py` con seed configurabile
- **Fase 4** — `scoring.py` lineare + test

:::info Il momento magico
A fine fase 4 avete un gioco che funziona *senza interfaccia*. I test sono verdi. Il difficile è fatto.
:::

---
filename: fasi-pygame.md
language: Markdown
branch: brain-shift/guida
repo: paideia-os
---

# Poi *pygame* (5-8)

Quattro fasi per mettere il gioco a schermo.

- **Fase 5** — finestra pygame, main loop vuoto, chiusura con ESC
- **Fase 6** — `ui.py` disegna la carta (posizione, lettera, numero)
- **Fase 7** — input frecce, aggiornamento score, trial successivo
- **Fase 8** — timer 60s, stato `RESULTS`, schermata risultati, `R` per rigiocare

A fine fase 8 il gioco è giocabile dall'inizio alla fine.

---
filename: fasi-polish.md
language: Markdown
branch: brain-shift/guida
repo: paideia-os
---

# Infine il *polish* (9-11)

Tre fasi per portarlo a livello di consegna.

- **Fase 9** — feedback visivo verde/rosso (non bloccante, timestamp)
- **Fase 10** — fading istruzioni dopo N corrette
- **Fase 11** — colori, font, README, `docs/`, devlog, verifica test verdi

:::warning Attenzione al feedback
Non usate `pygame.time.wait`: blocca il loop. Usate un timestamp futuro e controllate ogni frame.
:::

---
layout: section
section: Capitolo 5
---

# *Test* pytest

---
filename: test-forniti.md
language: Markdown
branch: brain-shift/test
repo: paideia-os
---

# Test *forniti*

Non dovete scriverli. Ve li dò io.

- `tests/test_rules.py` — 18 test su `is_even`, `is_vowel`, `compute_expected_answer`
- `tests/test_scoring_base.py` — 7 test su `apply_answer` lineare
- `tests/conftest.py` — configurazione path

Per lanciarli:

```bash
pip install pytest
pytest tests/
```

:::info Lezione dedicata
Prima della consegna faremo una lezione apposita su come funzionano pytest, le assert, i messaggi di errore.
:::

---
filename: test-letti.py
language: Python
branch: brain-shift/test
repo: paideia-os
---

# Leggere un *test*

Un test forniti di esempio — vale la pena capirlo.

```python
def test_is_even_with_even_number():
    """Un numero pari deve dare True."""
    assert is_even(4) is True

def test_is_even_with_odd_number():
    """Un numero dispari deve dare False."""
    assert is_even(3) is False
```

Se il test fallisce, pytest vi dice il **nome del test** e il **messaggio**. Quasi sempre basta leggerli per capire dove correggere.

---
layout: section
section: Capitolo 6
---

# Oltre la *base*

---
filename: obiettivi-avanzati.md
language: Markdown
branch: brain-shift/avanzati
repo: paideia-os
---

# Obiettivi *avanzati*

Non servono per il 6, servono per l'8 e il 10.

- **Scoring con meter e moltiplicatore** (come il gioco originale)
- **Fading graduale** con soglie progressive
- **Inter-trial interval** di 100-250 ms
- **Stati** `INTRO` e `PAUSED`
- **Input mouse** con normalizzazione a evento logico
- **Generatore migliorato** che evita streak di posizione
- **Metriche estese** nei risultati finali
- **Test scritti da voi** oltre ai forniti

---
filename: meter-multiplier.md
language: Markdown
branch: brain-shift/avanzati
repo: paideia-os
---

# Meter e *moltiplicatore*

Il sistema di scoring del gioco originale. Premia la **costanza**.

| trial | esito | score | mult  | meter |
| ----- | ----- | ----- | ----- | ----- |
| 1     | ✓     | 50    | 1     | 1     |
| 2     | ✓     | 100   | 1     | 2     |
| 3     | ✓     | 150   | 1     | 3     |
| 4     | ✓     | 200   | **2** | 0     |
| 5     | ✓     | 300   | 2     | 1     |
| 6     | ✗     | 300   | 2     | 0     |

Meter pieno (4) → multiplier sale. Errata con meter > 0 → azzera meter. Errata con meter = 0 → decrementa mult.

---
filename: fading-graduale.md
language: Markdown
branch: brain-shift/avanzati
repo: paideia-os
---

# Fading *graduale*

Nella versione base le istruzioni scompaiono di colpo. In avanzato, svaniscono con soglie.

| risposte corrette | opacità |
| ----------------- | ------- |
| 0 – 3             | 100%    |
| 4 – 7             | 70%     |
| 8 – 11            | 40%     |
| 12+               | 0%      |

Questo trasforma il gioco da «leggi e applica» a «ricorda e applica». È il cuore cognitivo del design.

---
filename: bonus.md
language: Markdown
branch: brain-shift/avanzati
repo: paideia-os
---

# *Bonus* facoltativi

Pochi, mirati. Al massimo due.

- **Audio** — effetti sonori brevi per corretta, errata, level-up. Usate `pygame.mixer`.
- **Leaderboard locale** — top 5 salvati in un file JSON, mostrati nella schermata risultati.

:::info Personalizzazione
Potete cambiare tema, asset, persino le due regole — purché il **core cognitivo** resti invariato. Lavoro in più da documentare.
:::

---
layout: section
section: Capitolo 7
---

# *Assignment*

---
filename: tempi-consegna.md
language: Markdown
branch: brain-shift/assignment
repo: paideia-os
---

# Tempi e *consegna*

Il calendario del progetto.

- **Assegnazione**: mercoledì 22 aprile 2026 (oggi)
- **Consegna**: **domenica 17 maggio 2026, ore 23:59**
- **Durata**: circa 3 settimane e mezza di lavoro

Consegnate inviando il **link al repository GitHub pubblico**. Niente zip, niente Drive, niente allegati.

:::warning Dopo le 23:59 di domenica 17
Il repo non deve più ricevere commit fino all'orale. Commit successivi = consegna tardiva.
:::

---
filename: gruppi.md
language: Markdown
branch: brain-shift/assignment
repo: paideia-os
---

# *Gruppi*

Come vi organizzate.

- **Coppie** (default) — libera scelta
- **Trii** — solo su richiesta, con **un'estensione bonus obbligatoria**
- Il voto è **individuale**, non di gruppo
- Ogni membro deve saper spiegare **tutto** il codice all'orale

:::info Consiglio
Fate code review reciproca man mano. Chi non conosce la parte del compagno all'orale paga dazio sul proprio voto.
:::

---
filename: git-come.md
language: Markdown
branch: brain-shift/assignment
repo: paideia-os
---

# *Git*: come va usato

La storia git è parte della valutazione.

- **Commit frequenti, atomici, messaggi significativi**
- Non «update» o «fix»: *«aggiunge test per scoring con multiplier saturo»*
- **Contributo bilanciato**: entrambi i membri devono avere commit a loro nome
- **Cronologia distribuita** nel tempo, non 200 commit nelle ultime 24 ore
- Configurate nome e cognome reali con `git config`

Branch e pull request non sono obbligatori, ma sono apprezzati.

---
filename: uso-ia.md
language: Markdown
branch: brain-shift/assignment
repo: paideia-os
---

# Uso dell'*IA*

Consentita come assistente, **non come risolutore**.

- ✓ Chiedere spiegazioni, chiarimenti, debugging
- ✓ Farsi suggerire codice di dettaglio, capito e integrato
- ✗ Consegnare codice che non sapete spiegare all'orale
- ✗ Farle scrivere **`scelte.md`, `devlog.md`, `uso-ia.md`**

Dichiarazione **granulare** obbligatoria in `docs/uso-ia.md`: per ogni uso, *dove*, *cosa avete chiesto*, *cosa avete accettato o rifiutato*.

:::warning Onestà prima di tutto
Nascondere l'uso dell'IA pesa molto di più che dichiararlo. All'orale si vede.
:::

---
filename: docs-struttura.md
language: Markdown
branch: brain-shift/assignment
repo: paideia-os
---

# *Documentazione*

Una cartella `docs/` con più file. Il canovaccio ve lo fornisco io.

- `docs/README-progetto.md` — overview pubblico
- `docs/architettura.md` — moduli, macchina a stati, diagrammi
- `docs/scelte.md` — decisioni, alternative scartate
- `docs/uso-ia.md` — trasparenza granulare sull'IA
- `docs/devlog.md` — diario settimanale di gruppo
- `docs/personalizzazioni.md` — solo se avete personalizzato

:::warning Metacognizione senza IA
`scelte.md`, `devlog.md`, `uso-ia.md`: scritti da voi, non dall'IA.
:::

---
filename: rubrica.md
language: Markdown
branch: brain-shift/assignment
repo: paideia-os
---

# *Rubrica* codice (30 pt)

Peso: **60%** del voto finale (l'altro 40% è l'orale).

| voce            | pt  | voce               | pt  |
| --------------- | --- | ------------------ | --- |
| Consegna e repo | 2   | Test               | 3   |
| Esecuzione      | 6   | Qualità git        | 3   |
| Architettura    | 5   | Uso dichiarato IA  | 1   |
| Leggibilità     | 3   | Obiettivi avanzati | 3   |
| Documentazione  | 4   | Bonus/extra        | ±3  |

Voto in decimi = punti ÷ 3, arrotondato allo 0,25.

---
filename: orale.md
language: Markdown
branch: brain-shift/assignment
repo: paideia-os
---

# L'*orale* (40%)

Una settimana dopo la consegna, in aula, 15-20 minuti a gruppo.

- Il docente **clona il repo** e fa partire il gioco
- Vi chiede di **navigare il codice** mentre fa domande mirate
- Vi chiede di spiegare **perché** avete fatto certe scelte
- Vi chiede di raccontare la **storia git**: chi ha fatto cosa
- Può chiedere di **modificare qualcosa al volo**

Valutazione **individuale**. Ciascuno risponde su tutto, non solo sulla propria parte.

---
layout: section
section: Capitolo 8
---

# Si *parte*

---
filename: checklist-6.md
language: Markdown
branch: brain-shift/partenza
repo: paideia-os
---

# Cosa serve per il *6*

Checklist minima per la sufficienza.

- Gioco giocabile, core base della specifica
- Stati `PLAYING` e `RESULTS`
- Scoring lineare, timer 60s, schermata risultati
- Feedback verde/rosso non bloccante
- Istruzioni che scompaiono dopo N corrette
- Separazione logica/pygame rispettata
- **Test forniti passano** (`pytest tests/`)
- Repo GitHub pubblico, storia git leggibile, entrambi committate
- `docs/` compilato, uso IA dichiarato

---
filename: prossimi-passi.md
language: Markdown
branch: brain-shift/partenza
repo: paideia-os
---

# Prossimi *passi*

Cosa fare oggi e nei prossimi giorni.

- **Oggi**: formate i gruppi, create il repo pubblico su GitHub
- **Entro domani**: struttura cartelle, `requirements.txt`, primo commit
- **Questa settimana**: completate le fasi 1-4 (logica pura, test verdi)
- **Settimana prossima**: pygame, disegno, input, timer
- **Ultima settimana**: polish, documentazione, devlog, rilettura

:::info Domande?
Il laboratorio è ampio ma guidato. Ogni fase è piccola. Partite dalle regole, non da pygame.
:::

---
layout: section
section: Fine
---

# Buon *lavoro*
