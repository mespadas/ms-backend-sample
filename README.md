# Introduction 
Microservicio Demo en Python y Flask, con BD local

# Run

 pip freeze > requirements.txt //actualizar el archivo de librerias
 python hello_api.py //correr localmente
 
 # Contenerizar
 docker build -t mspythonservice -f Dockerfile .
 docker run -p 5000:5000 --name mspythonservice mspythonservice:latest
