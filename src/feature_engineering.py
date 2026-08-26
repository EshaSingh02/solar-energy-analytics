import pandas as pd

def create_time_features(df):

    df["DATE_TIME"] = pd.to_datetime(df["DATE_TIME"])

    df["hour"] = df["DATE_TIME"].dt.hour
    df["day"] = df["DATE_TIME"].dt.day
    df["month"] = df["DATE_TIME"].dt.month
    df["minute"] = df["DATE_TIME"].dt.minute

    return df