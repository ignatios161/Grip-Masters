# Grip-Masters
Project in Experts in team innovation

Project Title: Scalable 2D Object-Tracking Robot Using Edge Computing on Raspberry Pi Cluster

Objective

Design and build a 2-axis robotic platform capable of moving in 2D space to track the movement of an object in real-time using a camera. The computational tasks for object tracking will be distributed across multiple Raspberry Pis, each running a Docker container, allowing for scalable edge computing. The goal is to test whether adding more Raspberry Pis improves tracking performance in terms of speed and accuracy.

Problem Statement

Real-time object-tracking systems require significant computational resources to process video data and control robot movement. However, centralized computing can be expensive and difficult to scale. This project addresses the challenge by distributing the computation across a network of low-cost Raspberry Pis, which allows the system to scale flexibly and cost-effectively. The project will explore whether adding more Raspberry Pis improves the robot’s tracking performance and response time.

Key Features

2D Robot Movement: The robot will be equipped with motors that allow movement in both the X and Y axes. It will follow the movement of an object detected by a camera in real-time.
Object Tracking: A camera will capture the position of the object, and the data will be processed by computer vision algorithms running on Raspberry Pis. OpenCV or a similar library will be used for real-time object detection and tracking.
Edge Computing with Scalability: Multiple Raspberry Pis will be connected in a cluster, with each performing a portion of the object-tracking computation. This setup will test how adding more computational nodes improves tracking speed and accuracy.

Methodology

1.Hardware

Construct a 2D robot with stepper motors or DC motors to handle precise movement along the X and Y axes.
Mount a camera (e.g., Raspberry Pi Camera or USB Webcam) to capture object movements.
Set up a Raspberry Pi cluster where each Pi runs a Docker container dedicated to processing part of the object-tracking task.

2.Object Tracking Algorithm

Use OpenCV to detect and track object movements from the camera feed.
Implement a distributed computing model where different Raspberry Pis handle different parts of the tracking process, such as processing frames or detecting specific features of the object.

3.Scalability and Edge Computing

Test the system's performance with varying numbers of Raspberry Pis (1, 2, 3, etc.) to determine how the tracking improves as more computational power is added.
Use Docker to ensure each Raspberry Pi can run an identical instance of the tracking software, allowing for easy scaling and deployment.
Measure latency, tracking accuracy, and robot response time at each level of scalability.

4.Performance Evaluation

Analyze how the system's performance scales with additional hardware, looking at metrics like tracking precision, computational latency, and real-time response.
Test whether the system remains efficient and cost-effective as the workload increases.

Tools and Resources

Hardware: Raspberry Pi 4 (or equivalent), camera module, stepper motors, motor controllers, and power supplies.
Software: Docker for containerization, OpenCV for object tracking, Python or C++ for control logic, and network setup for Raspberry Pi cluster.
Distributed Computing: Setup for inter-device communication between Raspberry Pis for coordinating computation and synchronization.



