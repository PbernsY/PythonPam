import unittest
import sys

sys.path.insert(1, '../crypto/')
from prime_utils import miller_rabin_test



class Test_miller(unittest.TestCase):
	
	def test_miller_rabin_false(self):
		'''
		The following values is not prime
		'''
		self.assertFalse(miller_rabin_test(1), False)

	def test_miller_rabin_true(self):
		'''
		The following values is prime
		'''    	
		self.assertTrue(miller_rabin_test(2), True)

	def test_miller_rabin_zero(self):
		'''
		The following values is prime
		'''    	
		self.assertFalse(miller_rabin_test(0), False)

	def test_miller_rabin_minus(self):
		'''
		The following values is prime
		'''    	
		self.assertFalse(miller_rabin_test(-1000), True)
		self.assertNotEqual(miller_rabin_test(-1000), True)



if __name__ == '__main__':
	unittest.main()
