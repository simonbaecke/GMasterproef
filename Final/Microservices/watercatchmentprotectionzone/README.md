# Microservices Flask Template
## Installation
To install this Microservices Template, make sure Python 3.9 or higher is installed on your device. Installing the Microservice Template can be done by first starting a Python virtual environment and then installing the dependencies stored in the [pyproject.toml](https://github.com/stelemme/template-microservice-py/blob/main/pyproject.toml) file. The virtual environment is activated using the following commands.
```
python -m venv .venv
.venv\Scripts\activate
```
The Microservices Template can now be installed using the following command.
```
pip install -e .
```
## Running the Microservice
To run the Microservices, a virtual environment needs to be activated using the following command.
```
.venv\Scripts\activate
```
After the virtual environment is activated the Microservices can be run using the following command. Additional arguments can be added to the command to for example run the Microservice in debug mode (--debug), which enables live reloading. The port on which the Microservice runs can also be changed with an additional argument (--port <port-number>).
```
flask --app flaskr run
```
## Dockerizing the Microservice
To Dockerize the Microservice, make sure Docker is installed. The Microservice can be built into a Docker Image using the following command.
```
docker build -t <image-name> .
```
To run the Docker image in a Docker Container, use the following command.
```
docker run <image-name>
```
