# Istruzioni per la Procedura CSV to Database

## Panoramica del Progetto

Creare una procedura Python modulare e testabile per importare dati da file CSV verso database relazionali (SQLite, Microsoft SQL Server, MariaDB). La procedura deve validare i dati prima dell'importazione e supportare l'aggiunta di nuove tipologie di file CSV in futuro.

## Obiettivi Principali

1. **Import CSV generico**: Leggere file CSV con diverse strutture e formati
2. **Validazione dati**: Verificare la compatibilità della lunghezza dei campi con lo schema del database
3. **Multi-database**: Supportare SQLite, MS SQL Server e MariaDB
4. **Estensibilità**: Permettere l'aggiunta di nuove tipologie di CSV tramite configurazione
5. **Testing completo**: Unit tests, integration tests, acceptance tests e BDD tests

## Architettura della Soluzione

### Struttura delle Cartelle

```
csv_to_db/
├── instructions.prompt.md              # Questo file
├── README.md                           # Documentazione utente
├── requirements.txt                    # Dipendenze aggiuntive
├── config/                             # Configurazioni
│   ├── __init__.py
│   ├── database_config.py             # Configurazioni database
│   └── csv_mappings.yaml              # Mappature CSV -> tabelle DB
├── src/                                # Codice sorgente
│   ├── __init__.py
│   ├── csv_reader.py                  # Lettura e parsing CSV
│   ├── validator.py                   # Validazione dati
│   ├── database/                      # Modulo database
│   │   ├── __init__.py
│   │   ├── base.py                    # Interfaccia base
│   │   ├── sqlite_adapter.py          # Adapter SQLite
│   │   ├── mssql_adapter.py           # Adapter MS SQL Server
│   │   └── mariadb_adapter.py         # Adapter MariaDB
│   ├── importer.py                    # Orchestrazione import
│   └── utils.py                       # Utility functions
├── tests/                              # Test suite
│   ├── __init__.py
│   ├── unit/                          # Unit tests
│   │   ├── __init__.py
│   │   ├── test_csv_reader.py
│   │   ├── test_validator.py
│   │   └── test_database_adapters.py
│   ├── integration/                   # Integration tests
│   │   ├── __init__.py
│   │   ├── test_csv_to_sqlite.py
│   │   ├── test_csv_to_mssql.py
│   │   └── test_csv_to_mariadb.py
│   ├── acceptance/                    # Acceptance tests
│   │   ├── __init__.py
│   │   └── test_full_import_workflow.py
│   └── bdd/                           # BDD tests (Behave)
│       ├── features/
│       │   ├── csv_import.feature
│       │   └── field_validation.feature
│       ├── steps/
│       │   ├── __init__.py
│       │   ├── csv_steps.py
│       │   └── database_steps.py
│       └── environment.py
├── data/                               # File di test
│   ├── sample_csv/
│   │   ├── assegnazioni.csv
│   │   └── consumazioni.csv
│   └── test_databases/
│       └── test.db
└── main.py                            # Entry point CLI

```

## Specifiche Tecniche Dettagliate

### 1. Gestione CSV (csv_reader.py)

#### Requisiti:
- Supportare separatori personalizzabili (`;`, `,`, `\t`)
- Gestire encoding multipli (UTF-8, Windows-1252, Latin-1)
- Leggere metadata dal file CSV (numero colonne, tipi dati rilevati)
- Gestire header con/senza intestazioni

#### Funzioni principali:
```python
class CSVReader:
    def __init__(self, file_path: str, config: dict):
        """Inizializza reader con path e configurazione"""
        
    def read(self) -> pd.DataFrame:
        """Legge CSV e restituisce DataFrame"""
        
    def get_metadata(self) -> dict:
        """Restituisce metadata del CSV (colonne, tipi, righe)"""
        
    def validate_structure(self, expected_columns: list) -> bool:
        """Verifica che le colonne attese siano presenti"""
```

