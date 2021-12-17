from flask import Flask, render_template
from flask_socketio import SocketIO
import cv2
import numpy as np;
import base64
import io
from imageio import imread
import threading
import queue


# ======================================== DO NOT MODIFY ================================================
# 							| | | WRITE YOUR OPENCV CODE IN THE __MAIN__ FUNCTON  | | |
#							V V V												  V V V


app = Flask(__name__, template_folder="_templates")
socketio = SocketIO(app)
q = queue.Queue()

@socketio.on('stream')
def handle_stream(data):
	base64_string = data.split(',')[1]
	img = imread(io.BytesIO(base64.b64decode(base64_string)))
	cv2_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
	q.put(cv2_img)

@socketio.on('connect')
def handle_connection(client_id):
	print("The Browser Camera seems to be connected. Let's see what cool ass stuff you can do with it !")

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
		cv2.namedWindow("preview")
		print("Browser Camera waiting for connection...")

	def read(self):
		val = np.zeros((100,100,3), np.uint8)
		while True:
			if not q.empty():
				val = q.get()
			yield val


if __name__ == '__main__':
	browserCamera = BrowserCamera()
	for frame in browserCamera.read():

		# *** WRITE YOUR CODE HERE ***  

		cv2.imshow("preview", frame)
		cv2.waitKey(1)