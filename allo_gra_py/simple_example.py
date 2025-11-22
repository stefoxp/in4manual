"""
Esempio semplice di utilizzo del modulo csv_control
"""

import sys
import os

# Assicura che l'output sia in UTF-8
if sys.platform == "win32":
    os.environ["PYTHONIOENCODING"] = "utf-8"

from src.csv_control import CSVController


def main():
    print("=" * 70)
    print("CSV CONTROL - Esempio di Utilizzo")
    print("=" * 70)

    # Inizializza il controller
    print("\n1. Inizializzazione...")
    controller = CSVController("data")

    # Analizza i file
    print("\n2. Analisi file CSV...")
    analyses = controller.analyze_all_files()
    print(f"   File trovati: {len(analyses)}")

    for analysis in analyses:
        print(f"\n   - {analysis.filename}")
        print(f"     Campi: {analysis.num_fields}")
        print(f"     Record: {analysis.num_records}")
        if analysis.inconsistent_records:
            print(f"     Record inconsistenti: {len(analysis.inconsistent_records)}")
        else:
            print(f"     OK: Tutti i record sono consistenti")

    # Ottieni master headers
    print("\n3. Identificazione headers master...")
    master_headers = controller.get_master_headers()
    print(f"   Numero campi standard: {len(master_headers)}")
    print(f"   Primi 5 campi: {', '.join(master_headers[:5])}")

    # Processa e salva
    print("\n4. Correzione e salvataggio...")
    output_files = controller.process_and_save()
    print(f"   File corretti generati: {len(output_files)}")

    for original, corrected in output_files.items():
        print(f"   - {original}")

    print("\n" + "=" * 70)
    print("Operazione completata con successo!")
    print("=" * 70)
    print(f"\nFile corretti disponibili in: output/")


if __name__ == "__main__":
    main()
