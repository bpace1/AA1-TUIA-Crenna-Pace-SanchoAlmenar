## Trabajos Prácticos: Aprendizaje Automático 1.
### Tec. Universitaria en Inteligencia Artificial - FCEIA (UNR)

### Alumnos: 
- Crenna, Giuliano. Legajo: C-7438/1.
- Pace, Bruno Emmanuel. Legajo: P-5295/7.
- Sancho Almenar, Mariano. Legajo: S-5778/9.

### Descripción:

Trabajos prácticos de aprendizaje automático 1. Se abordan los siguientes temas:
- Pre-procesado de datos.
- Modelos de regresión lineal.
- Modelos de regresión logística.
- Redes Neuronales.
- Exportado de modelo y entorno en Docker para la puesta en producción.
- Creación de API con FAStAPI.
- Dashboard en streamlit.

### Pre-requisitos:
- Python 3.10.
- Docker.


### Ejecución:

1. Clonar el repositorio y abrir la carpeta.

```sh
git clone https://github.com/bpace1/AA1-TUIA-Crenna-Pace-SanchoAlmenar.git
cd AA1-TUIA-Crenna-Pace-SanchoAlmenar

```

### En windows:


2. En cmd ejecutar:

```sh
  python -m venv .venv
  .venv\Scripts\activate
  pip install -r requirements.txt
```


#### En linux:

2. En terminal ejecutar:

```sh
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
```


3. Abrir los notebooks y ejecutar los códigos.

4. Para ejecutar el docker con el archivo inferencia.py mediante la api, volver a la raíz del proyecto y ejecutar:

```sh
  cd Docker
  docker build -t fastapi-models .
  docker run -d -p 8000:8000 --restart always fastapi-models
```

5. Para ejecutar el dashboard, volver a la raíz del proyecto y ejecutar:

```sh
  cd App
  docker build -t app-climate .
  docker run -d -p 8501:8501 --restart always app-climate 
  streamlit run main.py --server.port=8501 --server.address=0.0.0.0
```

Ingresar a la aplicación en [Dashboard app](http://localhost:8501/)

Si desea probar la api, ingrese en [API swagger](http://localhost:8000/docs)

Tenemos un dashboard con el modelo corriendo en [Dashboard en línea](https://clima.terralytics.com.ar/)


  