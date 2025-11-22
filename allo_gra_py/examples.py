"""
Esempi di utilizzo avanzato del modulo csv_control

Questo script mostra vari modi di utilizzare il CSVController
per casi d'uso specifici.
"""

from pathlib import Path
from src.csv_control import CSVController


def esempio_base():
    """Esempio base: analisi e correzione"""
    print("=" * 70)
    print("ESEMPIO 1: Utilizzo Base")
    print("=" * 70)

    controller = CSVController("data")

    # Analizza i file
    analyses = controller.analyze_all_files()

    print(f"\nFile analizzati: {len(analyses)}")
    for analysis in analyses:
        print(f"\n{analysis}")

    # Genera report
    report = controller.generate_report()
    print(report)

    # Processa e salva
    output_files = controller.process_and_save()

    print("\nFile corretti generati:")
    for orig, out in output_files.items():
        print(f"  {orig} -> {out}")


def esempio_encoding_personalizzato():
    """Esempio: gestione encoding diverso"""
    print("\n" + "=" * 70)
    print("ESEMPIO 2: Encoding Personalizzato")
    print("=" * 70)

    # Per file con encoding latin-1 o cp1252
    controller = CSVController(
        "data",
        delimiter=";",
        encoding="utf-8",  # Cambia in 'latin-1' o 'cp1252' se necessario
    )

    print("\nConfigurazione:")
    print(f"  Folder:    {controller.folder_path}")
    print(f"  Delimiter: {controller.delimiter}")
    print(f"  Encoding:  {controller.encoding}")


def esempio_output_personalizzato():
    """Esempio: cartella output personalizzata"""
    print("\n" + "=" * 70)
    print("ESEMPIO 3: Output Personalizzato")
    print("=" * 70)

    controller = CSVController("data")

    # Salva in una cartella specifica
    output_folder = Path("output_corretti_2025")
    output_folder.mkdir(exist_ok=True)

    output_files = controller.process_and_save(str(output_folder))

    print(f"\nFile salvati in: {output_folder.absolute()}")
    print(f"Numero file:     {len(output_files)}")


def esempio_analisi_dettagliata():
    """Esempio: analisi dettagliata di ogni file"""
    print("\n" + "=" * 70)
    print("ESEMPIO 4: Analisi Dettagliata")
    print("=" * 70)

    controller = CSVController("data")

    csv_files = controller.get_csv_files()

    for csv_file in csv_files:
        analysis = controller.analyze_csv_file(csv_file)

        print(f"\n--- {analysis.filename} ---")
        print(f"Campi:    {analysis.num_fields}")
        print(f"Records:  {analysis.num_records}")
        print(f"Headers (primi 5): {', '.join(analysis.headers[:5])}")

        if analysis.inconsistent_records:
            print(f"\nRecord inconsistenti: {len(analysis.inconsistent_records)}")
            for row_num, num_fields in analysis.inconsistent_records[:3]:
                print(
                    f"  - Riga {row_num}: {num_fields} campi invece di {analysis.num_fields}"
                )
        else:
            print("Tutti i record sono consistenti ✓")


def esempio_verifica_headers():
    """Esempio: verifica headers tra file diversi"""
    print("\n" + "=" * 70)
    print("ESEMPIO 5: Verifica Headers")
    print("=" * 70)

    controller = CSVController("data")
    controller.analyze_all_files()

    # Ottieni master headers
    master_headers = controller.get_master_headers()

    print(f"\nMaster Headers ({len(master_headers)} campi):")
    print(f"Primi 10: {', '.join(master_headers[:10])}")
    print(f"Ultimi 5: {', '.join(master_headers[-5:])}")

    # Verifica differenze per ogni file
    print("\nDifferenze per file:")
    for analysis in controller.analyses:
        missing_headers = set(master_headers) - set(analysis.headers)
        if missing_headers:
            print(f"\n{analysis.filename}:")
            print(f"  Campi mancanti: {len(missing_headers)}")
            if len(missing_headers) <= 10:
                print(f"  Lista: {', '.join(sorted(missing_headers))}")
        else:
            print(f"{analysis.filename}: nessuna differenza ✓")