#### Unit Tests da implementare:
- `test_read_csv_with_semicolon_separator()`
- `test_read_csv_with_comma_separator()`
- `test_read_csv_with_different_encodings()`
- `test_get_metadata_returns_correct_info()`
- `test_validate_structure_with_valid_columns()`
- `test_validate_structure_with_missing_columns()`
- `test_handle_empty_csv_file()`
- `test_handle_malformed_csv()`

### 2. Validazione Dati (validator.py)

#### Requisiti:
- Verificare lunghezza campi rispetto allo schema DB
- Validare tipi di dati (numeri, date, stringhe)
- Gestire valori NULL/empty secondo regole DB
- Generare report dettagliato degli errori

#### Funzioni principali:
```python
class DataValidator:
    def __init__(self, schema: dict):
        """Inizializza con schema database"""
        
    def validate_field_lengths(self, df: pd.DataFrame) -> ValidationResult:
        """Valida lunghezza di tutti i campi"""
        
    def validate_data_types(self, df: pd.DataFrame) -> ValidationResult:
        """Valida tipi di dati"""
        
    def validate_constraints(self, df: pd.DataFrame) -> ValidationResult:
        """Valida vincoli (NOT NULL, UNIQUE, etc.)"""
        
    def generate_report(self, results: list[ValidationResult]) -> str:
        """Genera report testuale delle validazioni"""

class ValidationResult:
    is_valid: bool
    errors: list[ValidationError]
    warnings: list[ValidationWarning]
```

#### Unit Tests da implementare:
- `test_validate_field_length_within_limit()`
- `test_validate_field_length_exceeds_limit()`
- `test_validate_numeric_fields()`
- `test_validate_date_fields()`
- `test_validate_not_null_constraints()`
- `test_generate_report_with_errors()`
- `test_generate_report_with_warnings()`
- `test_multiple_validation_errors_per_row()`

### 3. Database Adapters (database/)

#### Pattern: Strategy/Adapter
Ogni database ha un adapter che implementa l'interfaccia comune.

#### base.py - Interfaccia Base:
```python
from abc import ABC, abstractmethod

class DatabaseAdapter(ABC):
    @abstractmethod
    def connect(self, connection_string: str) -> None:
        """Stabilisce connessione al database"""
        
    @abstractmethod
    def get_table_schema(self, table_name: str) -> dict:
        """Recupera schema della tabella (colonne, tipi, lunghezze)"""
        
    @abstractmethod
    def insert_dataframe(self, df: pd.DataFrame, table_name: str, 
                        if_exists: str = 'append') -> int:
        """Inserisce DataFrame nella tabella"""
        
    @abstractmethod
    def execute_query(self, query: str) -> pd.DataFrame:
        """Esegue query SELECT"""
        
    @abstractmethod
    def close(self) -> None:
        """Chiude connessione"""
```

#### sqlite_adapter.py:
```python
import sqlite3

class SQLiteAdapter(DatabaseAdapter):
    def __init__(self):
        self.connection = None
        
    def connect(self, connection_string: str) -> None:
        """Connessione a SQLite database"""
        self.connection = sqlite3.connect(connection_string)
        
    def get_table_schema(self, table_name: str) -> dict:
        """Usa PRAGMA table_info per recuperare schema"""
        # Implementazione specifica SQLite
```

#### mssql_adapter.py:
```python
import pyodbc

class MSSQLAdapter(DatabaseAdapter):
    def __init__(self):
        self.connection = None
        
    def connect(self, connection_string: str) -> None:
        """Connessione a MS SQL Server"""
        self.connection = pyodbc.connect(connection_string)
        
    def get_table_schema(self, table_name: str) -> dict:
        """Query INFORMATION_SCHEMA per schema"""
        # Implementazione specifica MS SQL Server
```

#### mariadb_adapter.py:
```python
import mysql.connector

class MariaDBAdapter(DatabaseAdapter):
    def __init__(self):
        self.connection = None
        
    def connect(self, connection_string: str) -> None:
        """Connessione a MariaDB"""
        # Parse connection string e usa mysql.connector
        
    def get_table_schema(self, table_name: str) -> dict:
        """Query INFORMATION_SCHEMA per schema"""
        # Implementazione specifica MariaDB
```

