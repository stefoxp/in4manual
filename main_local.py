# from library import pandas_join_tables
from library import pandas_days_for_month

if __name__ == "__main__":
    file = "data/allo_assegnazioni_dal20240901_aa_2024-25.csv"
    FILE_OUT = "data/assegnazioni_calc.csv"
    result = pandas_days_for_month.main(file, FILE_OUT)
    """
    # Sample passy table data
    passy_data = {
        "room_key": ["A", "A", "B", "C"],
        "event_date": ["2023-01-15", "2023-02-10", "2023-03-20", "2023-04-05"],
    }
    domus_data = {
        "room_key": ["A", "A", "B", "C"],
        "start_date": ["2023-01-01", "2023-03-01", "2023-03-01", "2023-04-01"],
        "end_date": ["2023-01-31", "2023-03-31", "2023-03-15", "2023-04-30"],
    }

    final_df_actual = pandas_join_tables.join_tables(passy_data, domus_data)
    """
