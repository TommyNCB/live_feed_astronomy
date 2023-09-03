from flask import Flask

app = Flask(__name__)

import controllers.user_controller
import controllers.stream_controller