#### Unit Tests da implementare (per ogni adapter):
- `test_connect_success()`
- `test_connect_failure_invalid_credentials()`
- `test_get_table_schema_existing_table()`
- `test_get_table_schema_nonexistent_table()`
- `test_insert_dataframe_success()`
- `test_insert_dataframe_with_duplicates()`
- `test_execute_query_returns_dataframe()`
- `test_close_connection()`

### 4. Orchestrazione Import (importer.py)

#### Requisiti:
- Coordinare tutte le fasi: lettura CSV → validazione → import DB
- Gestire transazioni (rollback in caso di errore)
- Logging dettagliato di ogni operazione
- Supportare modalità "dry-run" (validazione senza import)

#### Funzioni principali:
```python
class CSVImporter:
    def __init__(self, db_adapter: DatabaseAdapter, config: dict):
        """Inizializza con adapter e configurazione"""
        
    def import_csv(self, csv_path: str, table_name: str, 
                   dry_run: bool = False) -> ImportResult:
        """
        Pipeline completa:
        1. Legge CSV
        2. Valida dati
        3. Inserisce in DB (se non dry_run)
        4. Restituisce risultato
        """
        
    def import_batch(self, csv_files: list[str], 
                    mapping: dict) -> list[ImportResult]:
        """Importa multipli CSV con mappatura custom"""

class ImportResult:
    success: bool
    rows_processed: int
    rows_inserted: int
    validation_errors: list[ValidationError]
    duration: float
    message: str
```

#### Unit Tests da implementare:
- `test_import_csv_success()`
- `test_import_csv_validation_failure()`
- `test_import_csv_dry_run_mode()`
- `test_import_batch_multiple_files()`
- `test_rollback_on_error()`
- `test_logging_output()`

### 5. Configurazione (config/)

#### csv_mappings.yaml:
```yaml
csv_types:
  assegnazioni:
    table_name: "assegnazioni"
    separator: ";"
    encoding: "utf-8"
    columns:
      - csv_name: "ASSE. DATA_ING"
        db_name: "data_ingresso"
        type: "date"
        required: true
      - csv_name: "ASSE. DATA_UN"
        db_name: "data_uscita"
        type: "date"
        required: false
    # ... altre colonne
    
  consumazioni:
    table_name: "consumazioni"
    separator: ";"
    encoding: "utf-8"
    columns:
      # ... definizione colonne
```

#### database_config.py:
```python
from enum import Enum
from dataclasses import dataclass

class DatabaseType(Enum):
    SQLITE = "sqlite"
    MSSQL = "mssql"
    MARIADB = "mariadb"

@dataclass
class DatabaseConfig:
    db_type: DatabaseType
    connection_string: str
    timeout: int = 30
    
    @classmethod
    def from_dict(cls, config: dict):
        """Factory method da dizionario"""
```

### 6. Entry Point CLI (main.py)

#### Funzionalità:
- Accettare parametri da linea di comando
- Supportare file singoli o batch
- Modalità interattiva vs batch
- Output formattato (JSON, testo, CSV)

```python
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(
        description="Importa file CSV in database relazionali"
    )
    parser.add_argument('csv_file', help='Path al file CSV')
    parser.add_argument('--db-type', choices=['sqlite', 'mssql', 'mariadb'],
                       required=True, help='Tipo di database')
    parser.add_argument('--connection-string', required=True,
                       help='Stringa di connessione al database')
    parser.add_argument('--table', required=True,
                       help='Nome tabella destinazione')
    parser.add_argument('--csv-type', help='Tipo CSV (da mappings.yaml)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Esegue solo validazione senza import')
    parser.add_argument('--output-format', choices=['text', 'json', 'csv'],
                       default='text', help='Formato output risultati')
    
    args = parser.parse_args()
    
    # Implementazione import
    # ...

if __name__ == "__main__":
    main()
```

## Testing Strategy

### Unit Tests (tests/unit/)

**Obiettivo**: Testare ogni funzione/metodo in isolamento con mock.

