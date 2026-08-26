import pandas as pd


def load_and_merge_data(gen_path, weather_path):

    gen = pd.read_csv(gen_path)
    weather = pd.read_csv(weather_path)

    gen["DATE_TIME"] = pd.to_datetime(gen["DATE_TIME"], dayfirst=True)
    weather["DATE_TIME"] = pd.to_datetime(weather["DATE_TIME"], dayfirst=True)

    gen = gen.sort_values("DATE_TIME")
    weather = weather.sort_values("DATE_TIME")

    df = pd.merge_asof(
        gen,
        weather,
        on="DATE_TIME",
        direction="nearest"
    )

    return df