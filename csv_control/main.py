# import os
from src import csv_validator
from pathlib import Path

directory = Path("data/gra_alloggi")
file_list = [f.name for f in directory.iterdir() if f.is_file()]
print("File presenti nella cartella:", file_list)

for file_i in file_list:
    file_in = "data/gra_alloggi/" + file_i

    print(f"\nProcessing file: {file_in}")
    is_valid = csv_validator.validate_csv(file_in, delimiter=";")
    print(f"CSV validation result: {'Valid' if is_valid else 'Invalid'}")

    # Extract info
    info = csv_validator.extract_record_info(file_in, delimiter=";", field_index=1)
    for record in info:
        print(record)
