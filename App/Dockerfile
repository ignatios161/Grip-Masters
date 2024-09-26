FROM python:3.8-slim

WORKDIR /usr/src/app

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

COPY requirements.txt ./

#  Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Generate gRPC files
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. object_tracking.proto

EXPOSE 8080

# change client.py depends what we are using
CMD ["python", "./client.py"] 
