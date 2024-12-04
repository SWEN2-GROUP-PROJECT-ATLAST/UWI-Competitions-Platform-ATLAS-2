import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import *
from App.controllers import *

LOGGER = logging.getLogger(__name__)

class UnitTests(unittest.TestCase):
    
    def setUp(self):
        """Setup the Flask app and the database."""
        self.app = create_app()  # Initialize the Flask app
        self.app.config['TESTING'] = True  # Set Flask to testing mode
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory SQLite for testing
        self.client = self.app.test_client()  # Create a test client
        with self.app.app_context():
            db.create_all()  # Create all tables

    def tearDown(self):
        """Clean up after each test."""
        with self.app.app_context():
            db.drop_all()  # Drop all tables after each test

    # Notification Unit Tests
    def test_new_notification(self):
        with self.app.app_context():  # Ensure we are in the application context
            notification = Notification(1, "Ranking changed!")
            db.session.add(notification)
            db.session.commit()

            # Retrieve the notification from the database and check values
            retrieved_notification = Notification.query.get(notification.id)
            assert retrieved_notification.student_id == 1 and retrieved_notification.message == "Ranking changed!"
    
    def test_notification_get_json(self):
        with self.app.app_context():  # Ensure we are in the application context
            notification = Notification(1, "Ranking changed!")
            db.session.add(notification)
            db.session.commit()

            expected_json = {"id": notification.id, "student_id": 1, "notification": "Ranking changed!"}
            self.assertDictEqual(notification.get_json(), expected_json)
