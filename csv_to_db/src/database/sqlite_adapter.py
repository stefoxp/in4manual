"""
Adapter per database SQLite.

Implementa DatabaseAdapter per SQLite usando sqlite3 standard library.
"""

import sqlite3
from typing import Optional
import pandas as pd
import logging

from src.database.base import DatabaseAdapter
from src.exceptions import DatabaseConnectionError

logger = logging.getLogger(__name__)


class SQLiteAdapter(DatabaseAdapter):
    """Adapter per database SQLite."""

    def __init__(self):
        """Inizializza SQLite adapter."""
        super().__init__()
        self.connection: Optional[sqlite3.Connection] = None

    def connect(self, connection_string: str) -> None:
        """
        Stabilisce connessione a database SQLite.

        Args:
            connection_string: Path al file database SQLite

        Raises:
            DatabaseConnectionError: Se la connessione fallisce

        Example:
            >>> adapter = SQLiteAdapter()
            >>> adapter.connect('data/test.db')
        """
        try:
            self.connection = sqlite3.connect(connection_string)
            self.connection.row_factory = sqlite3.Row
            logger.info(f"Connesso a SQLite database: {connection_string}")
        except sqlite3.Error as e:
            raise DatabaseConnectionError(
                f"Impossibile connettersi a SQLite: {str(e)}", connection_string
            )

    def get_table_schema(self, table_name: str) -> dict:
        """
        Recupera schema della tabella usando PRAGMA table_info.

        Args:
            table_name: Nome della tabella

        Returns:
            Dizionario con schema della tabella

        Raises:
            DatabaseConnectionError: Se non connesso
            ValueError: Se tabella non esiste

        Example:
            >>> schema = adapter.get_table_schema('users')
            >>> print(schema['nome']['max_length'])
            50
        """
        if not self.is_connected():
            raise DatabaseConnectionError("Non connesso al database")

        try:
            cursor = self.connection.cursor()
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()

            if not columns:
                raise ValueError(f"Tabella '{table_name}' non esiste")

            schema = {}
            for col in columns:
                col_name = col[1]
                col_type = col[2].upper()
                is_nullable = col[3] == 0
                is_pk = col[5] == 1

                # Estrai lunghezza massima dal tipo (es. VARCHAR(50))
                max_length = None
                if "(" in col_type:
                    type_base = col_type.split("(")[0]
                    length_str = col_type.split("(")[1].rstrip(")")
                    try:
                        max_length = int(length_str)
                    except ValueError:
                        max_length = None
                else:
                    type_base = col_type

                schema[col_name] = {
                    "type": type_base,
                    "max_length": max_length,
                    "nullable": is_nullable,
                    "primary_key": is_pk,
                }

            logger.info(
                f"Schema recuperato per tabella '{table_name}': {len(schema)} colonne"
            )
            return schema

        except sqlite3.Error as e:
            raise DatabaseConnectionError(f"Errore nel recupero schema: {str(e)}")

    def insert_dataframe(
        self, df: pd.DataFrame, table_name: str, if_exists: str = "append"
    ) -> int:
        """
        Inserisce DataFrame nella tabella SQLite.

        Args:
            df: DataFrame pandas da inserire
            table_name: Nome tabella destinazione
            if_exists: Comportamento se tabella esiste ('fail', 'replace', 'append')

        Returns:
            Numero di righe inserite

        Raises:
            DatabaseConnectionError: Se non connesso
            ValueError: Se if_exists non valido

        Example:
            >>> df = pd.DataFrame({'nome': ['Mario'], 'cognome': ['Rossi']})
            >>> rows = adapter.insert_dataframe(df, 'users')
            >>> print(f"Inserite {rows} righe")
        """
        if not self.is_connected():
            raise DatabaseConnectionError("Non connesso al database")

        if if_exists not in ["fail", "replace", "append"]:
            raise ValueError(
                f"if_exists deve essere 'fail', 'replace' o 'append', ricevuto: {if_exists}"
            )

        try:
            rows_inserted = len(df)
            df.to_sql(table_name, self.connection, if_exists=if_exists, index=False)
            logger.info(f"Inserite {rows_inserted} righe nella tabella '{table_name}'")
            return rows_inserted

        except Exception as e:
            raise DatabaseConnectionError(f"Errore nell'inserimento dati: {str(e)}")

    def execute_query(self, query: str, params: Optional[tuple] = None) -> pd.DataFrame:
        """
        Esegue query SELECT e restituisce risultati come DataFrame.

        Args:
            query: Query SQL da eseguire
            params: Parametri opzionali per query parametrizzata

        Returns:
            DataFrame con risultati della query

        Raises:
            DatabaseConnectionError: Se non connesso
            ValueError: Se query non valida

        Example:
            >>> df = adapter.execute_query("SELECT * FROM users WHERE eta > ?", (18,))
            >>> print(len(df))
        """
        if not self.is_connected():
            raise DatabaseConnectionError("Non connesso al database")

        try:
            if params:
                df = pd.read_sql_query(query, self.connection, params=params)
            else:
                df = pd.read_sql_query(query, self.connection)

            logger.info(f"Query eseguita: {len(df)} righe restituite")
            return df

        except Exception as e:
            raise ValueError(f"Errore nell'esecuzione query: {str(e)}")

    def close(self) -> None:
        """
        Chiude connessione al database SQLite.

        Raises:
            DatabaseConnectionError: Se errore durante chiusura
        """
        if self.connection:
            try:
                self.connection.close()
                self.connection = None
                logger.info("Connessione SQLite chiusa")
            except sqlite3.Error as e:
                raise DatabaseConnectionError(
                    f"Errore nella chiusura connessione: {str(e)}"
                )

    def begin_transaction(self) -> None:
        """Inizia una transazione SQLite."""
        if not self.is_connected():
            raise DatabaseConnectionError("Non connesso al database")

        self.connection.execute("BEGIN TRANSACTION")
        logger.debug("Transazione iniziata")

    def commit(self) -> None:
        """Commit della transazione corrente."""
        if not self.is_connected():
            raise DatabaseConnectionError("Non connesso al database")

        try:
            self.connection.commit()
            logger.debug("Transazione committata")
        except sqlite3.Error as e:
            raise DatabaseConnectionError(f"Errore nel commit: {str(e)}")

    def rollback(self) -> None:
        """Rollback della transazione corrente."""
        if not self.is_connected():
            raise DatabaseConnectionError("Non connesso al database")

        try:
            self.connection.rollback()
            logger.debug("Transazione annullata (rollback)")
        except sqlite3.Error as e:
            raise DatabaseConnectionError(f"Errore nel rollback: {str(e)}")
