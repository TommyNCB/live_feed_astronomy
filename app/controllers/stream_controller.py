from flask import render_template, request, redirect, url_for, send_file, Response
from models.stream_model import Stream
from models.post_model import Post
from models.file_model import File
from app import app

import datetime
import cv2
import os

recording = False
fourcc = None
out = None
camera_resolution = None
cap = cv2.VideoCapture(0)
saved_file = None

live = None
s_id = None

@app.route("/streaming/<stream_id>", methods=["GET"])
def streaming(stream_id):

    checking = Stream.is_stream_live(stream_id)

    s_id = stream_id

    if checking == False:
        return redirect(url_for("homepage"))
    else:
        s = Stream.get_stream_title_by_id(stream_id)
        is_live = request.form.get("live")
        if s != None:
            start_recording()
            return render_template("streaming.html")
        elif is_live == True and stream_id == s:
            return render_template("streaming.html")
        elif is_live == False and stream_id == s:
            return redirect(url_for("homepage"))
        else:
            return "INVALID ID!"

@app.route("/create_stream", methods=["POST"])
def create_stream():
    global saved_file, live, s_id

    if request.method == "POST":

        live = True

        file = File(type="vid", created_on=datetime.datetime.today())
        saved_file = file.create_file()

        title = request.form.get("title")
        summary = "## Example Summary ##"
        stream = Stream(live=live, title=title, created_on=datetime.datetime.today(), summary=None, exp_method=None, iso_sens=None, location=None, country=None, deleted=False, user_id=None, file_id=saved_file)
        stream_id = stream.create_stream()
        
        s_id = stream_id

    return redirect(url_for("streaming", stream_id=str(stream_id)))

@app.route("/update_live_status", methods=["PATCH"])
def update_live_status(stream_id, live):
    stream = Stream.set_stream_live_status(stream_id, live)

@app.route("/start_recording", methods=["POST"])
def start_recording():
    global recording, out, cam_width, cam_height

    fourcc = None

    video_id = str(saved_file)

    cam_width = int(cap.get(3)) 
    cam_height = int(cap.get(4))

    if not recording:
        fourcc = cv2.VideoWriter_fourcc(*"H264")
        output_dir = os.path.join(app.root_path, 'static', 'files')
        output_path = os.path.join(output_dir, video_id + ".mp4")
        out = cv2.VideoWriter(output_path, fourcc, 30.0, (cam_width, cam_height))
        recording = True

@app.route("/stop_recording", methods=["POST"])
def stop_recording():
    global recording, out, live, s_id

    if recording:
        out.release()
        recording = False

        live = False

        update_live_status(s_id, live)

        live = None
        s_id = None

    return redirect(url_for("homepage"))

def generate_frames():
    global camera_resolution

    while True:
        ret, frame = cap.read()

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

def display_live_streams():
    ls = Stream.get_live_streams()
    return ls