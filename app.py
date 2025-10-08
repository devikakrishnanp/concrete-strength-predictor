import streamlit as st
import pandas as pd
import joblib

# --- Page Configuration ---
st.set_page_config(
    page_title="Concrete Strength Predictor",
    page_icon="🧱",
    layout="wide"
)

# --- Load the Trained Model ---
try:
    model = joblib.load("best_model (1).pkl")
except FileNotFoundError:
    st.error("Model file not found. Make sure 'best_model (1).pkl' is in the root of the repository.")
    st.stop()

# --- App Title and Description ---
st.title("🧱 Concrete Compressive Strength Predictor")
st.write(
    "This app predicts the compressive strength of concrete in Megapascals (MPa) "
    "based on its components. Adjust the sliders in the sidebar to match your concrete mix design."
)

# --- Sidebar for User Inputs ---
st.sidebar.header("Input Concrete Components")

def user_input_features():
    cement = st.sidebar.number_input('Cement (kg in a m³ mix)', min_value=0.0, max_value=800.0, value=320.0, step=0.1)
    slag = st.sidebar.number_input('Blast Furnace Slag (kg in a m³ mix)', min_value=0.0, max_value=800.0, value=120.0, step=0.1)
    fly_ash = st.sidebar.number_input('Fly Ash (kg in a m³ mix)', min_value=0.0, max_value=300.0, value=50.0, step=0.1)
    water = st.sidebar.number_input('Water (kg in a m³ mix)', min_value=0.0, max_value=400.0, value=180.0, step=0.1)
    superplasticizer = st.sidebar.number_input('Superplasticizer (kg in a m³ mix)', min_value=0.0, max_value=50.0, value=6.0, step=0.1)
    coarse_agg = st.sidebar.number_input('Coarse Aggregate (kg in a m³ mix)', min_value=0.0, max_value=1200.0, value=970.0, step=0.1)
    fine_agg = st.sidebar.number_input('Fine Aggregate (kg in a m³ mix)', min_value=0.0, max_value=1200.0, value=770.0, step=0.1)
    age = st.sidebar.number_input('Age (days)', min_value=1, max_value=365, value=28, step=1)


    data = {
        'cement': cement,
        'slag': slag,
        'fly_ash': fly_ash,
        'water': water,
        'superplasticizer': superplasticizer,
        'coarse_agg': coarse_agg,
        'fine_agg': fine_agg,
        'age': age
    }
    features = pd.DataFrame(data, index=[0])
    return features

input_df = user_input_features()

# --- Main Panel for Displaying Inputs and Prediction ---
st.subheader("Your Input Parameters")
st.dataframe(input_df, use_container_width=True)

if st.button('**Predict Compressive Strength**', use_container_width=True):
    prediction = model.predict(input_df)
    predicted_strength = round(prediction[0], 2)

    st.subheader("Predicted Strength")
    st.markdown(
        f"""
        <div style="background-color:#2E8B57; padding:15px; border-radius:10px;">
        <h2 style="color:white; text-align:center;">
        {predicted_strength} MPa
        </h2>
        </div>
        """,
        unsafe_allow_html=True
    )
