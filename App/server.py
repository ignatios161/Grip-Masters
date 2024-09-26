import grpc
from concurrent import futures
import time
import cv2
import numpy as np
import object_tracking_pb2
import object_tracking_pb2_grpc

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

class ComputeNodeServiceServicer(object_tracking_pb2_grpc.ComputeNodeServiceServicer):
    def ProcessFrame(self, request, context):
        print("Received frame for processing")
        # Process the frame for sending it to another Pi if needed
        # implementation missing here 
        return object_tracking_pb2.ProcessedData(processed_frame=request.frame) # Return the processed frame

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    object_tracking_pb2_grpc.add_CameraServiceServicer_to_server(CameraServiceServicer(), server)
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
