from flask import render_template, request, redirect, url_for, send_file, Response, send_from_directory
from models.post_model import Post
from models.stream_model import Stream
from models.file_model import File
from app import app
import os

files_folder = os.path.join(app.root_path, "static", "files")   

def get_files():

    files = []

    for filename in os.listdir(files_folder):
        files.append(filename)
        

    return files

def display_posts():

    files_list_of_dict = File.get_all_fileids()
    ids_list = []

    data = {}

    stored = get_files()

    stored_files = [os.path.join("files", filename) for filename in stored]

    file = File.get_all_fileids()

    return ""

@app.route("/static/files/<filename>")
def serve_file(filename):
    return send_from_directory(files_folder, filename)

@app.template_filter("basename")
def basename_filter(value):
    return os.path.basename(value)