def esempio_report_su_file():
    """Esempio: salva report su file"""
    print("\n" + "=" * 70)
    print("ESEMPIO 6: Salva Report su File")
    print("=" * 70)

    controller = CSVController("data")
    report = controller.generate_report()

    report_file = Path("output/report_analisi.txt")
    report_file.parent.mkdir(exist_ok=True)

    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\nReport salvato in: {report_file.absolute()}")
    print(f"Dimensione: {report_file.stat().st_size} bytes")


def esempio_confronto_pre_post():
    """Esempio: confronta file prima e dopo la correzione"""
    print("\n" + "=" * 70)
    print("ESEMPIO 7: Confronto Pre/Post Correzione")
    print("=" * 70)

    controller = CSVController("data")

    # Analizza prima della correzione
    analyses_pre = controller.analyze_all_files()

    # Processa
    output_files = controller.process_and_save()

    # Analizza dopo la correzione
    controller_post = CSVController("output")
    analyses_post = controller_post.analyze_all_files()

    print("\nConfronto Pre/Post:")
    print(
        f"{'File':<40} {'Pre-Campi':<12} {'Post-Campi':<12} {'Pre-Inc':<10} {'Post-Inc':<10}"
    )
    print("-" * 90)

    for pre, post in zip(analyses_pre, analyses_post):
        print(
            f"{pre.filename:<40} {pre.num_fields:<12} {post.num_fields:<12} "
            f"{len(pre.inconsistent_records):<10} {len(post.inconsistent_records):<10}"
        )


def esempio_workflow_completo():
    """Esempio: workflow completo end-to-end"""
    print("\n" + "=" * 70)
    print("ESEMPIO 8: Workflow Completo")
    print("=" * 70)

    # 1. Setup
    print("\n1. Setup controller...")
    controller = CSVController("data", delimiter=";", encoding="utf-8")

    # 2. Analisi
    print("2. Analisi file CSV...")
    csv_files = controller.get_csv_files()
    print(f"   Trovati {len(csv_files)} file CSV")

    # 3. Analisi dettagliata
    print("3. Analisi dettagliata...")
    analyses = controller.analyze_all_files()

    problemi_trovati = sum(1 for a in analyses if a.inconsistent_records)
    print(f"   File con problemi: {problemi_trovati}/{len(analyses)}")

    # 4. Report
    print("4. Generazione report...")
    report = controller.generate_report()

    # Salva report
    report_file = Path("output/workflow_report.txt")
    report_file.parent.mkdir(exist_ok=True)
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"   Report salvato: {report_file}")

    # 5. Correzione
    print("5. Correzione e salvataggio...")
    output_files = controller.process_and_save("output")
    print(f"   File corretti: {len(output_files)}")

    # 6. Verifica
    print("6. Verifica post-correzione...")
    controller_verify = CSVController("output")
    analyses_verify = controller_verify.analyze_all_files()

    problemi_post = sum(1 for a in analyses_verify if a.inconsistent_records)
    print(f"   File con problemi dopo correzione: {problemi_post}")

    # 7. Riepilogo
    print("\n" + "=" * 70)
    print("RIEPILOGO WORKFLOW")
    print("=" * 70)
    print(f"File processati:        {len(csv_files)}")
    print(f"Problemi pre-correzione: {problemi_trovati}")
    print(f"Problemi post-correzione: {problemi_post}")
    print(f"Report generato:        {report_file}")
    print(f"Output folder:          output/")
    print("\n✓ Workflow completato con successo!")


if __name__ == "__main__":
    # Esegui tutti gli esempi
    print("\n")
    print("=" * 70)
    print(" " * 15 + "CSV CONTROL - ESEMPI AVANZATI")
    print("=" * 70)

    try:
        esempio_base()
        esempio_encoding_personalizzato()
        esempio_output_personalizzato()
        esempio_analisi_dettagliata()
        esempio_verifica_headers()
        esempio_report_su_file()
        esempio_confronto_pre_post()
        esempio_workflow_completo()

        print("\n" + "=" * 70)
        print("Tutti gli esempi eseguiti con successo! ✓")
        print("=" * 70)

    except Exception as e:
        print(f"\nERRORE: {e}")
        import traceback

        traceback.print_exc()
