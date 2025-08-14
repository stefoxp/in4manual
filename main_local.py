from library import pandas_join_tables

if __name__ == "__main__":
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
    pandas_join_tables.join_tables(passy_data, domus_data)
