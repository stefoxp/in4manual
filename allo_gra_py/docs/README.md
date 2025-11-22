# CSV Control - Documentazione

## Panoramica

CSV Control è un tool Python per verificare e correggere la struttura di file CSV. È progettato per garantire che tutti i file CSV in una cartella abbiano una struttura omogenea in termini di campi e valori.

## Caratteristiche

- ✅ Analisi della struttura di file CSV
- ✅ Rilevamento di record con numero di campi inconsistente
- ✅ Correzione automatica dei record troppo corti
- ✅ Standardizzazione di tutti i file al formato con il maggior numero di campi
- ✅ Preservazione integrale dei dati originali
- ✅ Riordinamento dei campi secondo l'ordine degli headers
- ✅ Generazione di report dettagliati
- ✅ Test completi (unitari e di integrazione)

## Installazione

### Prerequisiti

- Python 3.8 o superiore
- pip

### Setup dell'ambiente

#### Windows (PowerShell)

```powershell
# Naviga nella cartella del progetto
cd c:\GitHub\erdis-sql\PowerQuery\Excel\ETL\allo_gra_py

# Crea ambiente virtuale
python -m venv venv

# Attiva l'ambiente virtuale
.\venv\Scripts\Activate.ps1

# Installa le dipendenze
pip install -r requirements.txt
```

#### Linux/Mac

```bash
# Naviga nella cartella del progetto
cd /path/to/allo_gra_py

# Crea ambiente virtuale
python3 -m venv venv

# Attiva l'ambiente virtuale
source venv/bin/activate

# Installa le dipendenze
pip install -r requirements.txt
```

## Utilizzo

### Da Riga di Comando

```powershell
# Sintassi base
python src/csv_control.py <cartella_input> [cartella_output]

# Esempio con i dati nella sottocartella 'data'
python src/csv_control.py data

# Esempio con cartella di output personalizzata
python src/csv_control.py data output_corretti
```

### Da Codice Python

```python
from src.csv_control import CSVController

# Inizializza il controller
controller = CSVController("data", delimiter=';', encoding='utf-8')

# Analizza tutti i file
analyses = controller.analyze_all_files()

# Genera un report
report = controller.generate_report()
print(report)

# Processa e salva i file corretti
output_files = controller.process_and_save("output")

# Mostra i file generati
for original, corrected in output_files.items():
    print(f"{original} -> {corrected}")
```

## Funzionamento

### 1. Analisi

Il tool analizza ogni file CSV nella cartella specificata e rileva:

- Numero di campi nell'header
- Lista dei campi
- Numero totale di record
- Record con numero di campi diverso dall'header

### 2. Identificazione Headers Master

Identifica il file con il maggior numero di campi e utilizza i suoi headers come "master" per standardizzare tutti gli altri file.

### 3. Correzione

Per ogni file:

- Legge gli headers originali
- Per ogni record:
  - Mappa i valori ai campi corrispondenti negli headers master
  - Aggiunge campi vuoti per i campi mancanti
  - Riordina i valori secondo l'ordine degli headers master
- Salva il file corretto

### 4. Output

Genera file CSV corretti con:

- Stesso numero di campi in tutti i file
- Stessi nomi di campi (headers master)
- Stesso ordine dei campi
- Valori originali preservati
- Campi vuoti per i campi mancanti

## Esempi

### Scenario 1: Record più corti dell'header

**Input (file1.csv):**

```csv
ID;NOME;COGNOME;ETA
1;Mario;Rossi;30
2;Luca
3;Anna;Verdi;25
```

**Output (file1.csv corretto):**

```csv
ID;NOME;COGNOME;ETA
1;Mario;Rossi;30
2;Luca;;
3;Anna;Verdi;25
```

### Scenario 2: File con numero di campi diverso

**Input:**

file1.csv:

```csv
ID;NOME;COGNOME
1;Mario;Rossi
```

file2.csv:

```csv
ID;NOME;COGNOME;ETA;CITTA
2;Anna;Verdi;30;Roma
```

**Output:**

file1.csv (corretto):

```csv
ID;NOME;COGNOME;ETA;CITTA
1;Mario;Rossi;;
```

file2.csv (corretto):

```csv
ID;NOME;COGNOME;ETA;CITTA
2;Anna;Verdi;30;Roma
```

### Scenario 3: Campi in ordine diverso

**Input:**

file1.csv:

```csv
NOME;ID;COGNOME
Mario;1;Rossi
```

file2.csv:

```csv
ID;NOME;COGNOME;ETA
2;Anna;Verdi;30
```

**Output:**

file1.csv (corretto):

```csv
ID;NOME;COGNOME;ETA
1;Mario;Rossi;
```

file2.csv (corretto):

