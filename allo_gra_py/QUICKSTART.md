# CSV Control - Guida Quick Start

## 🚀 Installazione Rapida

### 1. Requisiti

- Python 3.8 o superiore
- Prompt dei comandi di Windows (cmd) o shell compatibile

### 2. Setup Automatico (Raccomandato)

```batch
REM Naviga nella cartella del progetto
cd allo_gra_py

REM Esegui lo script di setup
setup_env.bat
```

Lo script eseguirà automaticamente:

- ✓ Verifica installazione Python
- ✓ Creazione ambiente virtuale
- ✓ Aggiornamento pip
- ✓ Installazione dipendenze
- ✓ Verifica installazione

### 3. Setup Manuale (Alternativa)

```batch
REM Crea ambiente virtuale
python -m venv venv
REM Attiva ambiente
call venv\Scripts\activate.bat

REM Installa dipendenze
pip install -r requirements.txt
```

## 📋 Utilizzo

```batch
REM Attiva l'ambiente virtuale se non è già attivo
call venv\Scripts\activate.bat

REM Processa i file CSV nella cartella 'data'
python src\csv_control.py data

REM I file corretti saranno in 'output/'
```

### Modo 2: Specifica Cartella Output

```batch
python src\csv_control.py data output_personalizzato
```

### Modo 3: Da Codice Python

```python
from src.csv_control import CSVController

# Inizializza
controller = CSVController("data")

# Analizza
controller.analyze_all_files()

# Genera report
print(controller.generate_report())

# Processa e salva
output_files = controller.process_and_save("output")
```

## 🧪 Testing

```batch
REM Esegui tutti i test
pytest tests/

REM Test con report dettagliato
pytest -v tests/

REM Test con copertura del codice
pytest --cov=src tests/
```

Risultato atteso: **15 test passati**

## 📊 Output

Dopo l'esecuzione, troverai:

1. **Console Output**: Report dettagliato con:
   - Numero di file analizzati
   - Record inconsistenti per file
   - Riepilogo correzioni

2. **Cartella output/**: File CSV corretti con:
   - Stesso numero di campi in tutti i file
   - Campi standardizzati
   - Dati originali preservati
   - Campi mancanti riempiti con valori vuoti

## ⚡ Esempio Pratico

```batch
REM 1. Setup iniziale
setup_env.bat

REM 2. Esegui il tool sui tuoi dati
python src\csv_control.py mia_cartella_csv

REM 3. Verifica i risultati
dir output

REM 4. Esegui i test per sicurezza
pytest tests/ -v
```

## 🎯 Cosa fa il Tool

### Input

```text
File1.csv: ID;NOME;COGNOME (3 campi)
File2.csv: ID;NOME;COGNOME;ETA;CITTA (5 campi)
File3.csv: ID;NOME;COGNOME;ETA (4 campi)
```

### Output

```text
File1.csv: ID;NOME;COGNOME;ETA;CITTA (5 campi, aggiunti ETA e CITTA vuoti)
File2.csv: ID;NOME;COGNOME;ETA;CITTA (5 campi, invariato)
File3.csv: ID;NOME;COGNOME;ETA;CITTA (5 campi, aggiunto CITTA vuoto)
```

## 🔧 Risoluzione Problemi

### "Python non trovato"

```powershell
# Verifica installazione Python
python --version

# Se non installato, scarica da python.org
```

### "Impossibile eseguire lo script batch"

```batch
REM Avvia un Prompt dei comandi nella cartella del progetto
cd \percorso\allo_gra_py

REM Esegui lo script
setup_env.bat
```

Se Windows blocca lo script (file scaricato da Internet), apri le Proprietà del file, seleziona "Sblocca" e riprova.

### "Errore di encoding"

```python
# Usa encoding specifico
controller = CSVController("data", encoding='latin-1')
```

## 📚 Documentazione Completa

Per dettagli approfonditi, vedi:

- `docs/README.md` - Documentazione completa
- `tests/test_csv_control.py` - Esempi d'uso nei test
- `src/csv_control.py` - Codice sorgente commentato

## ✅ Checklist Completamento Setup

- [ ] Python 3.8+ installato
- [ ] Ambiente virtuale creato
- [ ] Dipendenze installate
- [ ] Test eseguiti con successo (15 passati)
- [ ] Tool eseguito sui dati di esempio
- [ ] File corretti generati in `output/`

## 🎓 Prossimi Passi

1. **Test sui tuoi dati**: Copia i tuoi CSV in una cartella e esegui il tool
2. **Verifica output**: Controlla i file generati in `output/`
3. **Integrazione**: Usa i file corretti per l'analisi successiva
4. **Automazione**: Integra il tool nel tuo workflow

---

**Data di creazione**: Novembre 2025  
**Autore**: ERDIS SQL Team  
**Versione**: 1.0.0
