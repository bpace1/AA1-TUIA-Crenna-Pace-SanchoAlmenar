import streamlit as st
import pandas as pd
import requests
import io

API_URL = "http://api-clima:8000"

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
            

            response = requests.post(f'{API_URL}{endpoint}', files=files)
            
            if response.status_code == 200:
                predictions = response.json()["predictions"]
                
                df["Prediccion"] = predictions

                df = df[["Prediccion"]]
                                
                st.write("Datos con predicciones:")
                st.write(df.head())

                csv_buffer = io.StringIO()
                df.to_csv(csv_buffer, index=False)
                csv_data = csv_buffer.getvalue()

                st.download_button(
                    label="Descargar CSV con predicciones",
                    data=csv_data,
                    file_name="predicciones.csv",
                    mime="text/csv"
                )
            else:
                st.error(f"Error: {response.json()['detail']}")
        except Exception as e:
            st.error(f"Ocurrió un error: {e}")
