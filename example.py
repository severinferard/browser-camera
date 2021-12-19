import cv2
from BrowserCamera import BrowserCamera

cap = BrowserCamera()
while True:
	ret, frame = cap.read()

	# *** WRITE YOUR CODE HERE ***  

	cv2.imshow("preview", frame)
	cv2.waitKey(1)