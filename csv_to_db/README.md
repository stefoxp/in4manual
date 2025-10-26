# csv_to_db

Procedura Python per importare file CSV in database relazionali (SQLite, MS SQL Server, MariaDB) con validazione dati integrata.

## Caratteristiche

- **Multi-database**: Supporto per SQLite, MS SQL Server e MariaDB
- **Validazione dati**: Verifica lunghezza campi e compatibilità schema
- **Configurabile**: Mappature CSV → tabelle DB tramite YAML
- **Testato**: Unit, integration, acceptance e BDD tests
- **Dry-run mode**: Validazione senza modifiche al database

## Installazione

```powershell
# Installa dipendenze
.\env\Scripts\pip.exe install -r csv_to_db\requirements.txt
```

## Quick Start

```python
from csv_to_db.src.database.sqlite_adapter import SQLiteAdapter
from csv_to_db.src.csv_reader import CSVReader

# Leggi CSV
reader = CSVReader('data.csv', {'separator': ';'})
df = reader.read()

# Connetti a database
adapter = SQLiteAdapter()
adapter.connect('database.db')

# Inserisci dati
rows = adapter.insert_dataframe(df, 'tabella_destinazione')
print(f"Inserite {rows} righe")

adapter.close()
```

## Struttura Progetto

```sh
csv_to_db/
├── src/                    # Codice sorgente
│   ├── csv_reader.py      # Lettura CSV
│   ├── exceptions.py      # Eccezioni custom
│   └── database/          # Adapters database
├── tests/                 # Test suite
│   ├── unit/             # Unit tests
│   ├── integration/      # Integration tests
│   └── acceptance/       # Acceptance tests
└── config/               # Configurazioni
```

## Testing

```powershell
# Esegui tutti i test
.\env\Scripts\pytest csv_to_db\tests\

# Con coverage
.\env\Scripts\pytest csv_to_db\tests\ --cov=csv_to_db\src --cov-report=html
```

## Stato Implementazione

**Fase 1 (Completata)**:

- ✅ Struttura progetto
- ✅ DatabaseAdapter base e SQLiteAdapter
- ✅ CSVReader
- ✅ Unit tests completi

**Fasi Future**:

- Fase 2: DataValidator e ValidationResult
- Fase 3: CSVImporter con dry-run
- Fase 4: MS SQL Server e MariaDB adapters
- Fase 5: CLI e configurazione YAML

## Licenza

Vedi LICENSE nel progetto principale.
