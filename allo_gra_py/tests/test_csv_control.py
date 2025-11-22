"""
Test unitari per il modulo csv_control
"""

import pytest
import csv
from pathlib import Path
from src.csv_control import CSVController, CSVAnalysis


class TestCSVAnalysis:
    """Test per la classe CSVAnalysis"""

    def test_csv_analysis_creation(self):
        """Test creazione oggetto CSVAnalysis"""
        analysis = CSVAnalysis(
            filename="test.csv",
            num_fields=5,
            headers=["A", "B", "C", "D", "E"],
            num_records=10,
            inconsistent_records=[],
        )

        assert analysis.filename == "test.csv"
        assert analysis.num_fields == 5
        assert len(analysis.headers) == 5
        assert analysis.num_records == 10
        assert len(analysis.inconsistent_records) == 0

    def test_csv_analysis_str(self):
        """Test rappresentazione stringa di CSVAnalysis"""
        analysis = CSVAnalysis(
            filename="test.csv",
            num_fields=3,
            headers=["A", "B", "C"],
            num_records=5,
            inconsistent_records=[(2, 2), (4, 4)],
        )

        output = str(analysis)
        assert "test.csv" in output
        assert "3" in output
        assert "5" in output
        assert "2" in output  # 2 record inconsistenti


class TestCSVController:
    """Test per la classe CSVController"""

    @pytest.fixture
    def temp_csv_folder(self, tmp_path):
        """Crea una cartella temporanea con file CSV di test"""
        # File 1: CSV con 3 campi, tutti i record corretti
        file1 = tmp_path / "file1.csv"
        with open(file1, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(["CAMPO_A", "CAMPO_B", "CAMPO_C"])
            writer.writerow(["val1", "val2", "val3"])
            writer.writerow(["val4", "val5", "val6"])

        # File 2: CSV con 5 campi (più lungo), tutti i record corretti
        file2 = tmp_path / "file2.csv"
        with open(file2, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(["CAMPO_A", "CAMPO_B", "CAMPO_C", "CAMPO_D", "CAMPO_E"])
            writer.writerow(["v1", "v2", "v3", "v4", "v5"])
            writer.writerow(["v6", "v7", "v8", "v9", "v10"])

        # File 3: CSV con 4 campi e un record più corto
        file3 = tmp_path / "file3.csv"
        with open(file3, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(["CAMPO_A", "CAMPO_B", "CAMPO_C", "CAMPO_D"])
            writer.writerow(["a1", "a2", "a3", "a4"])
            writer.writerow(["b1", "b2", "b3"])  # Record più corto
            writer.writerow(["c1", "c2", "c3", "c4"])

        return tmp_path

    def test_controller_initialization(self, temp_csv_folder):
        """Test inizializzazione CSVController"""
        controller = CSVController(str(temp_csv_folder))
        assert controller.folder_path == Path(temp_csv_folder)
        assert controller.delimiter == ";"
        assert controller.encoding == "utf-8"

    def test_controller_invalid_folder(self):
        """Test con cartella non esistente"""
        with pytest.raises(ValueError):
            CSVController("/path/non/esistente")

    def test_get_csv_files(self, temp_csv_folder):
        """Test ottenimento lista file CSV"""
        controller = CSVController(str(temp_csv_folder))
        csv_files = controller.get_csv_files()

        assert len(csv_files) == 3
        assert all(f.suffix == ".csv" for f in csv_files)

    def test_analyze_csv_file(self, temp_csv_folder):
        """Test analisi singolo file CSV"""
        controller = CSVController(str(temp_csv_folder))
        file_path = temp_csv_folder / "file1.csv"

        analysis = controller.analyze_csv_file(file_path)

        assert analysis.filename == "file1.csv"
        assert analysis.num_fields == 3
        assert len(analysis.headers) == 3
        assert analysis.num_records == 2
        assert len(analysis.inconsistent_records) == 0

    def test_analyze_csv_file_with_inconsistencies(self, temp_csv_folder):
        """Test analisi file con record inconsistenti"""
        controller = CSVController(str(temp_csv_folder))
        file_path = temp_csv_folder / "file3.csv"

        analysis = controller.analyze_csv_file(file_path)

        assert analysis.filename == "file3.csv"
        assert analysis.num_fields == 4
        assert len(analysis.inconsistent_records) == 1
        assert analysis.inconsistent_records[0][0] == 3  # riga 3
        assert analysis.inconsistent_records[0][1] == 3  # 3 campi invece di 4

    def test_analyze_all_files(self, temp_csv_folder):
        """Test analisi tutti i file"""
        controller = CSVController(str(temp_csv_folder))
        analyses = controller.analyze_all_files()

        assert len(analyses) == 3
        assert all(isinstance(a, CSVAnalysis) for a in analyses)

    def test_get_master_headers(self, temp_csv_folder):
        """Test ottenimento headers master (file con più campi)"""
        controller = CSVController(str(temp_csv_folder))
        master_headers = controller.get_master_headers()

        # file2.csv ha 5 campi, il massimo
        assert len(master_headers) == 5
        assert master_headers == ["CAMPO_A", "CAMPO_B", "CAMPO_C", "CAMPO_D", "CAMPO_E"]

    def test_fix_record_length_same_length(self, temp_csv_folder):
        """Test correzione record con lunghezza corretta"""
        controller = CSVController(str(temp_csv_folder))

        expected_headers = ["A", "B", "C"]
        current_headers = ["A", "B", "C"]
        row = ["1", "2", "3"]

        fixed_row = controller.fix_record_length(row, expected_headers, current_headers)
        assert fixed_row == row

    def test_fix_record_length_missing_fields(self, temp_csv_folder):
        """Test correzione record con campi mancanti"""
        controller = CSVController(str(temp_csv_folder))

        expected_headers = ["A", "B", "C", "D", "E"]
        current_headers = ["A", "B", "C"]
        row = ["1", "2", "3"]

        fixed_row = controller.fix_record_length(row, expected_headers, current_headers)

        assert len(fixed_row) == 5
        assert fixed_row[0] == "1"
        assert fixed_row[1] == "2"
        assert fixed_row[2] == "3"
        assert fixed_row[3] == ""  # Campo mancante
        assert fixed_row[4] == ""  # Campo mancante

    def test_fix_record_length_reordering(self, temp_csv_folder):
        """Test correzione con riordinamento campi"""
        controller = CSVController(str(temp_csv_folder))

        expected_headers = ["A", "B", "C", "D"]
        current_headers = ["B", "A", "D"]  # Ordine diverso
        row = ["val_B", "val_A", "val_D"]

        fixed_row = controller.fix_record_length(row, expected_headers, current_headers)

        assert len(fixed_row) == 4
        assert fixed_row[0] == "val_A"  # Riordinato
        assert fixed_row[1] == "val_B"  # Riordinato
        assert fixed_row[2] == ""  # Campo mancante
        assert fixed_row[3] == "val_D"

    def test_process_and_save(self, temp_csv_folder):
        """Test processamento e salvataggio file corretti"""
        controller = CSVController(str(temp_csv_folder))
        output_folder = temp_csv_folder / "output"

        output_files = controller.process_and_save(str(output_folder))

        # Verifica che tutti i file siano stati processati
        assert len(output_files) == 3

        # Verifica che i file esistano
        for output_path in output_files.values():
            assert Path(output_path).exists()

        # Verifica che i file abbiano tutti lo stesso numero di campi
        for output_path in output_files.values():
            with open(output_path, "r", encoding="utf-8") as f:
                reader = csv.reader(f, delimiter=";")
                headers = next(reader)
                assert len(headers) == 5  # Tutti devono avere 5 campi (dal file2.csv)

                # Verifica che tutti i record abbiano 5 campi
                for row in reader:
                    assert len(row) == 5

    def test_generate_report(self, temp_csv_folder):
        """Test generazione report"""
        controller = CSVController(str(temp_csv_folder))
        report = controller.generate_report()

        assert "REPORT ANALISI FILE CSV" in report
        assert str(temp_csv_folder) in report
        assert "file1.csv" in report
        assert "file2.csv" in report
        assert "file3.csv" in report
        assert "RIEPILOGO" in report


class TestIntegration:
    """Test di integrazione end-to-end"""

    def test_complete_workflow(self, tmp_path):
        """Test workflow completo: analisi, correzione, verifica"""
        # Crea file CSV con problemi diversi
        file1 = tmp_path / "data1.csv"
        with open(file1, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(["ID", "NOME", "COGNOME"])
            writer.writerow(["1", "Mario", "Rossi"])
            writer.writerow(["2", "Luca"])  # Campo mancante

        file2 = tmp_path / "data2.csv"
        with open(file2, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(["ID", "NOME", "COGNOME", "ETA", "CITTA"])
            writer.writerow(["3", "Anna", "Verdi", "30", "Roma"])
            writer.writerow(["4", "Paolo", "Bianchi", "25", "Milano"])

        # Inizializza controller
        controller = CSVController(str(tmp_path))

        # Analizza
        analyses = controller.analyze_all_files()
        assert len(analyses) == 2

        # Verifica inconsistenze
        file1_analysis = next(a for a in analyses if a.filename == "data1.csv")
        assert len(file1_analysis.inconsistent_records) == 1

        # Genera report
        report = controller.generate_report()
        assert "data1.csv" in report
        assert "data2.csv" in report

        # Processa e salva
        output_folder = tmp_path / "corrected"
        output_files = controller.process_and_save(str(output_folder))

        # Verifica file corretti
        assert len(output_files) == 2

        # Verifica contenuto file corretti
        corrected_file1 = output_folder / "data1.csv"
        with open(corrected_file1, "r", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=";")
            headers = next(reader)
            assert len(headers) == 5  # Deve avere 5 campi come file2

            row1 = next(reader)
            assert len(row1) == 5
            assert row1[0] == "1"
            assert row1[1] == "Mario"
            assert row1[2] == "Rossi"
            assert row1[3] == ""  # Campo aggiunto
            assert row1[4] == ""  # Campo aggiunto

            row2 = next(reader)
            assert len(row2) == 5
            assert row2[0] == "2"
            assert row2[1] == "Luca"
            assert row2[2] == ""  # Campo mancante corretto
