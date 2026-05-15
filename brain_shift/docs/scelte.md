# Scelte implementative

---

## Scelte rilevanti

---

### Gestore degli stati e `GameState` in `main.py` invece di un modulo separato

**Cosa:** Tutta la parte che gestisce gli stati, come la dataclass `GameState`, le funzioni `start_playing`, `submit_answer`, `reset_and_replay`, `end_game` e il main loop, si trova in `main.py`. Non esiste un file `states.py` separato come diceva la struttura consigliata nella consegna.

**Perché:** Quando abbiamo iniziato a implementare il gestore degli stati ci siamo accorti che le funzioni nel main (come `submit_answer` e `end_game`) hanno bisogno di accedere sia alla logica pura (`scoring`, `generator`) sia all'interfaccia utente (`ui`). Creare un `states.py` separato avrebbe richiesto importare troppe cose avendo una logica complessa. Tenere tutto in `main.py` ci ha permesso di mantenere pulita la separazione tra i moduli puri e quelli di interfaccia grafica.

**Alternative considerate:** Un modulo `states.py` con il gestore degli stati esterno. L'abbiamo scartato perché avrebbe spostato il problema senza risolverlo.

**Conseguenze:** `main.py` è il file più lungo del progetto (~200 righe). È un compromesso accettabile perché è comunque leggibile e le sue responsabilità sono chiare. È l'unico file che conosce sia la logica sia l'interfaccia utente.

---

### `apply_answer` base: penalità di -5 con clamp a 0

**Cosa:** Nella funzione `apply_answer` (scoring base) abbiamo scelto -5 per le risposte errate, ma con un controllo che impedisce al punteggio di scendere sotto 0.

**Perché:** -5 rende il gioco più teso rispetto a nessuna penalità, senza però che il punteggio diventi negativo, il che ci sembrava frustrante e difficile da leggere nella schermata dei risultati.

**Alternative considerate:** 0 punti per le errate (nessuna penalità). Scartato perché riduce l'incentivo a ragionare prima di rispondere.

**Conseguenze:** I test in `test_scoring_base.py` verificano che la policy sia coerente (`delta_1 == delta_2`), ma non specificano il valore esatto della penalità. Il nostro clamp a 0 passa comunque quei test perché da punteggio >= 5 la penalità è sempre -5. Bisogna fare attenzione: se si parte da un punteggio basso (es. 3) la penalità effettiva è diversa da -5, e questo è un comportamento che abbiamo scelto consapevolmente ma che non emerge dai test forniti.

---

### Logica anti-streak di posizione

**Cosa:** Il generatore tiene traccia delle ultime `MAX_POSITION_STREAK = 3` posizioni. Se sono tutte uguali, forza l'altra posizione invece di scegliere casualmente.

**Perché:** Senza questo controllo, la casualità pura può produrre sequenze di 6-7 carte tutte nella stessa posizione. Questo rompe il meccanismo logico del gioco, cioè che se tutte le carte sono in alto per 30 secondi, il giocatore può rispondere in automatico senza cambiare regola in testa, che è esattamente quello che il gioco vuole impedire.

**Alternative considerate:** Alternare strettamente TOP/BOTTOM (una sì una no). Scartato perché renderebbe il pattern prevedibile: il giocatore saprebbe già dove comparirà la prossima carta e potrebbe prepararsi in anticipo.

**Conseguenze:** Le streak di lunghezza <= 3 sono permesse, quelle di lunghezza 4+ no. Il valore 3 è configurabile come costante in `generator.py`.

---

### Gestione del tempo con `time.time()` invece di `pygame.time.get_ticks()`

**Cosa:** Il timer di sessione e tutti i timestamp di feedback/inter-trial usano `time.time()` (secondi in virgola mobile dal 1970) invece di `pygame.time.get_ticks()` (millisecondi dall'avvio di pygame).

**Perché:** `time.time()` restituisce un valore assoluto, il che rende banale calcolare intervalli anche fuori dal main loop (es. `response_time = time.time() - trial_start_time`). Con `pygame.time.get_ticks()` avremmo dovuto convertire costantemente tra millisecondi e secondi, e la pausa sarebbe stata più complessa da implementare.

**Alternative considerate:** `pygame.time.get_ticks()`. Sarebbe stato più nativo ma meno leggibile nelle formule del timer e nella gestione della pausa.

**Conseguenze:** I timestamp non sono significativi al di fuori del processo corrente, ma questo non è un problema per il nostro uso. La precisione di `time.time()` è sufficiente per misurare tempi di risposta e feedback.

---

### Due timestamp separati per feedback e inter-trial interval

**Cosa:** In `GameState` ci sono due timestamp distinti: `feedback_until` (fino a quando mostrare il colore verde/rosso e l'icona) e `inter_trial_until` (fino a quando bloccare l'input). Il secondo è sempre `feedback_until + INTER_TRIAL_DELAY`.

**Perché:** Separarli permette di controllare i due comportamenti in modo indipendente nel main loop, tipo il colore della carta cambia quando scade `feedback_until`, ma il nuovo input non viene accettato finché non scade `inter_trial_until`. Se avessimo usato un solo timestamp, non avremmo potuto avere la piccola pausa "vuota" dopo che il feedback scompare ma prima che il giocatore possa rispondere.

**Alternative considerate:** Un solo timestamp con la durata totale (feedback + pausa). Scartato perché avrebbe impedito di mostrare la carta neutra per quei 150ms tra la fine del feedback e la risposta successiva.

**Conseguenze:** La logica nel main loop controlla due condizioni separate, ma è più leggibile: ogni condizione ha un nome che spiega cosa controlla.

---

### Fading con rimbalzo sugli errori consecutivi

**Cosa:** La funzione `get_instruction_opacity` in `main.py` non calcola solo l'opacità in base alle risposte corrette cumulative (come da specifica), ma aggiunge opacità extra se il giocatore sbaglia più volte di fila (`wrong_streak >= 3`). Le istruzioni "ricompaiono" parzialmente quando il giocatore è in difficoltà.

**Perché:** Ci è sembrato un completamento logico del fading graduale, cioè che se le istruzioni spariscono perché il giocatore le ha imparate, ha senso che riappaiano se dimostra di averle dimenticate.

**Alternative considerate:** Fading solo in avanti, senza rimbalzo. È la versione base della specifica. Abbiamo scelto di andare oltre perché era un'estensione naturale della logica già implementata.

**Conseguenze:** Il contatore `wrong_streak` deve essere resettato a ogni risposta corretta e incrementato a ogni sbaglio, il che aggiunge un campo in più a `GameState`. L'opacità extra è cappata a 160 per evitare che le istruzioni diventino completamente opache anche con molti errori consecutivi.

---

## Cosa non siamo riusciti a fare e perché

**Audio:** Non abbiamo implementato gli effetti sonori. Nelle ultime settimane abbiamo dato priorità alle funzionalità avanzate dello scoring e alla documentazione. `pygame.mixer` sarebbe stato il passo successivo, ma non abbiamo avuto tempo di integrarlo senza rischiare di introdurre bug nell'ultima settimana prima della consegna.

**Leaderboard locale:** Non abbiamo implementato il salvataggio dei punteggi in JSON. Anche qui, la scelta è stata di finire bene quello che avevamo piuttosto che aggiungere una funzionalità nuova all'ultimo momento.

**Asset grafici personalizzati:** Il gioco usa solo la grafica generata da pygame (`draw.rect`, `draw.line`, font di sistema). Avremmo voluto aggiungere almeno font personalizzati, ma non l'abbiamo fatto per non complicare il setup da clone pulito (font esterni richiedono che il file sia presente nel repo).