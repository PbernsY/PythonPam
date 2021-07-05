from random import randrange, getrandbits
def miller_rabin_test(prime_candidate, repetitions = 128):
# miller rabin works by combining fermat primality test AND Solovay-Strassen primality test
	# below tests are to prevent errors)
	if prime_candidate == 2 or prime_candidate == 3:
		return True
	if prime_candidate <= 1 or prime_candidate % 2 == 0:
		return False
	# pick miller-rabin #'s r and s so (primecand - 1) = r*(2 * s) 
	# and r is odd
	# a is also used such that a in range [2, primecand - 1]
	s = 0
	r = (prime_candidate - 1)
	while r & 1 == 0:
		s += 1
		r //= 2
	# here we repeat so we know its accurate, as miller rabin is probablistic
	for iter in range(repetitions):
		# [2, primecand - 1]  
		fermat_witness = randrange(2, prime_candidate - 1)
		# modular exponentiation
		y = pow(fermat_witness, r, prime_candidate)
		# above is the same as  fermat_witness ** r mod prime_cand
		if y != 1 and y != (prime_candidate - 1):
			i = 1
			while i < s and y != (prime_candidate - 1):
				y = pow(y, 2, prime_candidate)
				if y == 1:
					return False
				i += 1
			if y != (prime_candidate - 1):
				return False
	return True




# we need to generate random big primes, we use a method called a mersenne twister (pseudo random number generator)



def generate_big_prime(bits = 128):
	# we need to generate a 1024 bit random integer
	# if we set the msb to 1 , it will hold on 1024 bits ie it will always be  1024 bits
	# if we set the lsb to 1, itll be odd , the standard for RSA is generating a pseudo random odd integer of specified length (bits) and testing for primality
	candidate = getrandbits(bits)
	candidate |= (1 << bits - 1) | 1
	return candidate


def obtain_both(bits = 128):
	start = 4
	# start at a NON prime  number (so we know the miller rabin is working correctly)
	while miller_rabin_test(start, 128) != True:
		# while the chosen number (start) isnt prime, keep going until we hit a prime
		start = generate_big_prime(bits)
	return start






