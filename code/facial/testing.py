#!/usr/bin/env python3
import numpy as np
import cv2 
import os
import pickle



BASE_DIR = os.path.dirname(os.path.abspath(__file__))
directory = os.path.join(BASE_DIR, "../images")
pickle_file = os.path.join(BASE_DIR, "labels.pickle")
trainer_data = os.path.join(BASE_DIR, "trainer_data.yml")

#left eye
left_e_cascade  = os.path.join(BASE_DIR, '../cascades/haarcascade_lefteye_2splits.xml')
left_eye_cascade = cv2.CascadeClassifier(left_e_cascade)

#right eye
right_e_cascade  = os.path.join(BASE_DIR, '../cascades/haarcascade_righteye_2splits.xml')
right_eye_cascade = cv2.CascadeClassifier(right_e_cascade)

#whole face
f_cascade = os.path.join(BASE_DIR, '../cascades/haarcascade_frontalface_default.xml')
face_cascade = cv2.CascadeClassifier(f_cascade)


#both eyes
both_e_cascade  = os.path.join(BASE_DIR, '../cascades/haarcascade_eye.xml')
both_eye_cascade = cv2.CascadeClassifier(both_e_cascade)


def assertain(positive_arr):
		#print('Confidence: {}'.format(sum(positive_arr) / len(positive_arr)))
		return (sum(positive_arr) / len(positive_arr))
'''
May want to fail if we cannot tell the difference ie 

you and someone else looking at the camera
def assertain(positive_arr):
	return (sum(positive_arr) / len(negative_arr))

'''
def detect():
	try:
		recognizer = cv2.face.LBPHFaceRecognizer_create()
		recognizer.read(trainer_data) 
	except:
		pass

	labels = {}

	with open(pickle_file,"rb") as f:
		labels = pickle.load(f)
		labels = {v:k for k,v in labels.items()}

	# Start looking at the camera
	cap = cv2.VideoCapture(0)
	
	# minimum size to fit criteria
	minimumWidth = 0.1*cap.get(3)
	minimumHeight = 0.1*cap.get(4)

	positive_identified = []
	negative_identified = []
	iters = 0
	while(True):
		# Capture from camera
		ret, frame = cap.read()

		#Convert frame to gray
		grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		faces = face_cascade.detectMultiScale(grayscale, scaleFactor=1.05, minNeighbors=6, minSize = (int(minimumWidth), int(minimumHeight))) # ScaleFactore may need to be adjusted


		for (x,y,w,h) in faces:
			#print(x,y,w,h)  DEBUG only prints when face is detected
			region_of_interest_gray = grayscale[y:y+h, x:x+w]  # Means face is being detected
															# (y_start value and y_end value)
			region_of_interest_color = frame[y:y+h, x:x+w]  # Means face is being detected

			#predict?

			# Eye detection 
			both_eye = both_eye_cascade.detectMultiScale(grayscale,scaleFactor= 1.05,minNeighbors=5,minSize=(5, 5))


			'''	
			left_eye = left_eye_cascade.detectMultiScale(grayscale,scaleFactor= 1.05,minNeighbors=5,minSize=(5, 5),)			
			right_eye = right_eye_cascade.detectMultiScale(grayscale,scaleFactor= 1.05,minNeighbors=5,minSize=(5, 5),)			
			'''			
			id_, confidence = recognizer.predict(region_of_interest_gray)

#			for (ex, ey, ew, eh) in left_eye:
				#cv2.rectangle(frame, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

#			for (ex, ey, ew, eh) in right_eye:
				#cv2.rectangle(frame, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
        


			# Face detection

			if (confidence < 100):

				print('Detecting:', labels[id_], confidence)
				font = cv2.FONT_HERSHEY_SIMPLEX
				name = labels[id_]
				color = (0,255,0) 
				stroke = 2
				iters += 1
				#print('\nHow confident:{}\nWe are of it being {}'.format(confidence,labels[id_]))
				positive_identified.append(confidence)
			
			else:
				name = "Unknown User"
				negative_identified.append(confidence)
				color = (0,0,255)
				#print('\nHow confident: {}\nWe are of it being {}'.format(confidence,name))
				stroke = 2
				end_cord_x = x+w  
				end_cord_y = y+h
				cv2.rectangle(frame, (x,y), (end_cord_x, end_cord_y), color, stroke)
			cv2.putText(frame,name,(x,y),cv2.FONT_HERSHEY_SIMPLEX,1,color,2,cv2.LINE_AA)

			# Draws box around face inherits the color from if above
			#cv2.rectangle(frame, (x,y), (end_cord_x, end_cord_y), color, stroke)
			
			iters += 1





		

		#return "success"	
		# Display image
		cv2.imshow('Window',frame)
		if cv2.waitKey(20) & 0xFF == ord('q'):
			break
	

	# Cleanup when Q is pressed
	'''
	if(assertain(positive_identified)) > 50:
		print("success")
	else:
		print("failure")
	'''
	# The closer we are to 0 the closer it is to identifying us correctly
	if(assertain(positive_identified)) < 50:
		print("success")
	else:
		# currently fails if it detects more than one person in the picture!
		print("failure")
	cap.release() # Stop capturing
	cv2.destroyAllWindows() # Close window displaying image


detect()
