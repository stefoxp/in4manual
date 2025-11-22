# CSV Control

Tool Python per verificare e correggere la struttura di file CSV.

## 🚀 Quick Start (30 secondi)

```powershell
# 1. Setup automatico
.\setup_env.ps1

# 2. Esegui il tool
python src/csv_control.py data

# 3. Verifica i risultati
Get-ChildItem output
```

**Fatto!** I tuoi file CSV corretti sono in `output/`

## 📋 Installazione Manuale

```powershell
# Crea e attiva ambiente virtuale
python -m venv venv
.\venv\Scripts\Activate.ps1

# Installa dipendenze
pip install -r requirements.txt
```

## 💡 Esempi di Utilizzo

### Da Riga di Comando

```powershell
# Processa i file CSV nella cartella 'data'
python src/csv_control.py data

# Specifica cartella di output personalizzata
python src/csv_control.py data output_personalizzato
```

### Da Codice Python

```python
from src.csv_control import CSVController

# Analizza e correggi i file
controller = CSVController("data")
controller.analyze_all_files()
controller.process_and_save("output")
```

### Esempio Completo

```powershell
# Esegui l'esempio semplificato
python simple_example.py
```

## ✨ Funzionalità

- ✅ **Analisi automatica**: Rileva inconsistenze nei file CSV
- ✅ **Correzione intelligente**: Riempie campi mancanti preservando i dati
- ✅ **Standardizzazione**: Uniforma tutti i file allo stesso formato
- ✅ **Report dettagliati**: Statistiche complete dell'analisi
- ✅ **100% Testato**: 15 test automatici con copertura completa

## 📊 Risultati Test

```text
pytest tests/ -v

15 passed in 0.17s ✓
```

## 📁 Struttura Progetto

```text
allo_gra_py/
├── data/                   # File CSV di input (esempio fornito)
├── src/                    # Codice sorgente
│   ├── csv_control.py      # Modulo principale
│   └── __init__.py
├── tests/                  # Test suite (15 test)
│   ├── test_csv_control.py
│   └── data/               # Dati di test
├── output/                 # File CSV corretti (generati automaticamente)
├── docs/                   # Documentazione completa
│   └── README.md
├── setup_env.ps1           # Script setup automatico (Windows)
├── simple_example.py       # Esempio d'uso semplice
├── examples.py             # Esempi avanzati
├── requirements.txt        # Dipendenze Python
├── QUICKSTART.md          # Guida rapida dettagliata
└── IMPLEMENTATION_SUMMARY.md  # Riepilogo implementazione
```

## 📚 Documentazione

- **[QUICKSTART.md](QUICKSTART.md)** - Guida rapida con esempi
- **[docs/README.md](docs/README.md)** - Documentazione completa (400+ righe)
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Dettagli implementazione
- **[simple_example.py](simple_example.py)** - Esempio pratico commentato

## 🧪 Testing

```powershell
# Esegui tutti i test
pytest tests/

# Test con output dettagliato
pytest tests/ -v

# Test con copertura del codice
pytest --cov=src tests/
```

## 🎯 Caso d'Uso

### Problema

Hai 3 file CSV:

- File1: 3 campi, alcuni record più corti
- File2: 5 campi, tutti OK
- File3: 4 campi, tutti OK

### Soluzione

```powershell
python src/csv_control.py cartella_csv
```

### Risultato

Tutti i file avranno 5 campi (dal file più lungo), con:

- Dati originali preservati
- Campi mancanti riempiti con valori vuoti
- Campi riordinati nell'ordine corretto
- Struttura omogenea per analisi successive

## ⚙️ Configurazione

Il tool supporta:

- **Delimitatore personalizzato**: `CSVController("data", delimiter=',')`
- **Encoding personalizzato**: `CSVController("data", encoding='latin-1')`
- **Output personalizzato**: `controller.process_and_save("mia_cartella")`

## 🔧 Risoluzione Problemi

### "Python non trovato"

Installa Python 3.8+ da [python.org](https://www.python.org)

### "Impossibile eseguire script PowerShell"

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Problemi di encoding

```python
controller = CSVController("data", encoding='latin-1')  # o 'cp1252'
```

## 📦 Dipendenze

Solo librerie Python standard + testing:

- **csv** (built-in)
- **pathlib** (built-in)
- **dataclasses** (built-in)
- **pytest** (testing)
- **pytest-cov** (coverage)

## 📄 Licenza

ERDIS (Ente Regionale per il Diritto allo Studio - Marche) - 2025

## 👥 Autori

ERDIS SQL Team

---

**Versione**: 1.0.0  
**Data**: Novembre 2025  
**Status**: ✅ Pronto per uso in produzione
