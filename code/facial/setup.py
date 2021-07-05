import numpy as np
import cv2 
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
directory = os.path.join(BASE_DIR, "../images")

#whole face
face_cascade = cv2.CascadeClassifier('../cascades/haarcascade_frontalface_default.xml')

#left eye
left_e_cascade  = os.path.join(BASE_DIR, '../cascades/haarcascade_lefteye_2splits.xml')
left_eye_cascade = cv2.CascadeClassifier(left_e_cascade)

#right eye
right_e_cascade  = os.path.join(BASE_DIR, '../cascades/haarcascade_righteye_2splits.xml')
right_eye_cascade = cv2.CascadeClassifier(right_e_cascade)


if os.path.isdir(os.path.join(BASE_DIR, "../images"))== False:
	images_directory = os.mkdir(os.path.join(BASE_DIR, "../images"))



def take_images(person):
	#person = input("Please enter your name: ")
	saved_images_dir = os.path.join(directory, person)
	try:
		os.mkdir(saved_images_dir)
	except FileExistsError:
		print("Overwriting.")
		saved_images_dir = os.path.join(directory, person)
		os.makedirs(saved_images_dir, exist_ok=True)
	
	i = 0
	cap = cv2.VideoCapture(0)
	minimumWidth = 0.1*cap.get(3)
	minimumHeight = 0.1*cap.get(4)
	while(True):
		# Capture from camera
		ret, frame = cap.read()

		try:
			#Convert frame to gray
			grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		except:
			print("Unable to open camera.\nExiting.")
			raise sys.exit(0)

		faces = face_cascade.detectMultiScale(grayscale, scaleFactor=1.05, minNeighbors=6, minSize = (int(minimumWidth), int(minimumHeight)))
		cv2.imshow('Window',frame)

		for (x,y,w,h) in faces:
			# Eye detection 
			left_eye = left_eye_cascade.detectMultiScale(
            grayscale,
            scaleFactor= 1.05,
            minNeighbors=5,
            minSize=(5, 5),
			)			
			right_eye = right_eye_cascade.detectMultiScale(
            grayscale,
            scaleFactor= 1.05,
            minNeighbors=5,
            minSize=(5, 5),
			)			


			#print(x,y,w,h)  DEBUG only prints when face is detected
			region_of_interest_gray = grayscale[y:y+h, x:x+w]  # Means face is being detected
															# (y_start value and y_end value)
			region_of_interest_color = frame[y:y+h, x:x+w]  # Means face is being detected
			
			# Draws box around face
			color = (255,0,0) # Blue, Green, Red 
			stroke = 2
			end_cord_x = x+w  
			end_cord_y = y+h
			
			# Save the image of the user as they're detected!
			cv2.imwrite(saved_images_dir+'/' +str(i)+'.png',frame)
			i += 1

			#Remove the rectangle from the saved image.
			#cv2.rectangle(frame, (x,y), (end_cord_x, end_cord_y), color, stroke)
		
		# Take 50 pictures
		if i > 51:
			break			
		# Shows the user their face
		cv2.imshow('Window',frame)
		
		# Needed to see the user in realtime
		if cv2.waitKey(20) & 0xFF == ord('q'):
			pass
			#break

	# Cleanup when Q is pressed or when 50 images are taken.
	cap.release() # Stop capturing
	cv2.destroyAllWindows() # Close window displaying image

