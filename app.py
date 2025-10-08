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
    model = joblib.load("best_model.pkl")
except FileNotFoundError:
    st.error("Model file not found. Make sure 'best_model.pkl' is in the root of the repository.")
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
    cement = st.sidebar.slider('Cement (kg in a m³ mix)', 102.0, 540.0, 320.0, 1.0)
    slag = st.sidebar.slider('Blast Furnace Slag (kg in a m³ mix)', 0.0, 359.4, 120.0, 1.0)
    fly_ash = st.sidebar.slider('Fly Ash (kg in a m³ mix)', 0.0, 200.1, 50.0, 1.0)
    water = st.sidebar.slider('Water (kg in a m³ mix)', 121.8, 247.0, 180.0, 1.0)
    superplasticizer = st.sidebar.slider('Superplasticizer (kg in a m³ mix)', 0.0, 32.2, 6.0, 0.1)
    coarse_agg = st.sidebar.slider('Coarse Aggregate (kg in a m³ mix)', 801.0, 1145.0, 970.0, 1.0)
    fine_agg = st.sidebar.slider('Fine Aggregate (kg in a m³ mix)', 594.0, 992.6, 770.0, 1.0)
    age = st.sidebar.slider('Age (days)', 1, 365, 28, 1)

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
