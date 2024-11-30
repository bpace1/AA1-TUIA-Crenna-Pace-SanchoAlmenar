Para ejecutar el dashboard:

```sh
  cd App
  docker build -t dashboard-clima . 
  docker run -d -p 8501:8501 --network clima-network --name  dashboard-clima --restart always  dashboard-clima
``` 