from flask import Flask, render_template, redirect, request
from flask_socketio import SocketIO
import cv2
import numpy as np;
import base64
import io
from imageio import imread
import threading
import os

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

class BrowserCamera:
	def __init__(self):
		self._properties = {"frame_width": 500, "frame_height": 700, "fps": 20}
		self.last_image = None
		self.create_ssl_certs()
		self.app()

	def create_ssl_certs(self):
		if not os.path.isdir(f"{DIR_PATH}/_ssl"):
			os.mkdir(f"{DIR_PATH}/_ssl")
		if not os.path.isfile(f"{DIR_PATH}/_ssl/cert.pem"):
			os.system(f"""openssl req -new -newkey rsa:4096 -days 365 -nodes -x509 -subj "/C=US/ST=Denial/L=Springfield/O=Dis/CN=localhost" -keyout {DIR_PATH}/_ssl/key.pem  -out {DIR_PATH}/_ssl/cert.pem""")

	def read(self):
		global last_image

		if self.last_image is None:
			return False, np.zeros((self._properties["frame_height"],self._properties["frame_width"],3), np.uint8)
		else:
			return True, self.last_image
	
	def set(self, propId, value):
		if propId == cv2.CAP_PROP_FRAME_WIDTH:
			self._properties["frame_width"] = value
			return True
		if propId == cv2.CAP_PROP_FRAME_HEIGHT:
			self._properties["frame_height"] = value
			return True
		if propId == cv2.CAP_PROP_FPS:
			self._properties["fps"] = value
			return True
		return False

	def get(self, propId):
		if propId == cv2.CAP_PROP_FRAME_WIDTH:
			return self._properties["frame_width"]
		if propId == cv2.CAP_PROP_FRAME_HEIGHT:
			return self._properties["frame_height"]
		if propId == cv2.CV_CAP_PROP_FPS:
			return self._properties["fps"]
		return 0

	def app(self):
		app = Flask(__name__, template_folder=f"{DIR_PATH}/_templates")
		socketio = SocketIO(app)

		@socketio.on('stream')
		def handle_stream(data):
			global last_image

			base64_string = data.split(',')[1]
			img = imread(io.BytesIO(base64.b64decode(base64_string)))
			cv2_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
			self.last_image = cv2_img

		@socketio.on('connect')
		def handle_connection(client_id):
			pass

		@app.route('/')
		def index():
			return render_template(
				'index.html', 
				FRAME_WIDTH=self._properties["frame_width"],
				FRAME_HEIGHT=self._properties["frame_height"],
				FPS=self._properties["fps"]
			)
			return (500)

		def run_camera_app():
			socketio.run(app, host="0.0.0.0", keyfile=f'{DIR_PATH}/_ssl/key.pem', certfile=f'{DIR_PATH}/_ssl/cert.pem')
		
		app_thread = threading.Thread(target=run_camera_app)
		app_thread.daemon = True
		app_thread.start()