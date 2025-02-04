run:
    docker build -t tritonserver-custom .
then, run:
    docker run --rm -p8000:8000 -p8001:8001 -p8002:8002 \
    -v /home/vbd-datnt-d/Documents/bert_triton/model_repository:/models \
    tritonserver-custom

in another terminal run 
    python rest_api.py 
to try the rest_api.py