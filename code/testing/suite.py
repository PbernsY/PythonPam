import unittest

# unit tests
import test_firebase
import test_facial_satisfaction
import test_miller
import test_clean
# Initialize our test suite
loader = unittest.TestLoader()
suite  = unittest.TestSuite()

# Add tests to our test suite

suite.addTests(loader.loadTestsFromModule(test_clean))
suite.addTests(loader.loadTestsFromModule(test_firebase))
suite.addTests(loader.loadTestsFromModule(test_miller))
suite.addTests(loader.loadTestsFromModule(test_facial_satisfaction))

# Start our runner and let the suite run!
runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)