import grpc
from concurrent import futures
import time
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import io
from PIL import Image
import image_processing_pb2
import image_processing_pb2_grpc
import os


def template_matching_numpy(image_path, template_path):
    img = cv.imread(image_path, 0)
    template = cv.imread(template_path, 0)
    w, h = template.shape[::-1]

    res = np.zeros((img.shape[0] - w, img.shape[1] - h))
    for i in range(img.shape[0] - w):
        for j in range(img.shape[1] - h):
            res[i, j] = np.sum((img[i:i + w, j:j + h] - template) ** 2)

    min_val = np.min(res)
    min_loc = np.where(res == min_val)
    top_left = (min_loc[1][0], min_loc[0][0])
    bottom_right = (top_left[0] + w, top_left[1] + h)

    plt.subplot(121), plt.imshow(res, cmap='gray')
    plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(img, cmap='gray')
    plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
    plt.suptitle('numpy implementation')
    plt.show()

    return f"Template matching result: min_val={min_val}, top_left={top_left}, bottom_right={bottom_right}"

def generate_template_image(square_size, path):
    img = Image.new('L', (square_size, square_size), 0)
    img.save(path + 'template.png')

def process_image(image_data):
    # Convert the received byte data into an image file
    if not os.path.exists('Images'):
        os.makedirs('Images')

    image_path = 'Images/generated_image.png'
    with open(image_path, 'wb') as f:
        f.write(image_data)

    # Generate a template image
    template_path = 'Templates/'
    if not os.path.exists(template_path):
        os.makedirs(template_path)
    generate_template_image(10, template_path)

    # Perform template matching on the received image
    result = template_matching_numpy(image_path, template_path + 'template.png')

    return result

class ImageProcessingServicer(image_processing_pb2_grpc.ImageProcessingServicer):
    def ProcessImage(self, request, context):
        image_data = request.image_data
        result = process_image(image_data)
        return image_processing_pb2.ImageResponse(result=result)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    image_processing_pb2_grpc.add_ImageProcessingServicer_to_server(ImageProcessingServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server started on port 50051...")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == "__main__":
    serve()
