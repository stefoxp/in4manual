"""
Unit tests per CSVReader.

Tests per lettura, parsing e validazione file CSV.
"""

import pytest
import tempfile
from pathlib import Path
import pandas as pd
from unittest.mock import patch, mock_open
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.csv_reader import CSVReader
from src.exceptions import ValidationError


@pytest.fixture
def temp_csv_semicolon(tmp_path):
    """Crea CSV temporaneo con separatore punto e virgola."""
    csv_file = tmp_path / "test_semicolon.csv"
    content = "col1;col2;col3\nval1;val2;val3\nval4;val5;val6"
    csv_file.write_text(content, encoding="utf-8")
    return str(csv_file)


@pytest.fixture
def temp_csv_comma(tmp_path):
    """Crea CSV temporaneo con separatore virgola."""
    csv_file = tmp_path / "test_comma.csv"
    content = "col1,col2,col3\nval1,val2,val3\nval4,val5,val6"
    csv_file.write_text(content, encoding="utf-8")
    return str(csv_file)


@pytest.fixture
def temp_csv_windows1252(tmp_path):
    """Crea CSV temporaneo con encoding Windows-1252."""
    csv_file = tmp_path / "test_windows.csv"
    content = "nome;città\nMario;Città con àccenti"
    csv_file.write_text(content, encoding="windows-1252")
    return str(csv_file)


@pytest.fixture
def temp_csv_empty(tmp_path):
    """Crea CSV vuoto."""
    csv_file = tmp_path / "test_empty.csv"
    csv_file.write_text("", encoding="utf-8")
    return str(csv_file)


@pytest.fixture
def temp_csv_malformed(tmp_path):
    """Crea CSV malformato."""
    csv_file = tmp_path / "test_malformed.csv"
    content = "col1;col2;col3\nval1;val2\nval3;val4;val5;val6"
    csv_file.write_text(content, encoding="utf-8")
    return str(csv_file)


class TestCSVReaderInit:
    """Test per inizializzazione CSVReader."""

    def test_init_with_valid_file(self, temp_csv_semicolon):
        """Test inizializzazione con file valido."""
        reader = CSVReader(temp_csv_semicolon)
        assert reader.file_path == Path(temp_csv_semicolon)
        assert reader.config["separator"] == ";"
        assert reader.config["encoding"] == "utf-8"

    def test_init_with_custom_config(self, temp_csv_comma):
        """Test inizializzazione con configurazione custom."""
        config = {"separator": ",", "encoding": "utf-8"}
        reader = CSVReader(temp_csv_comma, config)
        assert reader.config["separator"] == ","

    def test_init_with_nonexistent_file(self):
        """Test inizializzazione con file inesistente."""
        with pytest.raises(FileNotFoundError):
            CSVReader("nonexistent.csv")


class TestCSVReaderRead:
    """Test per metodo read()."""

    def test_read_csv_with_semicolon_separator(self, temp_csv_semicolon):
        """Test lettura CSV con separatore punto e virgola."""
        reader = CSVReader(temp_csv_semicolon, {"separator": ";"})
        df = reader.read()

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert list(df.columns) == ["col1", "col2", "col3"]
        assert df.iloc[0]["col1"] == "val1"

    def test_read_csv_with_comma_separator(self, temp_csv_comma):
        """Test lettura CSV con separatore virgola."""
        reader = CSVReader(temp_csv_comma, {"separator": ","})
        df = reader.read()

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert list(df.columns) == ["col1", "col2", "col3"]

    def test_read_csv_with_different_encodings(self, temp_csv_windows1252):
        """Test lettura CSV con encoding Windows-1252."""
        reader = CSVReader(
            temp_csv_windows1252, {"separator": ";", "encoding": "windows-1252"}
        )
        df = reader.read()

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 1
        assert "nome" in df.columns

    def test_handle_empty_csv_file(self, temp_csv_empty):
        """Test gestione file CSV vuoto."""
        reader = CSVReader(temp_csv_empty)
        with pytest.raises(ValidationError):
            reader.read()

    def test_handle_malformed_csv(self, temp_csv_malformed):
        """Test gestione CSV malformato (colonne inconsistenti)."""
        reader = CSVReader(temp_csv_malformed)
        # CSV malformato deve sollevare ValidationError
        with pytest.raises(ValidationError, match="Errore nel parsing"):
            reader.read()


class TestCSVReaderMetadata:
    """Test per metodo get_metadata()."""

    def test_get_metadata_returns_correct_info(self, temp_csv_semicolon):
        """Test che get_metadata restituisce informazioni corrette."""
        reader = CSVReader(temp_csv_semicolon)
        reader.read()
        metadata = reader.get_metadata()

        assert metadata["num_rows"] == 2
        assert metadata["num_columns"] == 3
        assert metadata["columns"] == ["col1", "col2", "col3"]
        assert "dtypes" in metadata
        assert "null_counts" in metadata
        assert metadata["file_size_bytes"] > 0

    def test_get_metadata_before_read_raises_error(self, temp_csv_semicolon):
        """Test che get_metadata solleva errore se chiamato prima di read()."""
        reader = CSVReader(temp_csv_semicolon)
        with pytest.raises(ValueError, match="CSV non ancora letto"):
            reader.get_metadata()


class TestCSVReaderValidation:
    """Test per metodo validate_structure()."""

    def test_validate_structure_with_valid_columns(self, temp_csv_semicolon):
        """Test validazione con colonne valide."""
        reader = CSVReader(temp_csv_semicolon)
        reader.read()
        result = reader.validate_structure(["col1", "col2", "col3"])
        assert result is True

    def test_validate_structure_with_missing_columns(self, temp_csv_semicolon):
        """Test validazione con colonne mancanti."""
        reader = CSVReader(temp_csv_semicolon)
        reader.read()

        with pytest.raises(ValidationError, match="Colonne mancanti"):
            reader.validate_structure(["col1", "col2", "col3", "col4"])

    def test_validate_structure_with_subset_of_columns(self, temp_csv_semicolon):
        """Test validazione con sottoinsieme di colonne."""
        reader = CSVReader(temp_csv_semicolon)
        reader.read()
        result = reader.validate_structure(["col1", "col2"])
        assert result is True

    def test_validate_structure_before_read_raises_error(self, temp_csv_semicolon):
        """Test che validate_structure solleva errore se chiamato prima di read()."""
        reader = CSVReader(temp_csv_semicolon)
        with pytest.raises(ValueError, match="CSV non ancora letto"):
            reader.validate_structure(["col1"])


class TestCSVReaderGetDataFrame:
    """Test per metodo get_dataframe()."""

    def test_get_dataframe_after_read(self, temp_csv_semicolon):
        """Test get_dataframe dopo read()."""
        reader = CSVReader(temp_csv_semicolon)
        reader.read()
        df = reader.get_dataframe()

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2

    def test_get_dataframe_before_read(self, temp_csv_semicolon):
        """Test get_dataframe prima di read()."""
        reader = CSVReader(temp_csv_semicolon)
        df = reader.get_dataframe()
        assert df is None


class TestCSVReaderDetectEncoding:
    """Test per metodo detect_encoding()."""

    def test_detect_encoding_without_chardet(self, temp_csv_semicolon):
        """Test detect_encoding quando chardet non disponibile."""
        reader = CSVReader(temp_csv_semicolon)

        with patch("builtins.__import__", side_effect=ImportError):
            encoding = reader.detect_encoding()
            assert encoding == "utf-8"  # Fallback a config default
