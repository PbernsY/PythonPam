from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os
import random



def generate_aes_key():
	# needs to be a 128 bit key ie 16 bytes
	# urandom takes random info from os and turns it into stuff
	key =  os.urandom(16)
	return key



# gonna use CBC mode here

def aes_encrypt(input_file, key, safety_rsa_key):
	# take an input file, read in as bytes
	# output an output file
	# gen the key and encrypt using this
	# create the cipher object with mode set as CBC (Cipher Block Chaining)
	contents = file_reader(input_file)
	encrypt_cipher = AES.new(key, AES.MODE_CBC)
	# takes key and mode and sets cipher accordingly 
	encrypted_data = encrypt_cipher.encrypt(pad(contents, AES.block_size))
	file_writer(input_file, encrypted_data, encrypt_cipher.iv, safety_rsa_key,  mode = "encrypt")


def aes_decrypt(input_file, key):
	decrypt_file = open(input_file, 'rb')
	decrypt_file.seek(60)
	# open the decrypt file and seek to byte 60 (this bypasses the key)
	vector = decrypt_file.read(16)
	# read the IV (vector)
	encrypted_contents = decrypt_file.read()
	decrypt_file.close()
	decrypt_cipher = AES.new(key, AES.MODE_CBC, iv = vector)
	# instantiate the decrypt cipher with the key, chosen mode and iv)
	original = unpad(decrypt_cipher.decrypt(encrypted_contents), AES.block_size)
	# unpad the contents, using the decrypt cipher )
	file_writer(input_file, original, decrypt_cipher.iv, None , mode = "decrypt")
	# use the file writer in decrypt mode to write decrypted contents back to file



def file_reader(input_file):
	handler = open(input_file, 'rb')
	# open the file in bytes
	data = handler.read()
	# read all of it 
	handler.close()
	# return the byte data
	return data

def file_writer(input_file, data,  IV, safety_rsa_key,  mode = None):
	# depending on mode, it either writes encrypted data and keys BACK to file
	# or write the decrypted data back into the file
	handler = open(input_file, "wb")
	if mode == "encrypt":
		handler.write(safety_rsa_key)
		handler.write(IV)
		handler.write(data)
	if mode == "decrypt":
		handler.write(data)
	handler.close()




