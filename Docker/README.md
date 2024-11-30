Para ejecutar el Docker con el archivo inferencia.py mediante la api ejecutar:

```sh
  cd Docker
  docker build -t api-clima .
  docker network create clima-network
  docker run -d -p 8000:8000 --restart always api-clima
``` 