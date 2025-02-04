# Variables
DOCKER_IMAGE_NAME=tritonserver-custom
MODEL_REPO_PATH=/home/vbd-datnt-d/Documents/bert_triton/model_repository
PROMETHEUS_YML_PATH=/home/vbd-datnt-d/Documents/bert_triton/prometheus.yml

.PHONY: build run prometheus rest_api all

# Build the Docker image
build:
	docker build -t $(DOCKER_IMAGE_NAME) .

# Run the Triton Docker container
run:
	docker run --rm --name triton -p8000:8000 -p8001:8001 -p8002:8002 \
	-v $(MODEL_REPO_PATH):/models \
	$(DOCKER_IMAGE_NAME)

# Run the Prometheus Docker container
prometheus:
	docker run --rm --name prometheus -p 9090:9090 \
	-v $(PROMETHEUS_YML_PATH):/etc/prometheus/prometheus.yml \
	prom/prometheus

# Run the REST API script
rest_api:
	python rest_api.py
grafana:
	docker run --name grafana \
  -p 3000:3000 \
  grafana/grafana			

# Run all tasks (build, run Triton, run Prometheus, and REST API)
all: build run prometheus rest_api
