from flask import Flask, render_template
from flask_socketio import SocketIO
import cv2
import numpy as np;
import base64
import io
from imageio import imread
import threading

app = Flask(__name__, template_folder="_templates")
socketio = SocketIO(app)
last_image = None

@socketio.on('stream')
def handle_stream(data):
	global last_image

	base64_string = data.split(',')[1]
	img = imread(io.BytesIO(base64.b64decode(base64_string)))
	cv2_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
	last_image = cv2_img

@socketio.on('connect')
def handle_connection(client_id):
	pass

@app.route('/')
def index():
	 return render_template('index.html')

def run_camera_app():
	socketio.run(app, host="0.0.0.0", keyfile='_ssl/key.pem', certfile='_ssl/cert.pem')

class BrowserCamera:
	def __init__(self):
		app_thread = threading.Thread(target=run_camera_app)
		app_thread.daemon = True
		app_thread.start()

	def read(self):
		global last_image

		if last_image is None:
			return False, np.zeros((100,100,3), np.uint8)
		else:
			return True, last_image
