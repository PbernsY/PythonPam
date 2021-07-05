# TODO FIX faces on line 46 otherwise wont be accurate

import cv2
import os
import numpy as np
from PIL import  Image
import pickle

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # uses path of this file
def training(name):
	# whole face
	face_cascade = cv2.CascadeClassifier('../cascades/haarcascade_frontalface_default.xml')
	
	# testing 
	face_two_cascade =cv2.CascadeClassifier('../cascades/haarcascade_frontalface_alt.xml')

	#both eyes
	both_e_cascade  = os.path.join(BASE_DIR, '../cascades/haarcascade_eye.xml')
	both_eye_cascade = cv2.CascadeClassifier(both_e_cascade)

	#left eye
	left_e_cascade  = os.path.join(BASE_DIR, '../cascades/haarcascade_lefteye_2splits.xml')
	left_eye_cascade = cv2.CascadeClassifier(left_e_cascade)

	#right eye
	right_e_cascade  = os.path.join(BASE_DIR, '../cascades/haarcascade_righteye_2splits.xml')
	right_eye_cascade = cv2.CascadeClassifier(right_e_cascade)


	#LBPH Recognizer
	recognizer = cv2.face.LBPHFaceRecognizer_create()

	current_id = 0
	label_ids = {}

	y_labels = []
	x_train = []

	image_dir = os.path.join(BASE_DIR, "../images/"+name)
	for root, dirs, files in os.walk(image_dir):
		for file in files:
			if file.endswith("png") or file.endswith("jpg"):
				path = os.path.join(root, file)			# Eye detection 
				label = os.path.basename(os.path.dirname(path)).replace(" ", "-").lower()
				if not label in label_ids:
					label_ids[label] = current_id
					current_id += 1
				id_ = label_ids[label] # ID of the user

				pil_image = Image.open(path).convert("L") # convert color to grayscale
				size = (550,550) # resize to provide better predictions
				final_image = pil_image.resize(size,Image.ANTIALIAS)
				image_array = np.array(final_image, "uint8") # convert to numpy array


				faces = face_cascade.detectMultiScale(image_array, scaleFactor=1.05,  minNeighbors=6)
				faces_two = face_two_cascade.detectMultiScale(image_array, scaleFactor=1.05,  minNeighbors=6)
				left_eye = left_eye_cascade.detectMultiScale(image_array,scaleFactor= 1.05,minNeighbors=6,minSize=(5, 5))			
				right_eye = right_eye_cascade.detectMultiScale(image_array,scaleFactor= 1.05,minNeighbors=6,minSize=(5, 5))								
				both_eye = both_eye_cascade.detectMultiScale(image_array,scaleFactor= 1.05,minNeighbors=6,minSize=(5, 5))								

				for (x,y,w,h) in both_eye:
					region_of_interest = image_array[y:y+h, x:x+w]
					x_train.append(region_of_interest)  
					y_labels.append(id_)

				for (x,y,w,h) in faces:
					region_of_interest = image_array[y:y+h, x:x+w]
					x_train.append(region_of_interest)  
					y_labels.append(id_)
				'''
				for (x,y,w,h) in left_eye:
					region_of_interest = image_array[y:y+h, x:x+w]
					x_train.append(region_of_interest)  
					y_labels.append(id_)

				for (x,y,w,h) in right_eye:
					region_of_interest = image_array[y:y+h, x:x+w]
					x_train.append(region_of_interest)  
					y_labels.append(id_)
				'''




	with open("labels.pickle", "wb") as file:
		pickle.dump(label_ids,file)


	recognizer.train(x_train, np.array(y_labels)) # generated from x_train.append(region_of_interest)  
	recognizer.save("trainer_data.yml")


