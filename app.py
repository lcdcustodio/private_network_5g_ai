import argparse
import io
import os
from PIL import Image
import cv2
import numpy as np

import torch
from flask import Flask, render_template, request, redirect, Response

app = Flask(__name__)

# Load Pre-trained Model
model = torch.hub.load(
        "ultralytics/yolov5", "yolov5s", pretrained=True, force_reload=True
        )#.autoshape()  # force_reload = recache latest code

# Set Model Settings
model.eval()
model.conf = 0.6  # confidence threshold (0-1)
model.iou = 0.45  # NMS IoU threshold (0-1)

from io import BytesIO

def gen():

    cap=cv2.VideoCapture("CrowdedAreaFootageVideo.mp4")

    # Read until video is completed
    while(cap.isOpened()):

        # Capture frame-by-fram ## read the camera frame
        success, frame = cap.read()
        if success == True:

            ret,buffer=cv2.imencode('.jpg',frame)
            frame=buffer.tobytes()

            img = Image.open(io.BytesIO(frame))
            results = model(img, size=640)

            results.print()  # print results to screen

            #convert remove single-dimensional entries from the shape of an array
            img = np.squeeze(results.render()) #RGB
            # read image as BGR
            img_BGR = cv2.cvtColor(img, cv2.COLOR_RGB2BGR) #BGR


        else:
            break


        # Encode BGR image to bytes so that cv2 will convert to RGB
        frame = cv2.imencode('.jpg', img_BGR)[1].tobytes()

        yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    
    return render_template('index.html')

@app.route('/video')
def video():
    """Video streaming route. Put this in the src attribute of an img tag."""

    return Response(gen(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask app exposing yolov5 models")
    parser.add_argument("--port", default=5000, type=int, help="port number")
    args = parser.parse_args()

    app.run(host="0.0.0.0", port=args.port)  # debug=True causes Restarting with stat



