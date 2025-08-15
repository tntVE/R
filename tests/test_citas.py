# -*- coding: utf-8 -*-
import unittest
from app import create_app
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

class CitasTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_example(self):
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
