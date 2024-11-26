This project demonstrates real-time object detection using YOLOv3 (You Only Look Once) and OpenCV. The script captures video from a webcam, processes each frame using a pre-trained YOLOv3 model, and draws bounding boxes around detected objects with confidence scores.

Table of Contents
Features
Installation
Usage
Dependencies
File Structure
Acknowledgements
Features
Real-time Object Detection: Detects objects in live video feed using the YOLOv3 model.
Bounding Boxes: Draws colored bounding boxes around detected objects with labels and confidence scores.
Configurable Confidence Threshold: Filters out detections with low confidence.
Non-Maximum Suppression (NMS): Suppresses overlapping bounding boxes for accurate results.
Installation
Clone the repository:

bash
Copy code
git clone https://github.com/yourusername/YOLO-Object-Detection.git
cd YOLO-Object-Detection
Install the required dependencies:

bash
Copy code
pip install opencv-python numpy
Download the YOLOv3 model files:

YOLOv3 Configuration File (yolov3.cfg)
YOLOv3 Pre-trained Weights (yolov3.weights)
Place these files in a folder called model_data inside the project directory.

Usage
Make sure your webcam is connected and working.

Run the object detection script:

bash
Copy code
python object_detection.py
The live video feed will open, displaying detected objects with bounding boxes and labels. Press the q key to exit the video window.

Dependencies
Python 3.6+
OpenCV (opencv-python)
NumPy
To install the dependencies, run:

bash
Copy code
pip install -r requirements.txt
File Structure
bash
Copy code
YOLO-Object-Detection/
│
├── object_detection.py        # Main script for object detection
├── model_data/
│   ├── yolov3.cfg             # YOLOv3 configuration file
│   └── yolov3.weights         # YOLOv3 pre-trained weights
└── requirements.txt           # List of dependencies
Acknowledgements
YOLO: Real-Time Object Detection by Joseph Redmon.
OpenCV Documentation.
COCO Dataset for object labels.
Feel free to contribute or suggest improvements!
