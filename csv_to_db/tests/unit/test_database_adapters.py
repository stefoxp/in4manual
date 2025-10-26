"""
Unit tests per Database Adapters.

Tests per SQLiteAdapter e interfaccia DatabaseAdapter.
"""

import pytest
import sqlite3
import tempfile
from pathlib import Path
import pandas as pd
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.database.sqlite_adapter import SQLiteAdapter
from src.exceptions import DatabaseConnectionError


@pytest.fixture
def temp_db(tmp_path):
    """Crea database SQLite temporaneo."""
    db_file = tmp_path / "test.db"
    return str(db_file)


@pytest.fixture
def test_database_with_table(tmp_path):
    """Crea database SQLite temporaneo con tabella di test."""
    db_file = tmp_path / "test_with_table.db"
    conn = sqlite3.connect(str(db_file))

    # Crea tabella di test
    conn.execute(
        """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome VARCHAR(50) NOT NULL,
            cognome VARCHAR(50) NOT NULL,
            eta INTEGER,
            email VARCHAR(100)
        )
    """
    )

    # Inserisci dati di test
    conn.execute(
        """
        INSERT INTO users (nome, cognome, eta, email)
        VALUES ('Mario', 'Rossi', 30, 'mario@test.it')
    """
    )
    conn.execute(
        """
        INSERT INTO users (nome, cognome, eta, email)
        VALUES ('Luigi', 'Verdi', 25, 'luigi@test.it')
    """
    )

    conn.commit()
    conn.close()

    return str(db_file)


class TestSQLiteAdapterConnection:
    """Test per connessione SQLite."""

    def test_connect_success(self, temp_db):
        """Test connessione riuscita a database SQLite."""
        adapter = SQLiteAdapter()
        adapter.connect(temp_db)

        assert adapter.is_connected()
        assert adapter.connection is not None

        adapter.close()

    def test_connect_creates_new_db(self, tmp_path):
        """Test che connect crea nuovo database se non esiste."""
        db_path = tmp_path / "new_db.db"
        adapter = SQLiteAdapter()
        adapter.connect(str(db_path))

        assert db_path.exists()
        assert adapter.is_connected()

        adapter.close()

    def test_connect_failure_invalid_path(self):
        """Test connessione fallita con path non valido."""
        adapter = SQLiteAdapter()
        # Path impossibile su Windows
        with pytest.raises(DatabaseConnectionError):
            adapter.connect("/invalid/path/\\0/test.db")

    def test_is_connected_before_connection(self):
        """Test is_connected prima della connessione."""
        adapter = SQLiteAdapter()
        assert not adapter.is_connected()

    def test_close_connection(self, temp_db):
        """Test chiusura connessione."""
        adapter = SQLiteAdapter()
        adapter.connect(temp_db)
        adapter.close()

        assert not adapter.is_connected()
        assert adapter.connection is None


class TestSQLiteAdapterSchema:
    """Test per recupero schema."""

    def test_get_table_schema_existing_table(self, test_database_with_table):
        """Test recupero schema tabella esistente."""
        adapter = SQLiteAdapter()
        adapter.connect(test_database_with_table)

        schema = adapter.get_table_schema("users")

        assert "nome" in schema
        assert "cognome" in schema
        assert "eta" in schema

        assert schema["nome"]["type"] == "VARCHAR"
        assert schema["nome"]["max_length"] == 50
        assert schema["nome"]["nullable"] is False

        assert schema["id"]["primary_key"] is True

        adapter.close()

    def test_get_table_schema_nonexistent_table(self, temp_db):
        """Test recupero schema tabella inesistente."""
        adapter = SQLiteAdapter()
        adapter.connect(temp_db)

        with pytest.raises(ValueError, match="non esiste"):
            adapter.get_table_schema("nonexistent_table")

        adapter.close()

    def test_get_table_schema_not_connected(self):
        """Test get_table_schema senza connessione."""
        adapter = SQLiteAdapter()

        with pytest.raises(DatabaseConnectionError, match="Non connesso"):
            adapter.get_table_schema("users")


