## Trabajos Prácticos: Aprendizaje Automático 1.
### Tec. Universitaria en Inteligencia Artificial - FCEIA (UNR)

Trabajo de regresión: estimador de precios de casas.

Trabajo de clasificación: estimador de días lluviosos de 10 ciudades.


### Alumnos: 
- Crenna, Giuliano. 
- Pace, Bruno Emmanuel. 
- Sancho Almenar, Mariano.

### Descripción:

Trabajos prácticos de aprendizaje automático 1. Se abordan los siguientes temas:
- Pre-procesado de datos.
- Modelos de regresión lineal.
- Modelos Lasso, Ridge y Elastic Net.
- Gradiente Descendiente, Batch y mini-batch.
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


### En linux:

2. En terminal ejecutar:

```sh
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
```


3. Abrir los notebooks y ejecutar los códigos.

4. Para ejecutar el docker con el archivo inferencia.py mediante la api y el dashboard, volver a la raíz del proyecto y ejecutar:

### En windows:

```sh
  deploy.cmd
```

### En linux:

```sh
  sudo bash deploy.sh
 ```


Ingresar a la aplicación en [Dashboard App](http://localhost:8501/)

Si desea probar la api, ingrese en [API Swagger](http://localhost:8000/docs)

Tenemos un dashboard con el modelo corriendo en [Dashboard en línea](https://clima.terralytics.com.ar/)

En caso de querer eliminar la imagen de la api y el dashboard, ejecutar:

### En windows:

```sh
  clean_docker.cmd
```

### En linux:

```sh
  sudo bash clean_docker.sh
 ```
