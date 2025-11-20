# Documentazione per la procedura csv_control

## Scopo

La procedura `csv_control` fornisce un insieme di strumenti per validare e analizzare file CSV. È progettata per essere flessibile, consentendo agli utenti di definire le proprie regole di validazione e di estrarre informazioni utili dai record.

## Architettura

Il progetto è strutturato come segue:

- `src/`: Contiene il codice sorgente principale della libreria.
  - `csv_validator.py`: Il modulo principale con le funzioni di validazione ed estrazione.
- `tests/`: Contiene la suite di test.
  - `test_csv_validator.py`: Test unitari per le funzioni in `csv_validator.py`.
  - `data/`: Contiene file CSV di esempio utilizzati per i test.
- `docs/`: Contiene la documentazione del progetto.
- `csv_validator.log`: File di log generato durante l'esecuzione.

## Funzionalità Principali

### `validate_csv(file_path, delimiter, rules)`

Questa è la funzione principale che orchestra il processo di validazione.

- **Argomenti:**
  - `file_path` (str): Il percorso del file CSV da validare.
  - `delimiter` (str): Il delimitatore di campo del CSV (default: ';').
  - `rules` (list): Una lista di regole di validazione da applicare. Attualmente, l'unica regola implementata è `'check_field_count_consistency'`.

- **Restituisce:**
  - `bool`: `True` se il file supera tutti i controlli di validazione, `False` altrimenti.

### `extract_record_info(file_path, delimiter, field_index)`

Estrae informazioni da ogni record del file CSV.

- **Argomenti:**
  - `file_path` (str): Il percorso del file CSV.
  - `delimiter` (str): Il delimitatore di campo.
  - `field_index` (int): L'indice del campo da cui estrarre il valore.

- **Restituisce:**
  - `list`: Una lista di dizionari. Ogni dizionario rappresenta un record e contiene:
    - `line_number`: Il numero di riga.
    - `field_count`: Il numero di campi nel record.
    - `field_value`: Il valore del campo specificato da `field_index`.

### `check_field_count_consistency(reader, file_path)`

Controlla che ogni riga nel file CSV abbia lo stesso numero di campi della prima riga.

### `detect_encoding(file_path)`

Rileva la codifica del file. **Nota:** L'implementazione attuale è un placeholder e restituisce sempre `'utf-8'`. Per un uso in produzione, si consiglia di integrarla con una libreria come `chardet`.

## Logging

La procedura registra i passaggi principali e gli errori in un file chiamato `csv_validator.log` nella directory principale di `csv_control`.

## Come Eseguire i Test

Per eseguire la suite di test, assicurarsi di avere `pytest` installato (`pip install pytest`) ed eseguire il seguente comando dalla directory radice del progetto (`in4manual`):

```bash
pytest csv_control/tests/
```

## Esempio di Utilizzo

```python
from csv_control.src.csv_validator import validate_csv, extract_record_info

file_da_controllare = 'percorso/al/tuo/file.csv'
delimitatore_csv = ';'

# Validare il file
is_valido = validate_csv(file_da_controllare, delimiter=delimitatore_csv)
print(f"Il file è {'valido' if is_valido else 'non valido'}.")

# Estrarre informazioni
indice_campo = 2 # Esempio: estrae il valore dal terzo campo
info_record = extract_record_info(file_da_controllare, delimiter=delimitatore_csv, field_index=indice_campo)

for record in info_record:
    print(f"Riga {record['line_number']}: {record['field_count']} campi, Valore campo[{indice_campo}]: {record['field_value']}")

```
