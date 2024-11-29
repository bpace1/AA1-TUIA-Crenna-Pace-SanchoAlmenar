import streamlit as st
import pandas as pd
import requests

API_URL = "http://localhost:8080"

st.set_page_config(page_title="Predictor Clima",
                   page_icon=':mostly_sunny:')

st.title("Predicciones del Clima")

st.sidebar.header("Subir archivo")
uploaded_file = st.sidebar.file_uploader(
    "Cargar un archivo CSV para realizar predicciones",
    type=["csv"]
)

model_type = st.sidebar.selectbox(
    "Seleccionar modelo de predicción",
    options=["Logistic Regression", "Neural Network"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("Datos cargados:")
    st.write(df.head())

    if st.button("Realizar predicción"):
        try:
            files = {"file": ("uploaded_file.csv", uploaded_file.getvalue())}
            
            if model_type == "Logistic Regression":
                endpoint = "/predict/logistic_regression"
            else:
                endpoint = "/predict/nn"
            
            response = requests.post(f"{API_URL}{endpoint}", files=files)
            
            if response.status_code == 200:
                predictions = response.json()["predictions"]
                st.write("Predicciones:")
                st.write(predictions)
            else:
                st.error(f"Error: {response.json()['detail']}")
        except Exception as e:
            st.error(f"Ocurrió un error: {e}")