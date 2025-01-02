docker run --rm --shm-size=10G -p8000:8000 -p8001:8001 -p8002:8002 -v $PWD/model_repository:/home/vbd-datnt-d/Documents/bert_triton/model_repository nvcr.io/nvidia/tritonserver:23.06-py3 tritonserver --model-repository=/model_repository --log-verbose=1
docker run --rm -p8000:8000 -p8001:8001 -p8002:8002 -v /home/vbd-datnt-d/Documents/bert_triton/model_repository:/models nvcr.io/nvidia/tritonserver:23.06-py3 tritonserver --model-repository=/models

docker run --rm -p8000:8000 -p8001:8001 -p8002:8002 \
  -v /home/vbd-datnt-d/Documents/bert_triton/model_repository:/models \
  tritonserver-custom \
  tritonserver --model-repository=/models