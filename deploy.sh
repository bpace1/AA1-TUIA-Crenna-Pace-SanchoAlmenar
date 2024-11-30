#!/bin/bash

cd Docker

docker build -t api-clima .

docker run -d -p 8000:8000 --network clima-network --name  api-clima --restart always  api-clima

cd ..

cd App

docker build -t dashboard-clima . 

docker run -d -p 8501:8501 --network clima-network --name  dashboard-clima --restart always  dashboard-clima
