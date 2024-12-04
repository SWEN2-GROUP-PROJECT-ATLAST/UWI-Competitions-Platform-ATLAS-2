import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import *
from App.controllers import *


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UnitTests(unittest.TestCase):

    #StudentTeam Unit Tests
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

    # StudentTeam Unit Tests
    def test_new_student_team(self):
        with self.app.app_context():  # Ensure we are in the application context
            # Create necessary records in the database for the test to work
            student = User(username="john_doe", password="password")
            db.session.add(student)
            db.session.commit()

            competition_team = CompetitionTeam(comp_id=1, name="Team A")
            db.session.add(competition_team)
            db.session.commit()

            # Create a TeamMember instance (this is the equivalent of a "student team")
            student_team = TeamMember(student_id=student.id, comp_team_id=competition_team.id)
            db.session.add(student_team)
            db.session.commit()

            # Retrieve the student_team and verify its attributes
            retrieved_student_team = TeamMember.query.get(student_team.id)
            self.assertEqual(retrieved_student_team.student_id, student.id)
            self.assertEqual(retrieved_student_team.comp_team_id, competition_team.id)

            # Test the get_json method
            expected_json = {
                'student_id': student.id,
                'comp_team_id': competition_team.id
            }
            self.assertDictEqual(retrieved_student_team.get_json(), expected_json)
    

