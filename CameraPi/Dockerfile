FROM python:3.8-slim

WORKDIR /CameraPi

# OpenCV dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    v4l-utils \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY . .

#  Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Generate gRPC files
RUN python -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. image_processing.proto

# change client.py depends what we are using

CMD ["python", "./clientCamera.py"] 
