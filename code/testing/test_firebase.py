import unittest
import sys

sys.path.insert(1, '../facial/')
from fire_data import check_available
from fire_data import query_retrieve_key

from fire_data import query_retrieve_contacts
from fire_data import query_contact_list




class Test_firebase(unittest.TestCase):
	
	def test_check_available_true(self):
		'''
		This function tests to see if dasdkla is availabe
		'''
		self.assertTrue(check_available('dasdkla'),True)

	def test_check_available_false(self):
		'''
		This function tests to see if dasdkla is not availabe
		'''
		self.assertFalse(check_available('berns-kyle'),False)

	def test_query_retrieve_key_success(self):
		'''
		This function retrieves the public key of a user 
		'''

		self.assertEqual(query_retrieve_key('berns-kyle'), "(30509583494067312855707515875099794915099139563086414086590450641730513297687, 46316640772856691484688364421225162270205641663332191572058569399640601778331)")

	def test_query_retrieve_key_failed(self):
		'''
		This function retrieves the public key of a user 
		'''

		self.assertNotEqual(query_retrieve_key('berns-kyle'), "")	

	def test_query_retrieve_contacts(self):
		'''
		This function tests retrieve contacts of a user
		'''
		self.assertEqual(query_retrieve_contacts(), ['berns-kyle', 'berns-kyle', 'kyle', 'test', 'john'] )
		self.assertNotEqual(query_retrieve_contacts(), "hello")

	def test_query_contact_list(self):
		'''
		This function retrieves the contact list of the user
		'''
		self.assertNotEqual(query_contact_list(), "hello")
		self.assertEqual(query_contact_list(), "berns-kyle")


if __name__ == '__main__':
	unittest.main()
