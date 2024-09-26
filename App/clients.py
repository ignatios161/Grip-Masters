import grpc
import cv2
import object_tracking_pb2
import object_tracking_pb2_grpc
import numpy as np 

def run_client():
    channel = grpc.insecure_channel('localhost:50051')  #  Server IP
    stub = object_tracking_pb2_grpc.CameraServiceStub(channel)

    while True:
        # Request the next dataset frame from the server
        request = object_tracking_pb2.Request(message="Requesting next frame")
        response = stub.SendDatasetFrame(request)

        if response.message == "Dataset complete":
            print("Dataset processing complete.")
            break

        if response.frame == b'':
            print("No more frames available or error occurred.")
            break

        # Decode the frame
        nparr = np.frombuffer(response.frame, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Perform object detection/tracking locally

        # (local object tracking logic here)

        # Send results back to the server
        results = object_tracking_pb2.ResultData(message="Processing done for frame")
        print(f"Processing complete for frame. Sending result to server.")
        stub.SendResultData(results)

if __name__ == '__main__':
    run_client()
