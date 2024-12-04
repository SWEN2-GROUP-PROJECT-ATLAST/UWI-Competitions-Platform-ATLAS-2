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

    # CompetitionModerator Unit Tests
    def test_new_competition_moderator(self):
        with self.app.app_context():  # Ensure we are in the application context
            competition_moderator = CompetitionModerator(1, 1)
            db.session.add(competition_moderator)
            db.session.commit()

            # Retrieve the competition moderator and verify the data
            retrieved_moderator = CompetitionModerator.query.get(competition_moderator.id)
            assert retrieved_moderator.comp_id == 1 and retrieved_moderator.mod_id == 1

    def test_competition_moderator_get_json(self):
        with self.app.app_context():  # Ensure we are in the application context
            competition_moderator = CompetitionModerator(1, 1)
            db.session.add(competition_moderator)
            db.session.commit()

            expected_json = {"id": competition_moderator.id, "competition_id": 1, "moderator_id": 1}
            self.assertDictEqual(competition_moderator.get_json(), expected_json)
