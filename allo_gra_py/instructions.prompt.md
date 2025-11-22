# Procedura csv_control

## 👤 Persona

Sei un programmatore Python con esperienza come Data analyst che usa abitualmente Python con le librerie built-in e quelle più diffuse per Data analysis.

## 🎯 Compito

Preparare una procedura Python che verifichi e corregga la coerenza della struttura interna di una serie di CSV, contenuti nella stessa cartella. La cartella iniziale, di esempio, è la sottocartella data contenuta nella stessa cartella di queste istruzioni.
Lo scopo è ottenere una copia di tutti i files originali che presenti una struttura omogenea in termini di campi e di valori dei records associati a tali campi in modo da poterli successivamente unire in un'unica tabella.

La procedura dovrà porre rimedio ad eventuali problemi riscontrati nei file CSV, quali, ad esempio:

1. la riga 1 di ciascun singolo file CSV contiene un numero di campi che non corrisponde ai records sottostanti. In questo caso i record che risultassero più corti (cioè con un numero di campi inferiore) rispetto alla prima riga devono essere integrati dei campi mancanti. 
Per capire quale dove vanno inseriti i valori vuoti bisogna capire se i valori del campo precedente e successivo a quello dove si inseriscono sono coerenti con i valori presenti nei record di lunghezza coerente con la riga 1
2. il numero di campi presenti in ogni file devono essere adattati a quelli del file CSV con il maggior numero di campi presente all'interno della cartella scelta dall'utente. Per l'ordine dei campi fare riferimento ai nomi dei campi stessi che sono sempre riportati nella riga 1 di ogni file. Riempire i valori dei campi aggiunti ai file che ne hanno di meno con valori vuoti.

Prepara il codice, i relativi tests, unitari e di integrazione, la documentazione e gli scripts necessari a creare un environment Python e un file requirements.txt all'interno della cartella che contiene questo file di istruzioni. Dividi il materiale in sottocartelle secondo la tipologia di file.

## 📚 Contesto

Una cartella, indicata dall'utente, che contiene files CSV che ci si aspetta abbiano una struttura molto simile.

## ⚠️ Vincoli

Utilizza preferibilmente librerie python built-in ed eventualmente librerie comuni per Data analysis (es. pandas).

Per i tests utilizza pytest.

I dati presenti all'interno dei files CSV non possono essere alterati.

## 📤 Formato di Output

La procedura deve produrre in output:

- il codice necessario alla verifica e la correzione delle strutture dei files CSV
- eventuali tests utili a verificare la correttezza dei risultati prodotti
- la documentazione del codice prodotto
- eventuali cartelle e files CSV utilizzati per i tests
