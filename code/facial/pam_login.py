#!/usr/bin/env python3
import numpy as np
import cv2 
import os
import pickle



BASE_DIR = os.path.dirname(os.path.abspath(__file__))
pickle_file = os.path.join(BASE_DIR, "labels.pickle")
trainer_data = os.path.join(BASE_DIR, "trainer_data.yml")

#whole face
cascade = os.path.join(BASE_DIR, '../cascades/haarcascade_frontalface_default.xml')
face_cascade = cv2.CascadeClassifier(cascade)

#both eyes
both_e_cascade  = os.path.join(BASE_DIR, '../cascades/haarcascade_eye.xml')
both_eye_cascade = cv2.CascadeClassifier(both_e_cascade)


def assertain(positive_arr):
		return (sum(positive_arr) / len(positive_arr))

def detect():
	try:
		recognizer = cv2.face.LBPHFaceRecognizer_create()
		recognizer.read(trainer_data) 
	except:
		pass

	labels = {}

	#Where it gets the name supplied to loader.py from
	with open(pickle_file,"rb") as f:
		labels = pickle.load(f)
		labels = {v:k for k,v in labels.items()}

	# Call to open webcam
	cap = cv2.VideoCapture(0)
	
	# minimum size to fit criteria
	minimumWidth = 0.1*cap.get(3)
	minimumHeight = 0.1*cap.get(4)
	# capture confidence when identifed
	positive_identified = []
	negative_identified = []

	i = 0
	while(i < 50):
		# Capture from camera
		ret, frame = cap.read()

		try:
			#Convert frame to gray
			grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		except:
			print("Unable to open camera.\nExiting.")
			raise sys.exit(0)

		faces = face_cascade.detectMultiScale(grayscale, scaleFactor=1.05, minNeighbors=6, minSize = (int(minimumWidth), int(minimumHeight))) # ScaleFactore may need to be adjusted

		for (x,y,w,h) in faces:

			region_of_interest_gray = grayscale[y:y+h, x:x+w]  # Means face is being detected
															# (y_start value and y_end value)
			region_of_interest_color = frame[y:y+h, x:x+w]  # Means face is being detected

			#predict?

			# Eye detection 
			both_eye = both_eye_cascade.detectMultiScale(grayscale,scaleFactor= 1.05,minNeighbors=5,minSize=(5, 5))

			id_, confidence = recognizer.predict(region_of_interest_gray)

			# Face detection
			if (confidence < 100):
				font = cv2.FONT_HERSHEY_SIMPLEX
				name = labels[id_]
				color = (0,255,0) 
				stroke = 2
				id_ += 1
				positive_identified.append(confidence)
			
			else:
				name = "Unknown User"
				negative_identified.append(confidence)
				color = (0,0,255)
				stroke = 2
				end_cord_x = x+w  
				end_cord_y = y+h
				cv2.rectangle(frame, (x,y), (end_cord_x, end_cord_y), color, stroke)
			cv2.putText(frame,name,(x,y),cv2.FONT_HERSHEY_SIMPLEX,1,color,2,cv2.LINE_AA)

			
			i += 1

		if cv2.waitKey(20) & 0xFF == ord('q'):
			break
	

	# Cleanup when Q is pressed
	
	# The closer we are to 0 the closer it is to identifying us correctly
	if(assertain(positive_identified)) < 60:
		#print("Authentication successful!")
		print(1)
	else:
		# currently fails if it detects more than one person in the picture!
		#print("Authentication failed!")
		print(-1)

	cap.release() # Stop capturing


detect()
