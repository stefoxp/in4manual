# Copilot Instructions for in4manual

## Project Overview

Flask web application for automating data processing tasks for "in4m" - specifically calculating monthly day allocations from CSV housing assignment data using pandas. The app provides web upload interface and standalone CLI processing.

## Architecture

### Two Execution Modes

1. **Flask Web App** (`erdis/` package): Upload CSV files via web interface, get processed results as downloads
2. **CLI Script** (`main_local.py`): Batch process CSV files directly from command line

### Core Components

- `erdis/__init__.py`: Flask app factory with blueprint registration pattern
- `erdis/assegnazioni.py`: File upload endpoint that processes CSV and returns results
- `erdis/home.py`: Landing page blueprint
- `library/pandas_days_for_month.py`: Core business logic - calculates days per month between date ranges
- `library/pandas_join_tables.py`: Table joining logic (currently unused but available)

## Key Data Processing Logic

### pandas_days_for_month.main()

Transforms housing assignment CSV by:

1. Reading CSV with `;` separator (Italian format)
2. Calling `add_days_for_month()` to calculate days per month between `ASSE. DATA_ING` and `ASSE. DATA_UN` columns
3. Adding new columns with format `YYYYMM` (e.g., `202309`, `202310`) containing day counts
4. Replacing `.` with `,` in numeric columns (Italian decimal format) starting at column index 48
5. Returns CSV with `;` separator

**Critical**: Column index 48 is hardcoded (`START_COLUMN_INDEX`) - this assumes specific CSV structure from source system.

### Date Calculation Pattern

`days_of_month()` uses pandas date_range and resample to count days per month:
```python
s = pd.date_range(*x, freq="D").to_series()
return s.resample("ME").count().rename(lambda x: str(x.year) + fill_string(str(x.month), final_len=2))
```
This creates columns dynamically based on date range span.

## Development Workflow

### Environment Setup

- Python 3.12 virtual environment in `env/`
- Activate: `.\env\Scripts\activate` (PowerShell) or `.\env\Scripts\activate.bat` (CMD)
- Dependencies: Flask 3.0.2, pandas 2.2.1, pytest 8.1.1

### Running the App

**Flask Web Server** (production-like):
```powershell
.\flask_app_run.bat
```
This runs on host `10.10.240.4` - internal network deployment configuration.

**Development Server**:
```powershell
.\env\Scripts\python.exe -m flask --app erdis run --debug
```

**CLI Processing**:
```powershell
.\env\Scripts\python.exe main_local.py
```

### Testing

Run tests with pytest:
```powershell
.\env\Scripts\pytest
```

Test structure:

- `tests/conftest.py`: Flask test client fixtures
- `tests/test_erdis.py`: Integration tests for Flask endpoints
- `tests/test_pandas_days_for_month.py`: Unit tests for business logic functions

## Project Conventions

### CSV Format Expectations

- Separator: `;` (semicolon)
- Decimal: `,` (comma) - Italian locale
- Date columns: `ASSE. DATA_ING` (check-in), `ASSE. DATA_UN` (check-out)
- Encoding: Commented code suggests windows-1252 awareness (`.decode("windows-1252")`)

### Flask Patterns

- Blueprint-based routing: Each feature is a blueprint registered in `create_app()`
- Templates extend `layout.html` base with erdis branding
- File uploads validated with `ALLOWED_EXTENSIONS = {'csv'}`
- Results returned as attachments with `CALCOLATO_` prefix

### Naming Conventions

- Italian identifiers in domain logic: `assegnazioni` (assignments), `consumazioni` (consumptions)
- Date columns use Italian abbreviations: `DATA_ING` (data ingresso/entry), `DATA_UN` (data uscita/exit)
- Function naming: snake_case, descriptive (`add_days_for_month`, `replace_char_in_dataframe_columns`)

## Important Notes

- **Commented Code**: `price_for_month()` function exists but is commented out in production flow - suggests future pricing calculations
- **Windows Path**: `flask_app_run.bat` uses absolute path `C:\fat\in4manual\` - deployment-specific
- **Test Coverage**: `test_assegnazioni` expects 302 redirect but doesn't validate file processing - integration test coverage is minimal
- **DataFrame Columns**: New month columns are added dynamically - column count varies by date range in input data
