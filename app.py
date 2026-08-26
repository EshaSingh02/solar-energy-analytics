from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent
RESULTS_DIR = PROJECT_ROOT / "results"
MODEL_PATH = RESULTS_DIR / "solar_power_model.pkl"
PREDICTION_RESULTS_PATH = RESULTS_DIR / "solar_prediction_results.csv"

st.set_page_config(
    page_title="Solar Energy Analytics Dashboard",
    layout="wide",
)

st.title("☀️ Solar Energy Analytics & Predictive Maintenance Dashboard")
st.markdown("---")
st.write("This dashboard analyzes solar PV performance and predicts power output.")

# Load model only when it is available.
model = None
if MODEL_PATH.exists():
    model = joblib.load(MODEL_PATH)
else:
    st.warning(
        "Trained model not found. Run the analysis notebook to train and save "
        "the model before using the prediction features."
    )

# Load prediction results when available.
if PREDICTION_RESULTS_PATH.exists():
    df = pd.read_csv(PREDICTION_RESULTS_PATH)

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    st.subheader("Dataset Statistics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Records", len(df))
    if "AC_POWER" in df.columns:
        col2.metric("Average AC Power", f"{df['AC_POWER'].mean():.2f}")
        col3.metric("Max AC Power", f"{df['AC_POWER'].max():.2f}")
else:
    df = None
    st.info(
        "Prediction results are not included in the repository by default. "
        "Run the notebook to generate them."
    )

st.sidebar.title("Enter Weather Inputs")
irradiation = st.sidebar.slider("Irradiation", 0.0, 1.5, 0.8)
module_temp = st.sidebar.slider("Module Temperature", 0.0, 80.0, 35.0)
ambient_temp = st.sidebar.slider("Ambient Temperature", 0.0, 50.0, 25.0)
hour = st.sidebar.slider("Hour of Day", 0, 23, 12)
day = st.sidebar.slider("Day of Month", 1, 31, 15)
month = st.sidebar.slider("Month", 1, 12, 6)

if model is not None:
    # The final Random Forest model is trained with six features:
    # irradiation, ambient temperature, module temperature, hour, day, month.
    input_data = np.array(
        [[irradiation, ambient_temp, module_temp, hour, day, month]]
    )
    predicted_power = model.predict(input_data)[0]

    st.subheader("Predicted Solar Power Output")
    st.metric("Predicted AC Power", f"{predicted_power:.2f}")

    st.subheader("System Performance Overview")
    expected_power = irradiation * 1000
    efficiency = (predicted_power / (expected_power + 1)) * 100

    col1, col2, col3 = st.columns(3)
    col1.metric("Predicted AC Power", f"{predicted_power:.2f} kW")
    col2.metric("Expected Power", f"{expected_power:.2f} kW")
    col3.metric("System Efficiency", f"{efficiency:.2f}%")

    st.subheader("Panel Maintenance Status")
    if efficiency < 75 and irradiation > 0.6:
        st.error("⚠️ Panel Cleaning Recommended")
    elif irradiation < 0.2:
        st.info("☁ Low solar irradiance detected")
    else:
        st.success("✅ Panels Operating Normally")

    st.subheader("Daily Power Prediction Curve")
    hours = list(range(24))
    predictions = []
    for h in hours:
        row = np.array(
            [[irradiation, ambient_temp, module_temp, h, day, month]]
        )
        predictions.append(model.predict(row)[0])

    prediction_df = pd.DataFrame(
        {"Hour": hours, "Predicted Power": predictions}
    )
    st.line_chart(prediction_df.set_index("Hour"), height=400)

st.subheader("Model Analysis Plots")
plots = [
    "actual_vs_predicted_power.png",
    "irradiation_vs_power.png",
    "module_temperature_vs_power.png",
    "feature_importance.png",
]

for plot in plots:
    path = RESULTS_DIR / plot
    if path.exists():
        st.image(path, caption=plot.replace("_", " ").title())
