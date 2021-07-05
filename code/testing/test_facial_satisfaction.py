import unittest
import sys

sys.path.insert(1, '../facial/')
from detection import assertain

class Test_detection(unittest.TestCase):
	
	def test_false_assertain(self):
		'''
		The following values captured from an authentication attempt which failed
		'''
		self.assertFalse(assertain([51.57502705940821, 51.681715493034694, 51.33240402883474, 52.31259402850559, 54.552747071949, 54.142084195864804, 54.3260142443206, 50.82937153813058, 51.095225987489044, 50.745581249105, 52.57548714206225, 51.07704380786218, 52.492898127730626, 50.692008583773884, 50.76830915989484, 51.23956289782422, 50.64033440060796, 52.73386015624086, 50.097677146212874, 51.281218696386176, 52.0094526548783, 50.48949324369988, 50.19098690511909, 50.56713294629312, 50.107046021044894, 50.329236416419974, 49.726450144025094, 50.80489309923476, 50.114952775808725, 49.910734891351154, 50.43732450719915, 50.1421912087699, 49.981581159268046, 50.63015133433008, 49.64924444777478, 50.04905590785745, 50.77035045015808, 50.37932634001421, 51.04086608042726, 51.484718883552056, 49.79213695730363, 49.398349764598464, 51.06328963275901, 49.62308050576432, 50.10858849566198, 49.369335953953815, 50.987043775352596, 49.441651486238484, 49.7216318010771, 49.003952225656704]))

	def test_true_assertain(self):
		'''
		The following values captured from an authentication attempt which passed.
		'''    	
		self.assertTrue(assertain([44.841154199406006, 45.788940451271095, 45.68625518821918, 43.800173146807474, 45.032477270412656, 44.54602734100917, 44.54702322520774, 44.59599183745054, 45.12578065043233, 44.766511514891846, 44.68326753424486, 44.99947352710371, 52.219141570346835, 45.274422573978924, 45.675794415103205, 43.33888332296908, 45.42169795028684, 45.36202227690281, 46.127997196840575, 43.270549279436864, 44.939486843141, 43.68539656221845, 45.933112876404984, 43.502802613344656, 43.30569979880528, 45.06587713622011, 45.29534593448032, 42.504868418568755, 45.56423148669084, 43.21980859368751, 45.453187410921984, 45.53759539892664, 44.66456281006771, 45.034252712099075, 44.77154454861443, 45.42031025119173, 45.78319460130237, 44.46549236928328, 45.70826259955556, 44.967413454936874, 44.79872460927027, 44.27163629121874, 45.57806988430379, 44.68173818662247, 43.685376816570454, 44.154101032316184, 44.10879178437788, 44.58820957114465, 44.36111750548747, 44.41098312823297] ))


if __name__ == '__main__':
	unittest.main()