# Triton Server with Custom Model Repository

This project demonstrates how to build and run a Triton server with a custom model repository and test it using a REST API.

## Prerequisites
- **Docker** installed on your machine
- **Python** installed with the necessary dependencies for `rest_api.py`
- A valid **model repository** located at `/home/vbd-datnt-d/Documents/bert_triton/model_repository`

## Getting Started

### Step 1: Build the Docker Image
To build the Docker image for the Triton server, run:
```bash
docker build -t tritonserver-custom .

### Step 2: Start the Triton Server
Start the Triton server with your custom model repository using the following command:
``bash
docker run --rm -p8000:8000 -p8001:8001 -p8002:8002 \
-v /home/vbd-datnt-d/Documents/bert_triton/model_repository:/models \
tritonserver-custom \
tritonserver --model-repository=/models

### Step 3: Run the REST API

``bash
python rest_api.py

