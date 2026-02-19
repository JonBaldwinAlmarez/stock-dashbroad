import pandas as pd

def to_dataframe(historical_data: list):
    """Convert API historical data to DataFrame"""
    df = pd.DataFrame(historical_data) # Create a DataFrame from the historical data list
    if not df.empty:
        df["t"] = dp.to_datetime(df["t"], unit="s") # Convert the timestamp column to datetime format
        df.set_index("t", inplace=True) # Set the timestamp column as the index of the DataFrame
        df.sort_index(inplace=True) # Sort the DataFrame by the index (timestamp)
    return df

def calculate_moving_average(df, window = 5):
    """Adding moving average column to the DataFrame"""
    if not df.empty and "c" in df.columns:
        df[f"MA_{window}"] = df["c"].rolling(window=window).mean()
        return df