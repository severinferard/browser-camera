import cv2
from BrowserCamera import BrowserCamera

cap = BrowserCamera()
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 500)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 700)
cap.set(cv2.CAP_PROP_FPS, 20)

while True:
	ret, frame = cap.read()

	# *** WRITE YOUR CODE HERE ***  

	cv2.imshow("preview", frame)
	cv2.waitKey(1)