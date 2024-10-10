import grpc
import cv2
import time
import os
import image_processing_pb2
import image_processing_pb2_grpc
from PIL import Image, ImageDraw
import random
import io

def generate_image_grayscale_random_placed_squares(img_width, img_height, square_size):
    # Create image with white background
    img = Image.new('L', (img_width, img_height), 255)
    draw = ImageDraw.Draw(img)
    x0 = random.randint(0, img_width - square_size)
    y0 = random.randint(0, img_height - square_size)
    x1 = x0 + square_size
    y1 = y0 + square_size
    draw.rectangle([x0, y0, x1, y1], fill=0)
    return img


def run_camera_client(pc_ip):
    # Generate an image
    img = generate_image_grayscale_random_placed_squares(100, 100, 10)

    # Save the image to a byte buffer
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='PNG')
    img_data = img_buffer.getvalue()

    # Connect to the PC server to send the image
    channel = grpc.insecure_channel(f'{pc_ip}:50052')  
    stub = image_processing_pb2_grpc.ImageProcessingStub(channel)

    # Create a request with the generated image data
    request = image_processing_pb2.ImageRequest(image_data=img_data)

    # Send the request and receive the response
    response = stub.ProcessImage(request)

    print("Response from PC: ", response.result)

if __name__ == "__main__":
    pc_ip = "192.168.10.194"  
    run_camera_client(pc_ip)
