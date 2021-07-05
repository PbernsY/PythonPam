import pyrebase
import sys
import os

config = {
	"authDomain":"fileencryption-214d3.firebaseio.com/",
	"databaseURL":"https://fileencryption-214d3.firebaseio.com/",
	"apiKey":"AIzaSyALXFqw4_qtLSaR6mpGnHkAQXRxot2Uuzg",
	"storageBucket": "https://fileencryption-214d3.firebaseio.com/"

}


firebase = pyrebase.initialize_app(config)

db = firebase.database() 

def check_available(name):
	check = db.child("public").get()
	check = check.val()
	for k, v in check.items():
		if name in check:
			check[name]
			return False
		return True


def new_upload(name,key):
	'''
	Uploads the following as:
	Name of user|
				|_public_key: publickey
				|
				|_contacts: None (currently as they're a new user) 

	'''
	db.child("public").child(name.lower()).child("public_key").set(str(key))
	db.child("public").child(name.lower()).child("contacts").set("")


#def upload_key(name,key):
	'''
	Uploads the following as:
	Name of user: their public key
	key         : value
	'''
#	db.child("public").child(name.lower()).set(str(key))
	

def update_last_contacted(user_to_add):
	# obtain the username
	with open("../facial/name.txt") as file:
		name = file.read()
	# Query firebase for the user information
	contacted = db.child("public").child(name).child("contacts").get()
	
	if contacted.val() != None:
		contacted = contacted.val()
		if type(contacted) == list:
			# put latest contact at the start
			contacted.insert(0,user_to_add)
		else:
			try:
				# Setup turns this to a string whereas a current user will return a list
				contacted = contacted.split(',') 
			except AttributeError:
				pass 
			contacted.insert(0,user_to_add) # This makes the latest user the top of the list.
		
		# Update firebase with the new addition
		update = db.child("public").child(name.lower()).child("contacts").set(contacted) 




def query_retrieve_key(name):
	'''
	All keys are currently stored under public -> name of user -> public key : key
	'''
	users = db.child("public").child(name).child("public_key").get()
	if users.val() != None:
		return( users.val())
	else:
		return(False)

def query_retrieve_contacts():
	'''
	Query the last three contacted of user
	'''
	with open("../facial/name.txt") as file:
		name = file.read()

	contacted = db.child("public").child(name).child("contacts").get()
	
	if contacted.val() != None:
		return contacted.val()
	else:
		return False



def query_contact_list():
	'''
	Query list of our users
	'''

	users = db.child("public").get()
	
	if users.val() != None:
		for u in users.val():
			return u
	

if __name__ == '__main__':
	query_retrieve_contacts()