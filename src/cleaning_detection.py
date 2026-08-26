def detect_cleaning(df):

    df["EFFICIENCY_RATIO"] = df["AC_POWER"] / df["PREDICTED_POWER"]
    df["EFFICIENCY_RATIO"] = df["EFFICIENCY_RATIO"].fillna(0)

    df["CLEANING_REQUIRED"] = (
        (df["IRRADIATION"] > 0.6) &
        (df["EFFICIENCY_RATIO"] < 0.75)
    )

    df["CLEANING_STATUS"] = df["CLEANING_REQUIRED"].map({
        True: "Cleaning Required",
        False: "System OK"
    })

    return df