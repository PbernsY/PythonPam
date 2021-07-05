from setup import take_images
from trainer import training
from detection import detect
from clean import remove_folder
import sys
import os
sys.path.insert(1, "../crypto")
import rsa_key_gen
from fire_data import check_available
from fire_data import new_upload


def setvar(name):
	with open ("name.txt", "w") as handler:
		handler.write(name)


def main():
	name = input("Please enter your username of choice, please note this is what you'll be identified by: ")
	name = name.lower()
	print("Checking if {} is available.".format(name))
	check = check_available(name)
	while check != True:
		name = input( "Username taken\nPlease select a different name: ")
		check = check_available(name)
		
	setvar(name)
	print("{} is available!".format(name))
	print("Stage 1: Generating dataset.")
	take_images(name)
	print("Stage 2: Training and generating keys")
	training(name)
	firebase_payload = rsa_key_gen.runner()
	new_upload( str(name), str(firebase_payload)) #### instead of print this will be fired up to firebase
	print("Stage 2: Training complete.")
	print("Stage 3: Clean up...")
	remove_folder()
	print("Stage 3: Clean up complete.")
	print("Stage 4: Starting Facial Recognition.")
	detect()

if __name__ == '__main__':
	main()
