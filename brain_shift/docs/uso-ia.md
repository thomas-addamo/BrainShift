# Uso dell'IA nel progetto
 
## Strumenti usati
 
- [x] **Claude (modello: Claude Sonnet 4.6)**
---
 
## Cosa abbiamo chiesto e cosa ha risposto
 
### 1. Convenzioni per i messaggi di commit Git
  
**Cosa abbiamo chiesto:** Come scrivere messaggi di commit significativi, se esistessero convenzioni standard.
 
**Cosa ci ha suggerito:** Di usare i prefissi convenzionali: `feat` per nuove funzionalità, `fix` per correggere bug, `refactor` per migliorare il codice senza cambiarne il comportamento, `docs` per la documentazione, `test` per i test, `chore` per modifiche alla struttura del progetto.
 
**Cosa abbiamo fatto:**
- [x] Accettato integralmente
 
---
 
### 2. Funzionamento di `random.Random()` e del parametro `rng`
  
**Cosa abbiamo chiesto:** Cosa fosse `rng = random.Random()` e perché non si potesse usare direttamente `import random` con `randint` dentro la funzione del generatore.
 
**Cosa ci ha suggerito:** Che `rng` è un oggetto `Random` "portatile" — funziona come il modulo `random` standard ma è un'istanza indipendente con il proprio stato interno. Passarlo come parametro permette di inizializzarlo con un seed in `main.py` e ottenere sequenze riproducibili, cosa impossibile se si chiama `random.randint` direttamente dentro il generatore (che userebbe lo stato globale del modulo).
 
**Cosa abbiamo fatto:**
- [x] Accettato integralmente
 
---
 
### 3. Posizionamento degli elementi a schermo in pygame
  
**Cosa abbiamo chiesto:** Come posizionare correttamente i vari elementi sullo schermo (carta, HUD, pulsanti, testo), con richiesta di blocchi di codice da usare come base.
 
**Cosa ci ha suggerito:** Blocchi di codice di partenza per il rendering degli elementi principali, con l'uso di `get_rect(center=...)`, `get_rect(midleft=...)`, `get_rect(midright=...)` per centrare e allineare le superfici, e la struttura generale delle funzioni di disegno.
 
**Cosa abbiamo fatto:**
- [x] Modificato adattandolo al nostro codice
 
---
 
### 4. Struttura del `GameState` e delle funzioni di gestione partita in `main.py`
  
**Cosa abbiamo chiesto:** Come gestire il moltiplicatore del gioco e come strutturare lo stato complessivo della partita in `main.py`.
 
**Cosa ci ha suggerito:** Di creare una dataclass `GameState` che raccogliesse tutti i valori mutabili della partita (score, multiplier, meter, trial corrente, timer, ecc.), e di separare la logica in funzioni dedicate come `submit_answer` per registrare una risposta e aggiornare lo stato, e `reset_and_replay` per azzerare tutto e ricominciare. Ci ha anche consigliato di tenere `score`, `multiplier` e `meter` come scalari passati alle funzioni di `scoring.py` invece di incapsularli in un oggetto separato.
 
**Cosa abbiamo fatto:**
- [x] Modificato adattandolo al nostro codice

---
 
### 5. Struttura della schermata di pausa
  
**Cosa abbiamo chiesto:** Come strutturare la schermata di pausa, in particolare come congelare correttamente il timer senza che il tempo di pausa venisse conteggiato nel tempo di gioco.
 
**Cosa ci ha suggerito:** Di usare due variabili: `pause_start` (il momento in cui inizia la pausa) e `total_pause_time` (la somma di tutte le pause). Il tempo effettivo di gioco si calcola come `time.time() - start_time - total_pause_time`. Alla ripresa si aggiorna `total_pause_time += time.time() - pause_start`.
 
**Cosa abbiamo fatto:**
- [x] Accettato integralmente
 
---
 
### 6. Consiglio generale sulla qualità del codice
  
**Cosa abbiamo chiesto:** Di leggere il nostro codice e darci consigli generali su cosa migliorare.
 
**Cosa ci ha suggerito:** Ci ha consigliato di separare più nettamente le responsabilità tra i moduli, di evitare stato globale in favore del passaggio esplicito dei parametri, e di aggiungere docstring alle funzioni principali. Ci ha anche suggerito di scrivere test aggiuntivi oltre a quelli forniti.
 
**Cosa abbiamo fatto:**
- [x] Preso solo l'idea e riscritto