# Triton Server with Custom Model Repository

This project demonstrates how to build and run a Triton server with a custom model repository and test it using a REST API and FastAPI.
***Remember to change the path at the Makefile***.

## Prerequisites
- **Docker** installed on your machine
- **Python** installed with the necessary dependencies for `rest_api.py`
- A valid **model repository** located at `/model_repository`
## Getting Started

### Step 1: Build the Docker Image
To build the Docker image for the Triton server, run:
```bash
make build
```
### Step 2: Start the Triton Server
Start the Triton server with your custom model repository using the following command:
```bash
make run
```
### Step 3: Run the REST API
In a separate terminal, execute the REST API script to interact with the Triton server:
```bash
make rest_api
```
## In Addition, Run the FastAPI:
**main.py** is the source code of the FastAPI
### Installation
```bash
pip install "fastapi[standard]"
```

### Run
```bash
uvicorn main:app --reload --port 8080
```
- Open http://127.0.0.1:8080/docs to use the API

