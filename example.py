import cv2
from BrowserCamera import BrowserCamera

browserCamera = BrowserCamera()

for frame in browserCamera.read():

		# *** WRITE YOUR CODE HERE ***  

		cv2.imshow("preview", frame)
		cv2.waitKey(1)