**Framework**: pytest con pytest-mock

**Copertura target**: > 90%

**Convenzioni**:
- Un file di test per ogni modulo sorgente
- Nomenclatura: `test_<nome_funzione>_<scenario>()`
- Usare fixtures per setup/teardown
- Mock per dipendenze esterne (DB, filesystem)

**Esempio test_csv_reader.py**:
```python
import pytest
from unittest.mock import Mock, patch
from src.csv_reader import CSVReader

@pytest.fixture
def mock_csv_content():
    return "col1;col2;col3\nval1;val2;val3\n"

def test_read_returns_dataframe(mock_csv_content):
    """Test che read() restituisce un DataFrame valido"""
    # Arrange
    with patch('builtins.open', mock_open(read_data=mock_csv_content)):
        reader = CSVReader('test.csv', {'separator': ';'})
        
        # Act
        df = reader.read()
        
        # Assert
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 1
        assert list(df.columns) == ['col1', 'col2', 'col3']
```

### Integration Tests (tests/integration/)

**Obiettivo**: Testare integrazione tra componenti reali (CSV + DB).

**Requisiti**:
- Database di test reali (SQLite in-memory per velocità)
- File CSV di test con dati noti
- Verificare l'intera pipeline

**Esempio test_csv_to_sqlite.py**:
```python
import pytest
import tempfile
from src.database.sqlite_adapter import SQLiteAdapter
from src.importer import CSVImporter

@pytest.fixture
def test_database():
    """Crea database SQLite temporaneo con schema"""
    with tempfile.NamedTemporaryFile(suffix='.db') as tmp:
        conn = sqlite3.connect(tmp.name)
        conn.execute("""
            CREATE TABLE test_table (
                id INTEGER PRIMARY KEY,
                nome VARCHAR(50),
                cognome VARCHAR(50),
                data_nascita DATE
            )
        """)
        conn.commit()
        yield tmp.name
        
def test_import_valid_csv_to_sqlite(test_database):
    """Test import completo di CSV valido in SQLite"""
    # Arrange
    adapter = SQLiteAdapter()
    adapter.connect(test_database)
    importer = CSVImporter(adapter, {})
    
    # Act
    result = importer.import_csv('data/sample_csv/test.csv', 'test_table')
    
    # Assert
    assert result.success
    assert result.rows_inserted == 3  # Assumendo 3 righe nel CSV
    
    # Verifica dati in DB
    df = adapter.execute_query("SELECT * FROM test_table")
    assert len(df) == 3
```

### Acceptance Tests (tests/acceptance/)

**Obiettivo**: Testare scenari end-to-end dal punto di vista utente.

**Caratteristiche**:
- Testare casi d'uso reali completi
- Includere scenari di successo e fallimento
- Verificare comportamento complessivo del sistema

**Esempio test_full_import_workflow.py**:
```python
def test_complete_import_workflow_with_validation():
    """
    Scenario: Utente importa CSV con alcuni errori di validazione
    Given: Un file CSV con 100 righe, 5 delle quali hanno campi troppo lunghi
    When: L'utente esegue l'import con validazione abilitata
    Then: 
        - Il sistema rileva i 5 errori
        - Genera un report dettagliato
        - Non inserisce nessuna riga (transazione atomica)
        - Restituisce codice errore appropriato
    """
    # Implementazione test
```

### BDD Tests (tests/bdd/)

**Obiettivo**: Definire comportamento in linguaggio naturale (Gherkin).

**Framework**: Behave

**Struttura feature files**:

