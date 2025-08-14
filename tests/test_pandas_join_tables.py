from library import pandas_join_tables
import pandas as pd


def test_join_tables():
    passy_data = {
        "room_key": ["A", "A", "B", "C"],
        "event_date": ["2023-01-15", "2023-02-10", "2023-03-20", "2023-04-05"],
    }
    domus_data = {
        "room_key": ["A", "A", "B", "C"],
        "start_date": ["2023-01-01", "2023-03-01", "2023-03-01", "2023-04-01"],
        "end_date": ["2023-01-31", "2023-03-31", "2023-03-15", "2023-04-30"],
    }
    final_data = {
        "room_key": ["A", "C"],
        "event_date": ["2023-01-15", "2023-04-05"],
        "start_date": ["2023-01-01", "2023-04-01"],
        "end_date": ["2023-01-31", "2023-04-30"],
    }
    final_df_actual = pandas_join_tables.join_tables(passy_data, domus_data)
    final_df_expected = pd.DataFrame(final_data)

    final_df_expected["event_date"] = pd.to_datetime(final_df_expected["event_date"])
    final_df_expected["start_date"] = pd.to_datetime(final_df_expected["start_date"])
    final_df_expected["end_date"] = pd.to_datetime(final_df_expected["end_date"])

    final_df_expected.index = [0, 5]

    assert final_df_actual.equals(final_df_expected)
