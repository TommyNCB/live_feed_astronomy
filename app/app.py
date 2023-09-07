from flask import Flask, render_template

app = Flask(__name__)

import controllers.user_controller
from controllers.stream_controller import *
from controllers.post_controller import *

@app.route('/homepage')
def homepage():
    streams_data = display_live_streams()
    return render_template('homepage.html', streams_data = streams_data)