# Brain Shift — progetto di gruppo

## Chi siamo

- Daniele Mazzetti — daniele.mazzetti08@gmail.com / DanyMazze
- Thomas Addamo — thomas.addamo2@jcmaxwell.it / thomas-addamo

Classe 4A Informatica — a.s. 2025-26.

## Cos'è Brain Shift

Brain Shift è un gioco di logica che unisce velocità di ragionamento e memoria, il gioco consiste 
con la visione di una shermat con la successiva apparizione di una carta con una lettera e un numero, in base a dove è apparsa la carta (sopra o sotto) devi rispondere alla domanda "è pari?" o "è una vocale?", premendo la freccia sinista e quella destra della tastiera o cliccando i pulsanti a schermo SI/NO

## Come giocare

Istruzioni minime ma complete per far partire il gioco da clone pulito:

```bash
git clone https://github.com/thomas-addamo/BrainShift.git
cd brain_shift
pip install -r requirements.txt
python main.py
```

Specifiche:

- versione Python richiesta Python 3.14+
- versione pygame richiesta Pygame 2.6.1

## Controlli

- ← freccia sinistra: per dire SI
- → freccia destra: per dire NO

## Struttura del repository

Breve spiegazione di dove sta cosa:

```
BrainShift/
├── .git/                   ← metadati del repository Git
└── brain_shift/            ← sorgente principale del gioco
    ├── config.py           ← configurazione globale e costanti
    ├── generator.py        ← generazione delle carte / del contenuto di gioco
    ├── main.py             ← entry point dell’applicazione
    ├── models.py           ← modelli dati per carte, turno, ecc.
    ├── requirements.txt    ← dipendenze Python del progetto
    ├── rules.py            ← regole di gioco e logica delle risposte
    ├── scoring.py          ← sistema di punteggio e calcolo dei risultati
    ├── ui.py               ← interfaccia grafica e rendering con pygame
    ├── docs/               ← documentazione del progetto
    │   ├── architettura.md ← descrizione architetturale
    │   ├── devlog.md       ← diario di sviluppo
    │   ├── personalizzazioni.md ← note su personalizzazioni e varianti
    │   ├── README.md       ← documentazione generale del progetto
    │   ├── scelte.md       ← motivazioni delle scelte tecniche
    │   └── uso-ia.md       ← uso dell’intelligenza artificiale / logica
    └── tests/              ← test automatici del codice
        ├── conftest.py     ← configurazione pytest
        ├── test_rules.py   ← test delle regole di gioco
        ├── test_scoring_base.py ← test del sistema di scoring
        └── __pycache__/    ← file compilati Python (cache)
```

## Come lanciare i test

```bash
pytest tests/
```