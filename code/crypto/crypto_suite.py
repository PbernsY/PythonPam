import rsa
import rsa_key_gen
import aes
import os.path
import os




def setup():
	if os.path.exists("cryptostore") == False:
		rsa_key_gen.runner()
	if os.path.exists("cryptostore") == True:
		return
	return



def encrypt_file(input_file, key = None):
	aes_key = aes.generate_aes_key()
	# generate the aes key using the os.urandom method
	apply_safety = rsa.encrypt(aes_key, key)
	# encrypt the aes key with rsa 
	byte_rep = apply_safety.to_bytes(60, byteorder = 'little')
	# turn the encrypted aes key into bytes , allows encryption AND obfuscation to take place
	aes.aes_encrypt(input_file, aes_key, byte_rep)
	#using aes, encrypt the chosen file



def decrypt_file(input_file):
	encrypted_aes_key = key_grab(input_file)
	# the key grab function grabs the  key as it is the first 60 bytes of the encrypted file
	if encrypted_aes_key is None:
		return 1
	#this above function ensures that an attempt to decrypt an empty file can be caught before it throws an exception
	inter = rsa.decrypt(encrypted_aes_key)
	# decrypt the RSA encrypted aes key 
	key = inter.to_bytes(16, byteorder = 'little')
	# turn it back into bytes so the aes decrypt function can decrypt the file 
	aes.aes_decrypt(input_file, key)
	# file decrypted


def key_grab(input_file):
	if os.path.getsize(input_file) == 0 or os.path.getsize(input_file) < 60:
		return None
	# sets the flag as 1 for decrypt file if the file is physcially too small to have been previously encrypted with aes
	handle = open(input_file, 'rb')
	byte_key = handle.read(60)
	# read the first 60 bytes (the key)
	handle.close()
	return int.from_bytes(byte_key, byteorder = 'little')
	# return an integer representation of the key 



