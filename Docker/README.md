Para ejecutar el Docker con el archivo inferencia.py mediante la api ejecutar:

```sh
  cd Docker
  docker build -t fastapi-models .
  docker run -d -p 8000:8000 --restart always fastapi-models
``` 