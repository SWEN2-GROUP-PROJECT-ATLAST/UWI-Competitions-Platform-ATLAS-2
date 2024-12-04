import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import *
from App.controllers import *


LOGGER = logging.getLogger(__name__)

'''
    Integration Tests
'''
class IntegrationTests(unittest.TestCase):

    def setUp(self):
        """Setup the Flask app and the database."""
        self.app = create_app()  # Initialize the Flask app
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()  # Create a test client
        with self.app.app_context():
            db.create_all()  # Create all tables

    def tearDown(self):
        """Clean up after each test."""
        with self.app.app_context():
            db.drop_all()  # Drop all tables after each test

    #Feature 3
    def test_create_student(self):
        with self.app.app_context():
            # Create a student
            student = create_student("james", "jamespass")
            
            # Ensure the student was created and committed to the database
            self.assertIsNotNone(student)
            self.assertEqual(student.username, "james")
            self.assertTrue(Student.query.filter_by(username="james").first() is not None)


