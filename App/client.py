import grpc
import cv2
import time
import os
import object_tracking_pb2
import object_tracking_pb2_grpc

def run():
    # Connect to the gRPC server (main PC)
    channel = grpc.insecure_channel('10.126.93.9:50051')  # Server's IP and port
    stub = object_tracking_pb2_grpc.CameraServiceStub(channel)

    # Open default camera 
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    start_time = time.time()

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            print("Can't receive frame. Exiting ...")
            break

        
        # Send the frame to the server (convert frame to bytes first)
        _, buffer = cv2.imencode('.jpg', frame)
        frame_data = object_tracking_pb2.FrameData(frame=buffer.tobytes())
        response = stub.SendFrameData(frame_data)
        print(f"Sent frame. Server response: {response.message}")


        # Add object tracking using OpenCV (implement specific algorithm here)
        tracker = cv2.TrackerCSRT_create()
        bbox = cv2.selectROI(frame, False)
        ok = tracker.init(frame, bbox)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break


            # Update tracker and draw bounding box
            ok, bbox = tracker.update(frame)
            if ok:
                p1 = (int(bbox[0]), int(bbox[1]))
                p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                cv2.rectangle(frame, p1, p2, (255, 0, 0), 2)

            cv2.imshow("Tracking", frame)

            # Stop on 'q' key or after 30 seconds
            if cv2.waitKey(1) & 0xFF == ord('q') or time.time() - start_time > 30:
                break

        # Release the camera
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    run()


