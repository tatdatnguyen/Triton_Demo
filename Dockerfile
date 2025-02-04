# Sử dụng Triton với Python
FROM nvcr.io/nvidia/tritonserver:23.06-py3


RUN pip install --no-cache-dir transformers torch

ENV MODEL_REPOSITORY=/models

# Tạo thư mục cho model repository
RUN mkdir -p $MODEL_REPOSITORY

# Expose các cổng của Triton
EXPOSE 8000 8001 8002

# Lệnh để tự động khởi chạy Triton khi container chạy
ENTRYPOINT ["tritonserver", "--model-repository=/models", "--log-verbose=1"]
