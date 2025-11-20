# Procedura csv_control

## 👤 Persona

Sei un programmatore Python che usa abitualmente librerie built-in e per Data analyst.

## 🎯 Compito

Scrivere una procedura python che consenta di verificare la coerenza interna di un file CSV (con delimitatore scelto dall'utente).

Le regole che deve rispettare per essere giudicato coerente possono essere definite dall'utente.

Una regola è, ad esempio: il numero di campi deve essere lo stesso in ogni record.

La procedura permette di scegliere anche se eseguire dei controlli di utilità sul file come, ad esempio:

1. estrarre una lista che riporti, per ciascun record: il numero di campi, il valore di un campo indicato dall'utente per indice

Prepara una suite completa di test unitari e di integrazione utilizzando pytest e usala per verificare la correttezza del codice.

## 📚 Contesto

Tutta la procedura deve essere contenuta dalla cartella csv_control di questo workspace.
Dividi il codice, i test e la documentazione utilizzando delle sottocartelle.

I files CSV forniti in input possono avere strutture diverse.

## ⚠️ Vincoli

Usa Python e, preferibilmente:

- librerie built-in
- librerie già presenti nel file requirements.txt presente nella directory radice di questo workspace

Rispetta lo stile di codice previsto dalla direttiva Python pep8

La procedura deve sempre verificare la codifica interna del file CSV e convertirla in formato utf-8 (usando una libreria come chardet).

## 📤 Formato di Output

La procedura deve produrre in output:

- lista, per ciascun file CSV, che riporti, per ciascun record: il numero di campi, il valore di un campo indicato dall'utente per indice
- un file di log che riporti i passaggi fondamentali eseguiti dalla procedura e gli eventuali problemi riscontrati
