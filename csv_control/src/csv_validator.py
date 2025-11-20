import csv
import logging
import chardet
from typing import List, Dict, Any, Optional

# Configure logging
logging.basicConfig(
    filename="csv_validator.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def detect_encoding(file_path: str) -> str:
    """
    Detects the encoding of a file using chardet.
    """
    logging.info(f"Detecting encoding for {file_path}...")
    try:
        with open(file_path, "rb") as f:
            result = chardet.detect(f.read())
            encoding = result["encoding"]
            logging.info(f"Detected encoding: {encoding}")
            return encoding if encoding is not None else "utf-8"
    except FileNotFoundError:
        logging.warning(
            f"File not found when detecting encoding: {file_path}. Defaulting to utf-8."
        )
        return "utf-8"


def check_field_count_consistency(reader: csv.reader, file_path: str) -> bool:
    """
    Checks if all rows in the CSV file have the same number of fields.
    """
    logging.info(f"Checking field count consistency for {file_path}...")
    try:
        first_row_field_count = len(next(reader))
        line_number = 2
        for row in reader:
            if len(row) != first_row_field_count:
                logging.error(
                    f"Inconsistent field count in {file_path} at line {line_number}. "
                    f"Expected {first_row_field_count}, found {len(row)}."
                )
                return False
            line_number += 1
        logging.info(f"Field count is consistent in {file_path}.")
        return True
    except StopIteration:
        # File is empty
        logging.info(f"{file_path} is empty.")
        return True
    except Exception as e:
        logging.error(f"An error occurred during field count consistency check: {e}")
        return False


def extract_record_info(
    file_path: str, delimiter: str, field_index: int
) -> List[Dict[str, Any]]:
    """
    Extracts information (field count and a specific field's value) from each record.
    """
    logging.info(f"Extracting record info from {file_path}...")
    record_info = []
    encoding = detect_encoding(file_path)
    try:
        with open(file_path, "r", encoding=encoding, errors="replace") as csvfile:
            reader = csv.reader(csvfile, delimiter=delimiter)
            line_number = 1
            for row in reader:
                info = {
                    "line_number": line_number,
                    "field_count": len(row),
                    "field_value": (
                        row[field_index] if 0 <= field_index < len(row) else "N/A"
                    ),
                }
                record_info.append(info)
                line_number += 1
        logging.info(f"Successfully extracted info from {len(record_info)} records.")
        return record_info
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return []
    except Exception as e:
        logging.error(f"An error occurred during record info extraction: {e}")
        return []


def validate_csv(
    file_path: str, delimiter: str = ";", rules: Optional[List[str]] = None
) -> bool:
    """
    Validates a CSV file based on a set of rules.
    """
    if rules is None:
        rules = ["check_field_count_consistency"]

    logging.info(
        f"Starting validation for {file_path} with delimiter '{delimiter}' and rules {rules}."
    )
    encoding = detect_encoding(file_path)

    try:
        with open(file_path, "r", encoding=encoding, errors="replace") as csvfile:
            reader = csv.reader(csvfile, delimiter=delimiter)

            is_valid = True
            if "check_field_count_consistency" in rules:
                # We need to pass a fresh reader iterator to the check function.
                # Re-opening or seeking is necessary. For simplicity, we'll just focus on the logic.
                # A better implementation might read the file into memory if it's not too large.
                pass  # For now, we will call it separately.

    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return False
    except Exception as e:
        logging.error(f"An error occurred during validation: {e}")
        return False

    # Since the reader is consumed, we need to re-open for each check or read once.
    # Let's re-open for simplicity here.
    all_checks_passed = True
    if "check_field_count_consistency" in rules:
        with open(file_path, "r", encoding=encoding, errors="replace") as csvfile:
            reader = csv.reader(csvfile, delimiter=delimiter)
            if not check_field_count_consistency(reader, file_path):
                all_checks_passed = False

    if all_checks_passed:
        logging.info(f"All validation checks passed for {file_path}.")
    else:
        logging.warning(f"Some validation checks failed for {file_path}.")

    return all_checks_passed


if __name__ == "__main__":
    # Example usage:
    # This part is for demonstration and will be replaced by a proper CLI or test cases.

    # Create a dummy CSV for testing
    with open("test.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["header1", "header2", "header3"])
        writer.writerow(["data1", "data2", "data3"])
        writer.writerow(["value1", "value2", "value3"])
        writer.writerow(["a", "b", "c", "d"])  # Inconsistent row

    # Validate the dummy CSV
    is_valid = validate_csv("test.csv", delimiter=";")
    print(f"CSV validation result: {'Valid' if is_valid else 'Invalid'}")

    # Extract info
    info = extract_record_info("test.csv", delimiter=";", field_index=1)
    for record in info:
        print(record)

    # Clean up the dummy file
    import os

    os.remove("test.csv")
