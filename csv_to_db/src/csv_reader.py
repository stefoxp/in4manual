"""
CSV Reader per lettura e parsing file CSV.

Supporta separatori personalizzabili, encoding multipli e validazione struttura.
"""

from pathlib import Path
from typing import Optional, List
import pandas as pd
import logging

from src.exceptions import ValidationError

logger = logging.getLogger(__name__)


class CSVReader:
    """Classe per lettura e parsing file CSV con configurazione flessibile."""

    def __init__(self, file_path: str, config: Optional[dict] = None):
        """
        Inizializza reader con path e configurazione.

        Args:
            file_path: Path al file CSV
            config: Dizionario configurazione opzionale con chiavi:
                - separator: Carattere separatore (default: ';')
                - encoding: Encoding file (default: 'utf-8')
                - has_header: Se CSV ha intestazioni (default: True)
                - decimal: Carattere decimale (default: '.')

        Raises:
            FileNotFoundError: Se file non esiste

        Example:
            >>> reader = CSVReader('data.csv', {'separator': ';', 'encoding': 'utf-8'})
            >>> df = reader.read()
        """
        self.file_path = Path(file_path)

        if not self.file_path.exists():
            raise FileNotFoundError(f"File non trovato: {file_path}")

        # Configurazione di default
        self.config = {
            "separator": ";",
            "encoding": "utf-8",
            "has_header": True,
            "decimal": ".",
        }

        # Aggiorna con config fornita
        if config:
            self.config.update(config)

        self._df: Optional[pd.DataFrame] = None
        logger.info(f"CSVReader inizializzato per file: {file_path}")

    def read(self) -> pd.DataFrame:
        """
        Legge CSV e restituisce DataFrame.

        Returns:
            DataFrame pandas con dati del CSV

        Raises:
            ValidationError: Se CSV malformato o non leggibile

        Example:
            >>> df = reader.read()
            >>> print(len(df))
            100
        """
        try:
            header = 0 if self.config["has_header"] else None

            self._df = pd.read_csv(
                self.file_path,
                sep=self.config["separator"],
                encoding=self.config["encoding"],
                header=header,
                decimal=self.config["decimal"],
                keep_default_na=True,
                na_values=["", "NA", "N/A", "null", "NULL"],
            )

            logger.info(
                f"CSV letto con successo: {len(self._df)} righe, "
                f"{len(self._df.columns)} colonne"
            )
            return self._df

        except pd.errors.ParserError as e:
            raise ValidationError(f"Errore nel parsing CSV: {str(e)}")
        except UnicodeDecodeError as e:
            raise ValidationError(
                f"Errore di encoding. Provare con encoding diverso. "
                f"Encoding attuale: {self.config['encoding']}"
            )
        except Exception as e:
            raise ValidationError(f"Errore nella lettura CSV: {str(e)}")

    def get_metadata(self) -> dict:
        """
        Restituisce metadata del CSV (colonne, tipi, righe).

        Returns:
            Dizionario con metadata:
            {
                'num_rows': int,
                'num_columns': int,
                'columns': list,
                'dtypes': dict,
                'null_counts': dict,
                'file_size_bytes': int
            }

        Raises:
            ValueError: Se CSV non ancora letto

        Example:
            >>> metadata = reader.get_metadata()
            >>> print(metadata['num_rows'])
            100
        """
        if self._df is None:
            raise ValueError("CSV non ancora letto. Chiamare read() prima.")

        metadata = {
            "num_rows": len(self._df),
            "num_columns": len(self._df.columns),
            "columns": list(self._df.columns),
            "dtypes": {col: str(dtype) for col, dtype in self._df.dtypes.items()},
            "null_counts": self._df.isnull().sum().to_dict(),
            "file_size_bytes": self.file_path.stat().st_size,
        }

        logger.debug(
            f"Metadata estratti: {metadata['num_rows']} righe, {metadata['num_columns']} colonne"
        )
        return metadata

    def validate_structure(self, expected_columns: List[str]) -> bool:
        """
        Verifica che le colonne attese siano presenti.

        Args:
            expected_columns: Lista nomi colonne attese

        Returns:
            True se tutte le colonne sono presenti

        Raises:
            ValueError: Se CSV non ancora letto
            ValidationError: Se colonne mancanti

        Example:
            >>> is_valid = reader.validate_structure(['nome', 'cognome', 'eta'])
            >>> print(is_valid)
            True
        """
        if self._df is None:
            raise ValueError("CSV non ancora letto. Chiamare read() prima.")

        actual_columns = set(self._df.columns)
        expected_columns_set = set(expected_columns)

        missing_columns = expected_columns_set - actual_columns

        if missing_columns:
            raise ValidationError(
                f"Colonne mancanti nel CSV: {', '.join(sorted(missing_columns))}"
            )

        extra_columns = actual_columns - expected_columns_set
        if extra_columns:
            logger.warning(
                f"Colonne extra nel CSV (ignorate): {', '.join(sorted(extra_columns))}"
            )

        logger.info("Struttura CSV validata con successo")
        return True

    def get_dataframe(self) -> pd.DataFrame:
        """
        Restituisce il DataFrame corrente.

        Returns:
            DataFrame pandas (può essere None se non ancora letto)

        Example:
            >>> df = reader.get_dataframe()
        """
        return self._df

    def detect_encoding(self) -> str:
        """
        Tenta di rilevare automaticamente l'encoding del file.

        Returns:
            Nome encoding rilevato (es. 'utf-8', 'windows-1252')

        Note:
            Richiede libreria 'chardet' (opzionale)
        """
        try:
            import chardet

            with open(self.file_path, "rb") as f:
                raw_data = f.read(10000)  # Leggi primi 10KB
                result = chardet.detect(raw_data)
                detected_encoding = result["encoding"]
                confidence = result["confidence"]

                logger.info(
                    f"Encoding rilevato: {detected_encoding} "
                    f"(confidenza: {confidence:.2%})"
                )
                return detected_encoding

        except ImportError:
            logger.warning(
                "chardet non installato. Impossibile rilevare encoding automaticamente."
            )
            return self.config["encoding"]
        except Exception as e:
            logger.warning(f"Errore nel rilevamento encoding: {str(e)}")
            return self.config["encoding"]
