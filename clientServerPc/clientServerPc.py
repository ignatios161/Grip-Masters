import grpc
from concurrent import futures
import time
import image_processing_pb2
import image_processing_pb2_grpc
import io

# gRPC Server to receive image from Camera Pi
class ImageProcessingServicer(image_processing_pb2_grpc.ImageProcessingServicer):
    def ProcessImage(self, request, context):
        image_data = request.image_data
        print("Received image from Camera Pi. Forwarding to Pi1 for processing.")
        result = forward_image_to_pi1(image_data)
        # Print the response from Pi1 (processed result)
        print("Response from Pi1 (Server): ", result)
        return image_processing_pb2.ImageResponse(result=result)

def forward_image_to_pi1(image_data):
    pi1_ip = "192.168.10.163"  # Replace with the actual IP of Pi1

    # Connect to Pi1 to forward the image for processing
    channel = grpc.insecure_channel(f'{pi1_ip}:50051')
    stub = image_processing_pb2_grpc.ImageProcessingStub(channel)

    # Create a request with the received image data
    request = image_processing_pb2.ImageRequest(image_data=image_data)

    # Forward the image to Pi1 and get the result
    print("Forwarding image to Pi1...")
    response = stub.ProcessImage(request)

    print("Received response from Pi1:", response.result)
    return response.result

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    image_processing_pb2_grpc.add_ImageProcessingServicer_to_server(ImageProcessingServicer(), server)
    server.add_insecure_port('[::]:50052')  # Listening on port 50052 for Camera Pi
    server.start()
    print("PC is ready and listening on port 50052 for Camera Pi...")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == "__main__":
    serve()
