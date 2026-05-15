# Personalizzazioni
 
## Cosa abbiamo personalizzato
 
### 1. Controlli invertiti rispetto alla specifica
 
**Cosa:** La specifica dice `← sinistra = NO`, `→ destra = SÌ`. Nel nostro gioco è il contrario: `← sinistra = SÌ`, `→ destra = NO`.
 
**Perché:** Abbiamo trovato più intuitivo associare la freccia sinistra a "sì" nel contesto del gioco, anche se è opposto alla convenzione indicata. È una scelta soggettiva che abbiamo fatto all'inizio dell'implementazione e mantenuto per coerenza.
 
**Come abbiamo verificato che il core cognitivo resti invariato:** Il meccanismo di task-switching non dipende da quale tasto corrisponde a SÌ o NO — dipende dal fatto che la risposta sia binaria e contestuale alla posizione della carta. La risposta attesa (`expected_answer`) viene calcolata indipendentemente dalla mappatura dei tasti. Abbiamo verificato che i test passano correttamente, poiché i test controllano la logica delle regole, non il binding dei tasti.
 
---
 
### 2. Pulsanti SI/NO cliccabili con il mouse
 
**Cosa:** Oltre all'input da tastiera, abbiamo aggiunto due pulsanti `SI` e `NO` nella barra in basso, cliccabili con il mouse.
 
**Perché:** L'input mouse è citato nella specifica come obiettivo avanzato. Abbiamo scelto di implementarlo perché migliora l'accessibilità del gioco e rende più immediato l'utilizzo per chi non ha familiarità con la tastiera.
 
**Come abbiamo verificato che il core cognitivo resti invariato:** I pulsanti SI e NO producono esattamente lo stesso effetto delle frecce corrispondenti. La normalizzazione avviene in `main.py`: sia il click che la pressione del tasto chiamano `submit_answer` con lo stesso valore booleano, senza nessuna differenza nel calcolo del punteggio o nella logica di gioco.
 
---
 
### 3. Feedback visivo con icona ✓/✗ invece del solo cambio di colore
 
**Cosa:** Oltre al cambio di colore della carta (verde per corretto, rosso per errato), disegniamo un'icona grafica — una spunta (✓) per le risposte corrette e una X per quelle errate — al centro dello schermo durante il feedback.
 
**Perché:** Il solo cambio di colore ci sembrava poco leggibile a colpo d'occhio, specie in una partita rapida. L'icona rende il feedback più immediato e riconoscibile anche per chi ha difficoltà nella percezione dei colori.
 
**Come abbiamo verificato che il core cognitivo resti invariato:** L'icona è puramente visiva e non modifica nessun aspetto della logica. La durata del feedback è controllata da `config.FEEDBACK_DURATION` e vale 0.35 secondi, come da specifica. Non influenza il timer, lo scoring o la generazione del trial successivo.
 
---
 
### 4. Pausa tra un trial e il successivo (inter-trial interval)
 
**Cosa:** Dopo il feedback visivo, prima che appaia il trial successivo, c'è una pausa di 0.15 secondi (`config.INTER_TRIAL_DELAY`). Durante questa pausa l'input non viene accettato.
 
**Perché:** Senza questa pausa, un giocatore molto veloce potrebbe rispondere al trial successivo mentre sta ancora registrando visivamente il feedback del precedente, portando a risposte involontarie. La pausa dà ritmo al gioco e rende più chiaro il confine tra un trial e l'altro.
 
**Come abbiamo verificato che il core cognitivo resti invariato:** La pausa non altera le regole, il punteggio o la durata della sessione (il timer continua a scorrere normalmente durante l'inter-trial interval). È solo una restrizione dell'input, non una modifica della logica.
 