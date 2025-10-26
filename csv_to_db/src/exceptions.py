"""
Eccezioni custom per il modulo csv_to_db.

Gerarchia:
    CSVImportError (base)
    ├── ValidationError
    ├── DatabaseConnectionError
    └── SchemaCompatibilityError
"""


class CSVImportError(Exception):
    """Errore base per import CSV."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class ValidationError(CSVImportError):
    """Errore di validazione dati."""

    def __init__(self, message: str, row: int = None, column: str = None):
        """
        Inizializza errore di validazione.

        Args:
            message: Descrizione errore
            row: Numero riga (opzionale)
            column: Nome colonna (opzionale)
        """
        self.row = row
        self.column = column
        full_message = message
        if row is not None:
            full_message = f"Riga {row}: {message}"
        if column:
            full_message = f"{full_message} (colonna: {column})"
        super().__init__(full_message)


class DatabaseConnectionError(CSVImportError):
    """Errore connessione database."""

    def __init__(self, message: str, connection_string: str = None):
        """
        Inizializza errore di connessione.

        Args:
            message: Descrizione errore
            connection_string: Stringa di connessione (opzionale, per debug)
        """
        self.connection_string = connection_string
        super().__init__(message)


class SchemaCompatibilityError(CSVImportError):
    """Errore compatibilità schema CSV-DB."""

    def __init__(self, message: str, csv_columns: list = None, db_columns: list = None):
        """
        Inizializza errore di compatibilità schema.

        Args:
            message: Descrizione errore
            csv_columns: Lista colonne CSV (opzionale)
            db_columns: Lista colonne DB (opzionale)
        """
        self.csv_columns = csv_columns
        self.db_columns = db_columns
        super().__init__(message)
