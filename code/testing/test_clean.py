import unittest
import sys

sys.path.insert(1, '../facial/')
from clean import remove_folder

class Test_clean(unittest.TestCase):
	
	def test_images_not_present(self):
		'''
		This function tests if the images folder does not exist
		'''
		self.assertFalse(remove_folder(), False)

	'''
	We will never see the folder present as its removed on clean up by loader.py
	'''


if __name__ == '__main__':
	unittest.main()
