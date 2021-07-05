import prime_utils
import rsa_key_gen
import os
import os.path
import sys
from pathlib import Path

def get_public():
	# this function is self explanatory
	# obtain the keys from the cryptostore dir
	cwd = os.getcwd()
	os.chdir("../cryptostore")
	handler = open("public.txt", 'r')
	key = handler.readline()
	e, n = key.strip("()").split(",")
	handler.close()
	parsed_key = (int(e), int(n))
	os.chdir(cwd)
	return parsed_key


def get_private():
	# same as get_public
	
	cwd = os.getcwd()
	os.chdir("../cryptostore")
	handler = open("private.txt", 'r')
	key = handler.readline()
	d, n = key.strip("()").split(",")
	handler.close()
	parsed_key = (int(d), int(n))
	os.chdir(cwd)
	return parsed_key


def encrypt(aes_key, alt_key = None):
	# get the integer representation of the random gen aes key
	integer_representation = int.from_bytes(aes_key, byteorder = 'little')
	if alt_key is None:
	# this happens when we choose to encrypt with somebody elses public key , hence the alk-key mode
		public = get_public()
		e, n = public[0], public[1]
	else:
		# parse the alt key 
		e, n = alt_key.strip("()").split(",")
	# either way , encrypt it 
	encrypted_aes = pow(integer_representation, int(e), int(n))
	return encrypted_aes


def decrypt(encrypted_key):
	# decrypt is easy , just get the private key and attempt to decrypt 
	private = get_private()
	d, n = private[0], private[1]
	return pow(encrypted_key, d, n)





