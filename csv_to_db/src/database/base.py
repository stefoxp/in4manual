"""
Interfaccia base per database adapters.

Implementa il pattern Strategy/Adapter per supportare diversi database
mantenendo un'interfaccia uniforme.
"""

from abc import ABC, abstractmethod
from typing import Optional
import pandas as pd


class DatabaseAdapter(ABC):
    """Interfaccia astratta per adapter di database."""

    def __init__(self):
        """Inizializza adapter."""
        self.connection = None

    @abstractmethod
    def connect(self, connection_string: str) -> None:
        """
        Stabilisce connessione al database.

        Args:
            connection_string: Stringa di connessione al database

        Raises:
            DatabaseConnectionError: Se la connessione fallisce
        """
        pass

    @abstractmethod
    def get_table_schema(self, table_name: str) -> dict:
        """
        Recupera schema della tabella (colonne, tipi, lunghezze).

        Args:
            table_name: Nome della tabella

        Returns:
            Dizionario con schema della tabella. Formato:
            {
                'column_name': {
                    'type': 'VARCHAR',
                    'max_length': 50,
                    'nullable': True,
                    'primary_key': False
                },
                ...
            }

        Raises:
            DatabaseConnectionError: Se non connesso
            ValueError: Se tabella non esiste
        """
        pass

    @abstractmethod
    def insert_dataframe(
        self, df: pd.DataFrame, table_name: str, if_exists: str = "append"
    ) -> int:
        """
        Inserisce DataFrame nella tabella.

        Args:
            df: DataFrame pandas da inserire
            table_name: Nome tabella destinazione
            if_exists: Comportamento se tabella esiste ('fail', 'replace', 'append')

        Returns:
            Numero di righe inserite

        Raises:
            DatabaseConnectionError: Se non connesso
            ValueError: Se tabella non esiste o struttura incompatibile
        """
        pass

    @abstractmethod
    def execute_query(self, query: str, params: Optional[tuple] = None) -> pd.DataFrame:
        """
        Esegue query SELECT e restituisce risultati.

        Args:
            query: Query SQL da eseguire
            params: Parametri opzionali per query parametrizzata

        Returns:
            DataFrame con risultati della query

        Raises:
            DatabaseConnectionError: Se non connesso
            ValueError: Se query non valida
        """
        pass

    @abstractmethod
    def close(self) -> None:
        """
        Chiude connessione al database.

        Raises:
            DatabaseConnectionError: Se errore durante chiusura
        """
        pass

    def is_connected(self) -> bool:
        """
        Verifica se connessione è attiva.

        Returns:
            True se connesso, False altrimenti
        """
        return self.connection is not None

    def begin_transaction(self) -> None:
        """
        Inizia una transazione.

        Da implementare nelle sottoclassi se supportato.
        """
        pass

    def commit(self) -> None:
        """
        Commit della transazione corrente.

        Da implementare nelle sottoclassi se supportato.
        """
        pass

    def rollback(self) -> None:
        """
        Rollback della transazione corrente.

        Da implementare nelle sottoclassi se supportato.
        """
        pass