**csv_import.feature**:
```gherkin
Feature: Import CSV in database
  Come utente del sistema
  Voglio importare file CSV in tabelle database
  Per popolare il database con dati da fonti esterne

  Background:
    Given un database SQLite di test è disponibile
    And la tabella "assegnazioni" esiste con lo schema corretto

  Scenario: Import di CSV valido
    Given un file CSV "assegnazioni.csv" con 10 righe valide
    When eseguo l'import verso la tabella "assegnazioni"
    Then l'import ha successo
    And 10 righe sono state inserite nella tabella
    And nessun errore di validazione è stato generato

  Scenario: Import con errori di validazione lunghezza campo
    Given un file CSV "assegnazioni_invalid.csv" con:
      | righe_valide | righe_campo_troppo_lungo |
      | 8            | 2                        |
    When eseguo l'import verso la tabella "assegnazioni"
    Then l'import fallisce
    And 0 righe sono state inserite nella tabella
    And il report contiene 2 errori di tipo "field_length_exceeded"
    And il report specifica le righe con errori

  Scenario: Dry-run validazione senza import
    Given un file CSV "assegnazioni.csv" con 10 righe valide
    When eseguo l'import in modalità dry-run
    Then la validazione ha successo
    And 0 righe sono state inserite nella tabella
    And il report indica che sarebbero state importate 10 righe
```

**field_validation.feature**:
```gherkin
Feature: Validazione campi CSV
  Come sistema
  Voglio validare i campi del CSV prima dell'import
  Per garantire integrità dei dati nel database

  Scenario Outline: Validazione lunghezza campo VARCHAR
    Given una colonna di database definita come VARCHAR(<max_length>)
    And un valore CSV di lunghezza <value_length>
    When eseguo la validazione
    Then il risultato è <result>

    Examples:
      | max_length | value_length | result  |
      | 50         | 30           | valid   |
      | 50         | 50           | valid   |
      | 50         | 51           | invalid |
      | 50         | 100          | invalid |

  Scenario: Validazione campo obbligatorio NULL
    Given una colonna definita come NOT NULL
    And un valore CSV vuoto o NULL
    When eseguo la validazione
    Then il risultato è "invalid"
    And l'errore è di tipo "null_constraint_violation"
```

**Steps implementation (steps/csv_steps.py)**:
```python
from behave import given, when, then
import tempfile
import pandas as pd

@given('un file CSV "{filename}" con {num_rows:d} righe valide')
def step_create_valid_csv(context, filename, num_rows):
    # Crea CSV temporaneo con dati validi
    context.csv_path = tempfile.mktemp(suffix='.csv')
    # ... genera dati
    
@when('eseguo l\'import verso la tabella "{table_name}"')
def step_execute_import(context, table_name):
    context.result = context.importer.import_csv(
        context.csv_path, 
        table_name
    )
    
@then('l\'import ha successo')
def step_verify_success(context):
    assert context.result.success
    
@then('{num_rows:d} righe sono state inserite nella tabella')
def step_verify_rows_inserted(context, num_rows):
    assert context.result.rows_inserted == num_rows
```

## Dipendenze Python

### requirements.txt aggiuntivo per csv_to_db:
```txt
# Database drivers
pyodbc>=5.0.0              # MS SQL Server
mysql-connector-python>=8.2.0  # MariaDB
SQLAlchemy>=2.0.0          # ORM opzionale per abstraction

# Testing
pytest>=8.1.0
pytest-cov>=4.1.0          # Coverage reports
pytest-mock>=3.12.0        # Mocking
behave>=1.2.6              # BDD framework
coverage>=7.4.0            # Coverage analysis

# Data validation
pydantic>=2.5.0            # Schema validation (opzionale)
cerberus>=1.3.5            # Data validation (alternativa)

# Configuration
PyYAML>=6.0.1              # YAML parsing
python-dotenv>=1.0.0       # Environment variables

# Logging
loguru>=0.7.2              # Enhanced logging (opzionale)

# Già presenti nel progetto principale
pandas>=2.2.1
numpy>=1.26.4
```

## Convenzioni di Codifica

### Stile Codice:
- **PEP 8** compliance (verificare con flake8/black)
- **Type hints** per tutte le funzioni pubbliche
- **Docstrings** Google style per classi e funzioni
- **Nomi variabili** italiani per logica di dominio (coerenza con progetto)

