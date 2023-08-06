import unittest
from . import test_registration, test_session_auth, test_token_auth


def my_module_suite() -> unittest.suite.TestSuite:
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(test_registration)
    return suite
