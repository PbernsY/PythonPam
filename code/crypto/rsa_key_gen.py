
from prime_utils import miller_rabin_test, generate_big_prime, obtain_both
from random import randrange
import os
import os.path
import sys

def euclid(number1, number2):
	while number2 != 0:
		number1, number2 = number2, number1 % number2
	return number1


def xgcd(a, b):
	# extended gcd
	# returns the (gcd, x, y)
	# such that gcd = ax + by
    x0, x1, y0, y1 = 0, 1, 1, 0
    while a != 0:
        (q, a), b = divmod(b, a), a
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1
    return (b, x0, y0)



def modinv(a, m):
	# requires the gcd of a and m , alongside the coefficients so 
	# gcd = ax + by
    g, x, y = xgcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


def generate_key_pair(prime1, prime2):
	# n -> used for modulus
	# phi -> carmichaels totient, basically LCM of p1 and p2
	# e -> coprime to phie ie the gcd of e and phi == 1 and 1 < e < phi 
	# d -> the modular multiplicative inverse of e modulo phi
	if not miller_rabin_test(prime1) and not miller_rabin_test(prime2):
		raise ValueError("Numbers need to be prime, re-run gen functions")
	# get the multiple of both primes, N , (this is RSA naming convention)
	n = prime1 * prime2
	# calculcate the totient the two primes, convention names this phi 
	phi = (prime1 - 1) * (prime2 - 1)
	# the below approach is okay, may need to write more maths to ensure it doesnt sit there spinning its wheels making random numbers
	initial_e_value = randrange(1, phi)
	possible_co_prime = euclid(initial_e_value, phi)
	while possible_co_prime != 1:
		initial_e_value = randrange(1, phi)
		possible_co_prime = euclid(initial_e_value, phi)
	d = modinv(initial_e_value, phi)
	#        public_key          private_key
	return ((initial_e_value,n),(d, n))



def store_keys(key_pair):
# make a directory called cryptostore which will store the keys
	public_component, private_component = key_pair[0], key_pair[1]
	os.chdir("../")
	os.mkdir("cryptostore")
	path = os.path.realpath("cryptostore")
	os.chdir(path)
	public = open("public.txt", 'w')
	public.write(str(key_pair[0]))
	public.close()
	private = open("private.txt", 'w')
	private.write(str(key_pair[1]))
	private.close()





def runner():
	#just a runner to make both keys (public private)
	#stores them as needed
	prime_1 = obtain_both(128)
	prime_2 = obtain_both(128)
	public, private = (generate_key_pair(prime_1, prime_2))
	store_keys((public, private))
	return public