class TestSQLiteAdapterInsert:
    """Test per inserimento dati."""

    def test_insert_dataframe_success(self, test_database_with_table):
        """Test inserimento DataFrame riuscito."""
        adapter = SQLiteAdapter()
        adapter.connect(test_database_with_table)

        # Crea DataFrame di test
        df = pd.DataFrame(
            {
                "nome": ["Anna", "Paolo"],
                "cognome": ["Bianchi", "Neri"],
                "eta": [28, 35],
                "email": ["anna@test.it", "paolo@test.it"],
            }
        )

        rows = adapter.insert_dataframe(df, "users", if_exists="append")

        assert rows == 2

        # Verifica inserimento
        result_df = adapter.execute_query(
            "SELECT * FROM users WHERE nome IN ('Anna', 'Paolo')"
        )
        assert len(result_df) == 2

        adapter.close()

    def test_insert_dataframe_replace(self, test_database_with_table):
        """Test inserimento con replace."""
        adapter = SQLiteAdapter()
        adapter.connect(test_database_with_table)

        df = pd.DataFrame(
            {
                "nome": ["Nuovo"],
                "cognome": ["Utente"],
                "eta": [40],
                "email": ["nuovo@test.it"],
            }
        )

        adapter.insert_dataframe(df, "users", if_exists="replace")

        # Verifica che tabella sia stata sostituita
        result_df = adapter.execute_query("SELECT * FROM users")
        assert len(result_df) == 1
        assert result_df.iloc[0]["nome"] == "Nuovo"

        adapter.close()

    def test_insert_dataframe_not_connected(self):
        """Test insert_dataframe senza connessione."""
        adapter = SQLiteAdapter()
        df = pd.DataFrame({"col": [1, 2, 3]})

        with pytest.raises(DatabaseConnectionError, match="Non connesso"):
            adapter.insert_dataframe(df, "test_table")

    def test_insert_dataframe_invalid_if_exists(self, test_database_with_table):
        """Test insert_dataframe con if_exists non valido."""
        adapter = SQLiteAdapter()
        adapter.connect(test_database_with_table)
        df = pd.DataFrame({"nome": ["Test"]})

        with pytest.raises(ValueError, match="if_exists"):
            adapter.insert_dataframe(df, "users", if_exists="invalid")

        adapter.close()


class TestSQLiteAdapterQuery:
    """Test per esecuzione query."""

    def test_execute_query_returns_dataframe(self, test_database_with_table):
        """Test esecuzione query restituisce DataFrame."""
        adapter = SQLiteAdapter()
        adapter.connect(test_database_with_table)

        df = adapter.execute_query("SELECT * FROM users")

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert "nome" in df.columns

        adapter.close()

    def test_execute_query_with_params(self, test_database_with_table):
        """Test query parametrizzata."""
        adapter = SQLiteAdapter()
        adapter.connect(test_database_with_table)

        df = adapter.execute_query("SELECT * FROM users WHERE eta > ?", (26,))

        assert len(df) == 1
        assert df.iloc[0]["nome"] == "Mario"

        adapter.close()

    def test_execute_query_not_connected(self):
        """Test execute_query senza connessione."""
        adapter = SQLiteAdapter()

        with pytest.raises(DatabaseConnectionError, match="Non connesso"):
            adapter.execute_query("SELECT 1")

    def test_execute_query_invalid_sql(self, test_database_with_table):
        """Test query SQL non valida."""
        adapter = SQLiteAdapter()
        adapter.connect(test_database_with_table)

        with pytest.raises(ValueError):
            adapter.execute_query("INVALID SQL QUERY")

        adapter.close()


class TestSQLiteAdapterTransactions:
    """Test per gestione transazioni."""

    def test_commit_transaction(self, test_database_with_table):
        """Test commit transazione."""
        adapter = SQLiteAdapter()
        adapter.connect(test_database_with_table)

        adapter.begin_transaction()

        df = pd.DataFrame(
            {
                "nome": ["Test"],
                "cognome": ["Commit"],
                "eta": [30],
                "email": ["test@test.it"],
            }
        )
        adapter.insert_dataframe(df, "users", if_exists="append")

        adapter.commit()

        # Verifica che dati siano persistiti
        result = adapter.execute_query("SELECT * FROM users WHERE nome = 'Test'")
        assert len(result) == 1

        adapter.close()

    def test_rollback_transaction(self, test_database_with_table):
        """Test rollback transazione."""
        adapter = SQLiteAdapter()
        adapter.connect(test_database_with_table)

        # Conta righe iniziali
        initial_count = len(adapter.execute_query("SELECT * FROM users"))

        # Nota: pandas to_sql non rispetta le transazioni manuali
        # Usiamo execute diretto per test transazioni
        cursor = adapter.connection.cursor()
        cursor.execute(
            """
            INSERT INTO users (nome, cognome, eta, email)
            VALUES (?, ?, ?, ?)
        """,
            ("Test", "Rollback", 30, "test@test.it"),
        )

        adapter.rollback()

        # Verifica che dati NON siano persistiti
        final_count = len(adapter.execute_query("SELECT * FROM users"))
        assert final_count == initial_count

        adapter.close()

    def test_transaction_not_connected(self):
        """Test operazioni transazione senza connessione."""
        adapter = SQLiteAdapter()

        with pytest.raises(DatabaseConnectionError):
            adapter.begin_transaction()

        with pytest.raises(DatabaseConnectionError):
            adapter.commit()

        with pytest.raises(DatabaseConnectionError):
            adapter.rollback()