### Esempio funzione documentata:
```python
def validate_field_lengths(
    df: pd.DataFrame, 
    schema: dict[str, int]
) -> ValidationResult:
    """
    Valida che tutti i campi rispettino le lunghezze massime dello schema.
    
    Args:
        df: DataFrame pandas contenente i dati CSV
        schema: Dizionario con mapping colonna -> lunghezza_massima
        
    Returns:
        ValidationResult con esito validazione ed eventuali errori
        
    Raises:
        ValueError: Se schema contiene colonne non presenti in df
        
    Example:
        >>> schema = {'nome': 50, 'cognome': 50}
        >>> df = pd.DataFrame({'nome': ['Mario'], 'cognome': ['Rossi']})
        >>> result = validate_field_lengths(df, schema)
        >>> result.is_valid
        True
    """
    # Implementazione
```

### Gestione Errori:
- Usare eccezioni custom per errori di dominio
- Logging strutturato per debugging
- Non catturare eccezioni generiche senza re-raise

```python
# csv_to_db/src/exceptions.py
class CSVImportError(Exception):
    """Errore base per import CSV"""
    pass

class ValidationError(CSVImportError):
    """Errore di validazione dati"""
    pass

class DatabaseConnectionError(CSVImportError):
    """Errore connessione database"""
    pass

class SchemaCompatibilityError(CSVImportError):
    """Errore compatibilità schema CSV-DB"""
    pass
```

## Logging Strategy

### Configurazione logging:
```python
import logging
from pathlib import Path

def setup_logging(log_level: str = "INFO"):
    """Configura logging per l'applicazione"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / "csv_import.log"),
            logging.StreamHandler()
        ]
    )
```

### Log events da tracciare:
- Inizio/fine import CSV
- Numero righe lette/validate/inserite
- Errori di validazione (con dettagli riga/colonna)
- Errori database (con query/parametri)
- Tempo di esecuzione per ogni fase

## Metriche di Qualità

### Obiettivi:
- **Test Coverage**: > 90% per unit tests
- **Integration Coverage**: Scenari principali coperti
- **BDD Coverage**: Casi d'uso utente documentati e testati
- **Performance**: Import di 10.000 righe in < 5 secondi (SQLite)
- **Maintainability Index**: > 70 (verificare con radon)

### Comandi verifica qualità:
```powershell
# Coverage report
.\env\Scripts\pytest --cov=csv_to_db\src --cov-report=html --cov-report=term

# Type checking
.\env\Scripts\mypy csv_to_db\src

# Linting
.\env\Scripts\flake8 csv_to_db\src

# Code complexity
.\env\Scripts\radon cc csv_to_db\src -a

# BDD tests
.\env\Scripts\behave csv_to_db\tests\bdd
```

## Fasi di Implementazione Suggerite

### Fase 1: Setup Base (Priorità Alta)
1. Creare struttura cartelle
2. Implementare DatabaseAdapter base e SQLiteAdapter
3. Implementare CSVReader con tests
4. Setup pytest e configurazione base

### Fase 2: Validazione (Priorità Alta)
1. Implementare DataValidator
2. Creare ValidationResult e classi errore
3. Unit tests per validazione
4. Integration test CSV → SQLite con validazione

### Fase 3: Import Completo (Priorità Media)
1. Implementare CSVImporter
2. Aggiungere gestione transazioni
3. Implementare dry-run mode
4. Integration tests per scenari completi

### Fase 4: Multi-Database (Priorità Media)
1. Implementare MSSQLAdapter
2. Implementare MariaDBAdapter
3. Integration tests per ogni database
4. Gestione connection pooling

### Fase 5: Configurazione e CLI (Priorità Media)
1. Implementare parsing YAML mappings
2. Creare main.py con argparse
3. Acceptance tests end-to-end
4. Documentazione utente

### Fase 6: BDD Tests (Priorità Bassa)
1. Scrivere feature files Gherkin
2. Implementare step definitions
3. Integrare Behave nel workflow testing
4. Report BDD

### Fase 7: Ottimizzazioni (Priorità Bassa)
1. Batch insert ottimizzato
2. Parallel processing per batch multipli
3. Caching schema database
4. Performance tests

## Esempi di Uso

