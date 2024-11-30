import pandas as pd
import pickle
import numpy as np
import math
from fastapi import FastAPI, UploadFile, HTTPException
from io import StringIO
from sklearn.impute import KNNImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

app = FastAPI()

logistic_model_path = "models/logistic_regression_model.pkl"
nn_model_path = "models/model_nn.h5"

try:
    with open(logistic_model_path, "rb") as f:
        logistic_model = pickle.load(f)
except FileNotFoundError:
    raise Exception(f"Modelo no encontrado en {logistic_model_path}")

try:
    with open(nn_model_path, "rb") as f:
        nn_model = pickle.load(f)
except FileNotFoundError:
    raise Exception(f"Modelo no encontrado en {nn_model_path}")

def angle_to_xy(angle: float):
    """
    Función que recibe la dirección del viento en grados y la transformará en projecciones sobre el eje x e y,
    obteniendo así dos valores numéricos por cada columna.
    """
    if math.isnan(angle):
        return (np.nan, np.nan)

    # Convertimos el ángulo a radianes
    angle_rad = math.radians(angle)

    x = math.sin(angle_rad)
    y = math.cos(angle_rad)

    return (x, y)

def reimpute_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Reemplaza los valores atípicos en el DataFrame con la mediana de la columna.
    """
    for column in df.columns:
        if column == 'RainToday':
            continue

        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1

        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        median_value = df[column].median()

        df[column] = df[column].where((df[column] >= lower_bound) & (df[column] <= upper_bound), median_value)

    return df

def preprocess_for_prediction(file: UploadFile):
    try:
        # Cargar el archivo CSV
        print(1)
        content = file.file.read().decode("utf-8")
        df = pd.read_csv(StringIO(content))
        print(2)
        # Preprocesamiento de la columna 'Date'
        df = df.reset_index(drop=True)
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df['Year'] = df['Date'].dt.year
        df['Day'] = df['Date'].dt.dayofyear
        df.drop(columns='Date', inplace=True)

        # Mapeo de direcciones de viento a grados
        direction_angles = {
            'N': 0, 'NNE': 22.5, 'NE': 45, 'ENE': 67.5, 'E': 90, 'ESE': 112.5,
            'SE': 135, 'SSE': 157.5, 'S': 180, 'SSW': 202.5, 'SW': 225, 'WSW': 247.5,
            'W': 270, 'WNW': 292.5, 'NW': 315, 'NNW': 337.5
        }
        print(3)
        columnas_viento = ['WindDir3pm', 'WindDir9am', 'WindGustDir']
        for columna in columnas_viento:
            df[columna] = df[columna].map(direction_angles)

        # Aplicar la función de proyecciones de viento
        df[['WindDir3pm_x', 'WindDir3pm_y']] = df['WindDir3pm'].apply(lambda angle: pd.Series(angle_to_xy(angle)))
        df[['WindDir9am_x', 'WindDir9am_y']] = df['WindDir9am'].apply(lambda angle: pd.Series(angle_to_xy(angle)))
        df[['WindGustDir_x', 'WindGustDir_y']] = df['WindGustDir'].apply(lambda angle: pd.Series(angle_to_xy(angle)))
        
        df.drop(columns=columnas_viento, inplace=True)
        print(4)
        # Mapeo de RainToday y RainTomorrow
        df['RainToday'] = df['RainToday'].map({'Yes': 1, 'No': 0})

        # Añadir coordenadas de las ciudades
        chosen_cities_coordinates = {
            "Newcastle": {"latitude": -32.9282, "longitude": 151.7817},
            "BadgerysCreek": {"latitude": -33.8836, "longitude": 150.7386},
            "Penrith": {"latitude": -33.7532, "longitude": 150.6880},
            "Perth": {"latitude": -31.9505, "longitude": 115.8605},
            "Canberra": {"latitude": -35.2809, "longitude": 149.1300},
            "Wollongong": {"latitude": -34.4278, "longitude": 150.8931},
            "Nuriootpa": {"latitude": -34.4658, "longitude": 138.9784},
            "NorahHead": {"latitude": -33.2886, "longitude": 151.6154},
            "NorfolkIsland": {"latitude": -29.0408, "longitude": 167.9547},
            "MountGinini": {"latitude": -35.4622, "longitude": 148.9525}
        }
        coords_df = pd.DataFrame.from_dict(chosen_cities_coordinates, orient='index')
        coords_df.reset_index(inplace=True)
        coords_df.rename(columns={'index': 'Location'}, inplace=True)
        df = df.merge(coords_df, on='Location', how='left')
        df.drop(columns=['Location'], inplace=True)

        print(5)
        # Imputación de valores faltantes con KNN
        print(6)
        # Normalización de las características
        scaler = StandardScaler()
        df_normalized = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)

        # Codificación OneHot para la columna 'Year'
        encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False).set_output(transform='pandas')
        df_year_enc = encoder.fit_transform(df[['Year']].astype(np.int32))
        print(7)
        # Concatenar las características normalizadas con las codificadas
        df_normalized = pd.concat([df_normalized, df_year_enc], axis=1)
        
        # Devolver el DataFrame procesado para predicción
        
        features = [f'Year_{i}' for i in range(2007, 2018)]
        
        df_normalized.drop(columns='Year', inplace=True)
        curr_year = ''
        
        for i in features:
            if i in df_normalized.columns:
                curr_year = i
                df_normalized.drop(columns=i, inplace=True)
            
        for i in features:
            if i != curr_year:
                print(i)
                df_normalized[i] = 0
                continue
            print(i)
            df_normalized[i] = 1    
                

        return df_normalized.fillna(0)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/predict/logistic_regression")
async def predict_logistic_regression(file: UploadFile):
    df = preprocess_for_prediction(file)
    
    predictions = logistic_model.predict(df)
    
    print(predictions)
    
    return {"predictions": ['Yes' if x == 0 else 'No' for x in predictions.tolist()]}

@app.post("/predict/nn")
async def predict_nn(file: UploadFile):
    df = preprocess_for_prediction(file)
    
    predictions = nn_model.predict(df)
    
    return {"predictions": ['Yes' if x == 0 else 'No' for x in predictions.tolist()]}  