```csv
ID;NOME;COGNOME;ETA
2;Anna;Verdi;30
```

## Testing

### Esecuzione dei Test

```powershell
# Esegui tutti i test
pytest tests/

# Esegui i test con output dettagliato
pytest -v tests/

# Esegui i test con copertura del codice
pytest --cov=src tests/

# Esegui un singolo file di test
pytest tests/test_csv_control.py

# Esegui una singola classe di test
pytest tests/test_csv_control.py::TestCSVController

# Esegui un singolo test
pytest tests/test_csv_control.py::TestCSVController::test_analyze_csv_file
```

### Struttura dei Test

- `tests/test_csv_control.py`: Test unitari e di integrazione
  - `TestCSVAnalysis`: Test per la classe CSVAnalysis
  - `TestCSVController`: Test per la classe CSVController
  - `TestIntegration`: Test end-to-end completi

## Struttura del Progetto

```text
allo_gra_py/
├── data/                          # File CSV di input (esempio)
│   ├── gra_102_2024-25_allo_def_ridotto_errato.csv
│   ├── gra_102_2025-26_allo_def_ridotto.csv
│   └── gra_104_2023-24_allo_def_ridotto.csv
├── src/                           # Codice sorgente
│   ├── __init__.py
│   └── csv_control.py             # Modulo principale
├── tests/                         # Test
│   ├── __init__.py
│   ├── test_csv_control.py        # Test unitari e di integrazione
│   └── data/                      # Dati di test
│       ├── test_short.csv
│       ├── test_medium.csv
│       └── test_long.csv
├── output/                        # File CSV corretti (generati)
├── docs/                          # Documentazione
│   └── README.md                  # Questo file
├── requirements.txt               # Dipendenze Python
├── setup_env.ps1                  # Script setup ambiente (Windows)
└── instructions.prompt.md         # Istruzioni originali
```

## API Reference

### Classe `CSVAnalysis`

Dataclass per contenere i risultati dell'analisi di un file CSV.

**Attributi:**

- `filename` (str): Nome del file
- `num_fields` (int): Numero di campi nell'header
- `headers` (List[str]): Lista degli headers
- `num_records` (int): Numero totale di record
- `inconsistent_records` (List[Tuple[int, int]]): Lista di record inconsistenti [(riga, num_campi), ...]

### Classe `CSVController`

Classe principale per il controllo e la correzione di file CSV.

#### Metodi

**`__init__(folder_path: str, delimiter: str = ';', encoding: str = 'utf-8')`**

Inizializza il controller.

**`get_csv_files() -> List[Path]`**

Restituisce la lista di tutti i file CSV nella cartella.

**`analyze_csv_file(filepath: Path) -> CSVAnalysis`**

Analizza un singolo file CSV.

**`analyze_all_files() -> List[CSVAnalysis]`**

Analizza tutti i file CSV nella cartella.

**`get_master_headers() -> List[str]`**

Restituisce gli headers del file con il maggior numero di campi.

**`fix_record_length(row: List[str], expected_headers: List[str], current_headers: List[str]) -> List[str]`**

Corregge la lunghezza di un record aggiungendo campi mancanti.

**`process_and_save(output_folder: Optional[str] = None) -> Dict[str, str]`**

Processa tutti i file CSV e salva le versioni corrette.

**`generate_report() -> str`**

Genera un report testuale dell'analisi.

## Risoluzione dei Problemi

### Errore: "Nessun file CSV trovato"

Verifica che:

1. Il percorso della cartella sia corretto
2. I file abbiano estensione `.csv`
3. Hai i permessi di lettura sulla cartella

### Errore di encoding

Se i file CSV usano una codifica diversa da UTF-8, specifica l'encoding:

```python
controller = CSVController("data", encoding='latin-1')
```

### I record corretti non sono come previsto

Verifica:

1. Il delimitatore sia corretto (default: `;`)
2. Gli headers nel file originale siano corretti
3. Non ci siano caratteri speciali non gestiti

## Limitazioni

- Il tool presuppone che l'header sia sempre alla riga 1
- I campi mancanti vengono riempiti con stringhe vuote
- L'ordine dei campi viene determinato dal file con più campi
- Non gestisce CSV con delimitatori multipli o irregolari

## Contribuire

Per contribuire al progetto:

1. Esegui i test esistenti
2. Aggiungi test per nuove funzionalità
3. Mantieni la compatibilità con Python 3.8+
4. Documenta le modifiche

## Licenza

Questo progetto è sviluppato per uso interno di ERDIS (Ente Regionale per il Diritto allo Studio - Marche).

## Autori

ERDIS SQL Team - Novembre 2025

## Contatti

Per domande o supporto, contattare il team informatico ERDIS.
