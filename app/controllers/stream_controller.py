from flask import render_template, request, redirect, url_for, send_file, Response
from models.stream_model import Stream
from app import app

import datetime
import cv2
import os

recording = False
fourcc = None
out = None
camera_resolution = None
cap = cv2.VideoCapture(0)


@app.route("/streaming")
def streaming():
    start_recording()
    return render_template("streaming.html", recording=recording)

@app.route("/create_stream", methods=["POST"])
def create_stream():
    title = request.form.get("title")
    created_on = datetime.datetime.today()
    summary = request.form.get("summary")
    exp_method = request.form.get("exp_method")
    iso_sens = request.form.get("iso_sens")
    location = request.form.get("location")
    country = request.form.get("country")
    deleted = request.form.get("deleted")
    user_id = request.form.get("user_id")

    stream = Stream(title, created_on, summary, exp_method, iso_sens, location, country, deleted, user_id)
    stream.create_stream()

    return "success"

def start_recording():
    global recording, fourcc, out, cam_width, cam_height

    cam_width = int(cap.get(3)) 
    cam_height = int(cap.get(4))

    if not recording:
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        output_dir = "C:\\Users\\UnHelmet\\Desktop"
        output_path = os.path.join(output_dir, "output.avi")
        out = cv2.VideoWriter(output_path, fourcc, 30.0, (cam_width, cam_height))
        recording = True

def stop_recording():
    global recording, out

    if recording:
        out.release()
        recording = False

def generate_frames():
    global camera_resolution

    while True:
        ret, frame = cap.read()

        frame = cv2.resize(frame, (cam_width, cam_height))

        if recording:
            out.write(frame)

        if not ret:
            break

        _, buffer = cv2.imencode('.jpg', frame)

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')


@app.route("/video_feed")
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/stop_recording", methods=['POST'])
def stop_recording_route():
    stop_recording()
    return "Recording stopped"