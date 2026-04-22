# Scelte implementative

> Qui va la parte più **metacognitiva** del progetto: cosa avete scelto, perché, cosa avete scartato. Non può essere scritta dall'IA — è il ragionamento che mostra che avete capito quello che avete fatto.

## Scelte rilevanti

Per ciascuna scelta non banale che avete fatto, scrivete:

1. **Cosa**: la scelta in una riga.
2. **Perché**: la ragione. Vincoli? Pregi? Abitudine?
3. **Alternative considerate**: almeno una alternativa che avete valutato e scartato.
4. **Conseguenze**: cosa è diventato facile e cosa è diventato difficile per colpa di questa scelta.

### Esempio di formato

**Scelta**: rappresentiamo la posizione della carta con un `Enum` (`Position.TOP`, `Position.BOTTOM`) invece che con una stringa.

**Perché**: autocompletamento nell'IDE, impossibile passare un valore errato per sbaglio, codice più leggibile nei `match`.

**Alternative considerate**: stringhe ("top", "bottom"). Scartata perché troppo facile scrivere "Top" invece di "top" e introdurre un bug silenzioso.

**Conseguenze**: un import in più nei moduli che usano la posizione; nessuno svantaggio concreto.

---

## Sezioni da trattare

Non dovete coprire tutte queste sezioni in modo rigido: sceglietene le più rilevanti per il vostro progetto e approfonditele.

### Struttura del progetto

Perché quella decomposizione in moduli? Avete valutato un'unica libreria `game.py`?

### Scoring

Come avete tradotto la formula della specifica in codice? `dict` mutabile, `dataclass` mutabile, funzioni pure che restituiscono un nuovo stato?

### Generatore

Che algoritmo usate per bilanciare YES/NO? Rigenerate i trial sbilanciati o aggiustate dopo? Come gestite il seed?

### Gestione del tempo

Come tenete traccia del timer di sessione? `time.time()`, `pygame.time.get_ticks()`, `Clock`? Perché?

### Inter-trial interval

Come lo realizzate senza bloccare il main loop? Variabile di stato + timer? Timestamp della prossima transizione?

### Input

Se avete input multipli, come li normalizzate? Dove avviene la normalizzazione?

### Feedback visivo

Come evitate che le animazioni rallentino il loop? Se è un'animazione "a tempo" come la gestite (stato + timestamp)?

### Fading istruzioni

Interpolazione lineare, soglie discrete, funzione ease? Come l'avete implementato?

### Asset grafici / audio

Se ne avete usati, da dove vengono? Licenza? Come li caricate (a init, a richiesta)?

---

## Cosa non siamo riusciti a fare e perché

Parte importante. Onestà, non scuse.

- cosa avete lasciato fuori
- cosa avete iniziato e poi abbandonato
- cosa sapete che è fatto male ma non abbiamo avuto tempo di sistemare

Riconoscere i limiti del proprio progetto è una competenza professionale, non una debolezza.

---

### Domande-guida

1. Un lettore capisce **perché** le cose sono come sono, o solo **come** sono?
2. Ogni scelta descritta ha almeno un'alternativa scartata?
3. Avete evitato frasi tipo «abbiamo scelto così perché è il modo migliore»? (Non è una spiegazione.)
4. Questa pagina è scritta da voi, con il vostro stile, o sembra l'output di un'IA?
