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

    #Feature 2
    def test_create_notification(self):
        with self.app.app_context():
            # Create a user (student)
            student = User(username="james", password="jamespass")
            db.session.add(student)
            db.session.commit()

            # Create a notification for the student
            notification = Notification(student_id=student.id, message="Ranking changed!")
            db.session.add(notification)
            db.session.commit()

            # Retrieve the notification and check its attributes
            created_notification = Notification.query.filter_by(student_id=student.id).first()

            # Assert the notification is created
            self.assertIsNotNone(created_notification)
            self.assertEqual(created_notification.student_id, student.id)
            self.assertEqual(created_notification.message, "Ranking changed!")

    def test_notification_get_json(self):
        with self.app.app_context():
            # Create a user (student)
            student = User(username="james", password="jamespass")
            db.session.add(student)
            db.session.commit()

            # Create a notification for the student
            notification = Notification(student_id=student.id, message="Ranking changed!")
            db.session.add(notification)
            db.session.commit()

            # Retrieve the notification
            created_notification = Notification.query.filter_by(student_id=student.id).first()

            # Assert that the `get_json` method returns the correct format
            expected_json = {
                "id": created_notification.id,
                "student_id": created_notification.student_id,
                "notification": created_notification.message
            }
            self.assertDictEqual(created_notification.get_json(), expected_json)
