import pandas as pd


def join_tables(passy_data, domus_data):
    # **Import Pandas and Create Sample DataFrames**: First, let's set up the environment and create some sample data to work with.
    passy_df = pd.DataFrame(passy_data)
    domus_df = pd.DataFrame(domus_data)

    # --- Important: Convert date columns to datetime objects ---
    passy_df["event_date"] = pd.to_datetime(passy_df["event_date"])
    domus_df["start_date"] = pd.to_datetime(domus_df["start_date"])
    domus_df["end_date"] = pd.to_datetime(domus_df["end_date"])

    # 2 **Merge the DataFrames on `room_key`**:
    # Use the `pd.merge()` function to perform an inner join on the `room_key`.
    # This will match all `passy` events with all `domus` intervals for the same room.
    merged_df = pd.merge(passy_df, domus_df, on="room_key", how="inner")

    # merged_df = pd.merge(passy_df, domus_df, on='room_key')

    print("--- After Merging on room_key ---")
    print(merged_df)

    """
    The `merged_df` will contain rows that may not yet satisfy the date condition. 
    For room 'A', the event on `2023-02-10` will be incorrectly matched with the interval in January.
    """

    # 3 **Filter the Merged DataFrame**: Now, apply a boolean filter to keep only the rows where the `event_date` is between the `start_date` and `end_date`.

    # Apply the date range condition
    condition = (merged_df["event_date"] >= merged_df["start_date"]) & (
        merged_df["event_date"] <= merged_df["end_date"]
    )

    # Apply the filter to get the final result
    final_df = merged_df[condition]

    print("\n--- Final Joined Table ---")
    print(final_df)

    # **Expected Output:**
    """
    --- Final Joined Table ---
    room_key event_date start_date   end_date
    0        A 2023-01-15 2023-01-01 2023-01-31
    3        C 2023-04-05 2023-04-01 2023-04-30
    """
