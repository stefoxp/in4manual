import pytest
import os
import csv
from csv_control.src.csv_validator import (
    detect_encoding,
    check_field_count_consistency,
    extract_record_info,
    validate_csv,
)


@pytest.fixture(scope="module")
def test_data_dir(tmpdir_factory):
    """Create a temporary directory for test data."""
    data_dir = tmpdir_factory.mktemp("data")

    # Consistent CSV
    consistent_csv_path = data_dir.join("consistent.csv")
    with open(consistent_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["h1", "h2", "h3"])
        writer.writerow(["d1", "d2", "d3"])
        writer.writerow(["v1", "v2", "v3"])

    # Inconsistent CSV
    inconsistent_csv_path = data_dir.join("inconsistent.csv")
    with open(inconsistent_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["h1", "h2"])
        writer.writerow(["d1", "d2", "d3"])  # Inconsistent
        writer.writerow(["v1", "v2"])

    # Empty CSV
    empty_csv_path = data_dir.join("empty.csv")
    open(empty_csv_path, "w").close()

    return data_dir


def test_detect_encoding(test_data_dir):
    """Test the encoding detection with chardet."""
    consistent_csv = test_data_dir.join("consistent.csv")
    # We expect chardet to identify ASCII or utf-8 for this simple file
    detected_encoding = detect_encoding(str(consistent_csv)).lower()
    assert detected_encoding in ["ascii", "utf-8"]


def test_check_field_count_consistency_consistent(test_data_dir):
    """Test field count consistency with a valid CSV."""
    consistent_csv = test_data_dir.join("consistent.csv")
    with open(consistent_csv, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        assert check_field_count_consistency(reader, str(consistent_csv)) is True


def test_check_field_count_consistency_inconsistent(test_data_dir):
    """Test field count consistency with an invalid CSV."""
    inconsistent_csv = test_data_dir.join("inconsistent.csv")
    with open(inconsistent_csv, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        assert check_field_count_consistency(reader, str(inconsistent_csv)) is False


def test_check_field_count_consistency_empty(test_data_dir):
    """Test field count consistency with an empty CSV."""
    empty_csv = test_data_dir.join("empty.csv")
    with open(empty_csv, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        assert check_field_count_consistency(reader, str(empty_csv)) is True


def test_extract_record_info(test_data_dir):
    """Test the extraction of record information."""
    consistent_csv = test_data_dir.join("consistent.csv")
    info = extract_record_info(str(consistent_csv), delimiter=";", field_index=1)

    assert len(info) == 3
    assert info[0]["line_number"] == 1
    assert info[0]["field_count"] == 3
    assert info[0]["field_value"] == "h2"
    assert info[1]["field_value"] == "d2"
    assert info[2]["field_value"] == "v2"


def test_extract_record_info_out_of_bounds_index(test_data_dir):
    """Test extraction with an out-of-bounds field index."""
    consistent_csv = test_data_dir.join("consistent.csv")
    info = extract_record_info(str(consistent_csv), delimiter=";", field_index=99)
    assert info[0]["field_value"] == "N/A"


def test_extract_record_info_file_not_found():
    """Test extraction with a non-existent file."""
    info = extract_record_info("non_existent_file.csv", delimiter=";", field_index=0)
    assert info == []


def test_validate_csv_consistent(test_data_dir):
    """Test the main validation function with a consistent file."""
    consistent_csv = test_data_dir.join("consistent.csv")
    assert validate_csv(str(consistent_csv), delimiter=";") is True


def test_validate_csv_inconsistent(test_data_dir):
    """Test the main validation function with an inconsistent file."""
    inconsistent_csv = test_data_dir.join("inconsistent.csv")
    assert validate_csv(str(inconsistent_csv), delimiter=";") is False


def test_validate_csv_file_not_found():
    """Test the main validation function with a non-existent file."""
    assert validate_csv("non_existent_file.csv") is False
