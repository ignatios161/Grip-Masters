import grpc
from concurrent import futures
import time
import cv2
import numpy as np
import object_tracking_pb2
import object_tracking_pb2_grpc
import os

class CameraServiceServicer(object_tracking_pb2_grpc.CameraServiceServicer):
    def SendObjectPosition(self, request, context):
        print(f"Received object position: x={request.x}, y={request.y}")
        return object_tracking_pb2.Response(message="Position received by server")

    def SendFrameData(self, request, context):
        # Forward frame data to other compute nodes for processing/ later implementation 
        print("Received frame data from camera Pi")

        # Decode frame
        nparr = np.frombuffer(request.frame, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Perform processing here (e.g., object detection/tracking)
        tracker = cv2.TrackerCSRT_create()
        bbox = (100, 100, 80, 80)  # Example 
        ok = tracker.init(frame, bbox)

        if ok:
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (0, 255, 0), 2)
        
        return object_tracking_pb2.Response(message="Frame data processed and tracked.")
        
class DatasetDistributor(object_tracking_pb2_grpc.CameraServiceServicer):
    def __init__(self, dataset_dir):
        self.dataset_dir = dataset_dir
        self.image_files = sorted([f for f in os.listdir(dataset_dir) if f.endswith(('.png', '.jpg', '.jpeg'))])
        self.current_index = 0

    def SendDatasetFrame(self, request, context):
        if self.current_index >= len(self.image_files):
            return object_tracking_pb2.FrameData(frame=b'', message="Dataset complete")

        # Load the next image from the dataset
        image_path = os.path.join(self.dataset_dir, self.image_files[self.current_index])
        frame = cv2.imread(image_path)

        if frame is None:
            return object_tracking_pb2.FrameData(frame=b'', message="Error loading frame")

        # Encode frame to bytes and increment index
        _, buffer = cv2.imencode('.jpg', frame)
        self.current_index += 1

        return object_tracking_pb2.FrameData(frame=buffer.tobytes(), message=f"Sending frame {self.current_index}")
        
class ComputeNodeServiceServicer(object_tracking_pb2_grpc.ComputeNodeServiceServicer):
    def ProcessFrame(self, request, context):
        print("Received frame for processing")
        # Process the frame for sending it to another Pi if needed
        # implementation missing here 
        return object_tracking_pb2.ProcessedData(processed_frame=request.frame) # Return the processed frame

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    object_tracking_pb2_grpc.add_CameraServiceServicer_to_server(DatasetDistributor(dataset_dir), server) #Testing with Dataset
    #object_tracking_pb2_grpc.add_CameraServiceServicer_to_server(CameraServiceServicer(), server) # Real-time testing
    #object_tracking_pb2_grpc.add_ComputeNodeServiceServicer_to_server(ComputeNodeServiceServicer(), server) # Later implementation if we need
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051...")
    
    try:
        while True:
            time.sleep(86400)  # Keep server running
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