### Scenario 1: Import singolo CSV
```powershell
.\env\Scripts\python.exe csv_to_db\main.py `
    data\allo_assegnazioni_dal20230901_aa_2023-24.csv `
    --db-type sqlite `
    --connection-string "data\test_databases\test.db" `
    --table assegnazioni `
    --csv-type assegnazioni
```

### Scenario 2: Dry-run validazione
```powershell
.\env\Scripts\python.exe csv_to_db\main.py `
    data\consumazioni_202309.csv `
    --db-type mssql `
    --connection-string "Driver={ODBC Driver 17 for SQL Server};Server=localhost;Database=testdb;UID=user;PWD=pass" `
    --table consumazioni `
    --dry-run `
    --output-format json
```

### Scenario 3: Uso programmatico
```python
from csv_to_db.src.database.sqlite_adapter import SQLiteAdapter
from csv_to_db.src.importer import CSVImporter
from csv_to_db.src.validator import DataValidator

# Setup
adapter = SQLiteAdapter()
adapter.connect('data/production.db')

# Configurazione validazione
schema = adapter.get_table_schema('assegnazioni')
validator = DataValidator(schema)

# Import
importer = CSVImporter(adapter, {'validator': validator})
result = importer.import_csv(
    'data/nuove_assegnazioni.csv',
    'assegnazioni',
    dry_run=False
)

# Gestione risultato
if result.success:
    print(f"Importate {result.rows_inserted} righe in {result.duration:.2f}s")
else:
    print("Errori validazione:")
    for error in result.validation_errors:
        print(f"  Riga {error.row}: {error.message}")
```

## Note di Compatibilità con Progetto Esistente

### Integrazione con libreria esistente:
- Mantenere pattern di lettura CSV con separatore `;` come default
- Riutilizzare logica pandas esistente dove possibile
- Convenzione nomi italiani per continuità con `library/pandas_days_for_month.py`
- Gestione encoding windows-1252 per retrocompatibilità

### Riuso codice:
La procedura può riutilizzare pattern dal progetto principale:
- Struttura testing (pytest + fixtures)
- Gestione DataFrame pandas
- Pattern di separazione logica/presentation

### Estensione futura:
La procedura csv_to_db può essere integrata con Flask per creare endpoint web:
```python
# erdis/import_csv.py (blueprint futuro)
@bp.route('/import', methods=['POST'])
def import_csv_endpoint():
    file = request.files['csv_file']
    db_type = request.form['db_type']
    # ... usa CSVImporter per processing
```

## Checklist Completamento

### Codice:
- [ ] Tutti i moduli implementati
- [ ] Type hints su tutte le funzioni pubbliche
- [ ] Docstrings complete
- [ ] Gestione eccezioni appropriata
- [ ] Logging configurato

### Tests:
- [ ] Unit tests con coverage > 90%
- [ ] Integration tests per ogni database
- [ ] Acceptance tests per scenari principali
- [ ] BDD features e steps implementati
- [ ] Tutti i test passano in CI

### Documentazione:
- [ ] README.md con istruzioni uso
- [ ] Esempi codice funzionanti
- [ ] Documentazione API (Sphinx opzionale)
- [ ] Commenti inline per logica complessa

### Qualità:
- [ ] Nessun errore flake8
- [ ] Type checking mypy passa
- [ ] Complexity accettabile (radon)
- [ ] Performance requirements soddisfatti

## Risorse Aggiuntive

### Collegamenti utili:
- [pytest documentation](https://docs.pytest.org/)
- [behave BDD framework](https://behave.readthedocs.io/)
- [pandas documentation](https://pandas.pydata.org/docs/)
- [SQLAlchemy documentation](https://docs.sqlalchemy.org/)
- [Python Database API Specification](https://peps.python.org/pep-0249/)

### Riferimenti progetto:
- Pattern esistenti: `library/pandas_days_for_month.py`
- Test examples: `tests/test_pandas_days_for_month.py`
- Flask integration: `erdis/assegnazioni.py`

---

**Versione documento**: 1.0  
**Data**: 26 ottobre 2025  
**Autore**: GitHub Copilot (generato su richiesta utente)
