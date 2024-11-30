Para ejecutar el dashboard:

```sh
  cd App
  docker build -t app-climate .
  docker run -d -p 8501:8501 --restart always app-climate 
``` 