FROM nvcr.io/nvidia/tritonserver:23.06-py3

# Install Python dependencies
RUN pip install transformers torch