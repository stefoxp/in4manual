"""
CSV Control - Modulo per la verifica e correzione della struttura di file CSV

Questo modulo fornisce funzionalità per:
1. Analizzare la struttura di file CSV in una cartella
2. Verificare la coerenza del numero di campi tra header e record
3. Correggere record con campi mancanti
4. Standardizzare tutti i file al formato con il maggior numero di campi
5. Generare file CSV corretti e omogenei

Autore: ERDIS SQL Team
Data: Novembre 2025
"""

import csv
import os
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from collections import Counter


@dataclass
class CSVAnalysis:
    """Classe per contenere i risultati dell'analisi di un file CSV"""

    filename: str
    num_fields: int
    headers: List[str]
    num_records: int
    inconsistent_records: List[Tuple[int, int]]  # (row_number, num_fields)

    def __str__(self):
        return (
            f"File: {self.filename}\n"
            f"  Headers: {self.num_fields}\n"
            f"  Records: {self.num_records}\n"
            f"  Inconsistent: {len(self.inconsistent_records)}"
        )


class CSVController:
    """Classe principale per il controllo e la correzione di file CSV"""

    def __init__(self, folder_path: str, delimiter: str = ";", encoding: str = "utf-8"):
        """
        Inizializza il controller CSV

        Args:
            folder_path: Percorso della cartella contenente i file CSV
            delimiter: Delimitatore utilizzato nei CSV (default: ';')
            encoding: Codifica dei file (default: 'utf-8')
        """
        self.folder_path = Path(folder_path)
        self.delimiter = delimiter
        self.encoding = encoding
        self.analyses: List[CSVAnalysis] = []

        if not self.folder_path.exists():
            raise ValueError(f"La cartella {folder_path} non esiste")

    def get_csv_files(self) -> List[Path]:
        """Ottiene la lista di tutti i file CSV nella cartella"""
        return sorted(self.folder_path.glob("*.csv"))

    def analyze_csv_file(self, filepath: Path) -> CSVAnalysis:
        """
        Analizza un singolo file CSV

        Args:
            filepath: Percorso del file CSV

        Returns:
            CSVAnalysis: Oggetto contenente i risultati dell'analisi
        """
        with open(filepath, "r", encoding=self.encoding, newline="") as f:
            reader = csv.reader(f, delimiter=self.delimiter)

            # Leggi l'header
            headers = next(reader)
            num_fields = len(headers)

            # Analizza i record
            inconsistent_records = []
            num_records = 0

            for row_num, row in enumerate(
                reader, start=2
            ):  # start=2 perché row 1 è l'header
                num_records += 1
                if len(row) != num_fields:
                    inconsistent_records.append((row_num, len(row)))

            return CSVAnalysis(
                filename=filepath.name,
                num_fields=num_fields,
                headers=headers,
                num_records=num_records,
                inconsistent_records=inconsistent_records,
            )

    def analyze_all_files(self) -> List[CSVAnalysis]:
        """
        Analizza tutti i file CSV nella cartella

        Returns:
            List[CSVAnalysis]: Lista delle analisi per ciascun file
        """
        csv_files = self.get_csv_files()
        self.analyses = [self.analyze_csv_file(f) for f in csv_files]
        return self.analyses

    def get_master_headers(self) -> List[str]:
        """
        Determina l'insieme completo di headers da utilizzare
        Sceglie il file con il maggior numero di campi

        Returns:
            List[str]: Lista degli headers master
        """
        if not self.analyses:
            self.analyze_all_files()

        if not self.analyses:
            raise ValueError("Nessun file CSV trovato nella cartella")

        # Trova il file con il maggior numero di campi
        max_analysis = max(self.analyses, key=lambda a: a.num_fields)
        return max_analysis.headers

    def fix_record_length(
        self, row: List[str], expected_headers: List[str], current_headers: List[str]
    ) -> List[str]:
        """
        Corregge la lunghezza di un record aggiungendo campi mancanti

        Args:
            row: Record da correggere
            expected_headers: Headers attesi (master)
            current_headers: Headers del file corrente

        Returns:
            List[str]: Record corretto
        """
        if len(row) == len(expected_headers):
            return row

        # Crea un dizionario con i valori attuali
        current_dict = {}
        for i, value in enumerate(row):
            if i < len(current_headers):
                current_dict[current_headers[i]] = value

        # Costruisci il record corretto nell'ordine dei master headers
        fixed_row = []
        for header in expected_headers:
            if header in current_dict:
                fixed_row.append(current_dict[header])
            else:
                fixed_row.append("")  # Campo mancante

        return fixed_row

    def process_and_save(self, output_folder: Optional[str] = None) -> Dict[str, str]:
        """
        Processa tutti i file CSV e salva le versioni corrette

        Args:
            output_folder: Cartella di output (default: output/ nella stessa directory)

        Returns:
            Dict[str, str]: Mappa filename -> output_path
        """
        if not self.analyses:
            self.analyze_all_files()

        # Determina la cartella di output
        if output_folder is None:
            output_path = self.folder_path.parent / "output"
        else:
            output_path = Path(output_folder)

        output_path.mkdir(parents=True, exist_ok=True)

        # Ottieni gli headers master
        master_headers = self.get_master_headers()

        # Processa ogni file
        output_files = {}
        csv_files = self.get_csv_files()

        for filepath, analysis in zip(csv_files, self.analyses):
            output_filepath = output_path / filepath.name

            with open(filepath, "r", encoding=self.encoding, newline="") as infile:
                reader = csv.reader(infile, delimiter=self.delimiter)

                # Salta l'header originale
                current_headers = next(reader)

                with open(
                    output_filepath, "w", encoding=self.encoding, newline=""
                ) as outfile:
                    writer = csv.writer(outfile, delimiter=self.delimiter)

                    # Scrivi l'header master
                    writer.writerow(master_headers)

                    # Processa e scrivi i record
                    for row in reader:
                        fixed_row = self.fix_record_length(
                            row, master_headers, current_headers
                        )
                        writer.writerow(fixed_row)

            output_files[filepath.name] = str(output_filepath)

        return output_files

    def generate_report(self) -> str:
        """
        Genera un report testuale dell'analisi

        Returns:
            str: Report formattato
        """
        if not self.analyses:
            self.analyze_all_files()

        report_lines = [
            "=" * 70,
            "REPORT ANALISI FILE CSV",
            "=" * 70,
            f"\nCartella analizzata: {self.folder_path}",
            f"Numero file CSV trovati: {len(self.analyses)}",
            "\n" + "-" * 70,
        ]

        # Analisi dettagliata per file
        for analysis in self.analyses:
            report_lines.append(f"\n{analysis}")
            if analysis.inconsistent_records:
                report_lines.append(f"  Record non coerenti:")
                for row_num, num_fields in analysis.inconsistent_records[
                    :5
                ]:  # mostra primi 5
                    report_lines.append(f"    - Riga {row_num}: {num_fields} campi")
                if len(analysis.inconsistent_records) > 5:
                    report_lines.append(
                        f"    ... e altri {len(analysis.inconsistent_records) - 5}"
                    )

        # Riepilogo
        report_lines.extend(
            [
                "\n" + "-" * 70,
                "\nRIEPILOGO:",
            ]
        )

        master_headers = self.get_master_headers()
        report_lines.append(
            f"Numero di campi standard (massimo): {len(master_headers)}"
        )

        files_needing_fix = [
            a
            for a in self.analyses
            if a.inconsistent_records or a.num_fields != len(master_headers)
        ]
        report_lines.append(
            f"File che necessitano correzione: {len(files_needing_fix)}"
        )

        report_lines.append("\nCampi master (primi 10):")
        for i, header in enumerate(master_headers[:10], 1):
            report_lines.append(f"  {i}. {header}")
        if len(master_headers) > 10:
            report_lines.append(f"  ... e altri {len(master_headers) - 10} campi")

        report_lines.append("\n" + "=" * 70)

        return "\n".join(report_lines)


def main():
    """Funzione principale per l'esecuzione da riga di comando"""
    import sys

    if len(sys.argv) < 2:
        print("Uso: python csv_control.py <cartella_csv> [cartella_output]")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_folder = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        controller = CSVController(input_folder)

        # Analizza i file
        print("Analisi dei file CSV in corso...")
        controller.analyze_all_files()

        # Genera e mostra il report
        print(controller.generate_report())

        # Processa e salva i file corretti
        print(f"\nProcessamento file in corso...")
        output_files = controller.process_and_save(output_folder)

        print("\nFile corretti generati:")
        for original, output in output_files.items():
            print(f"  {original} -> {output}")

        print("\nOperazione completata con successo!")

    except Exception as e:
        print(f"ERRORE: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
