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

    #CompetitionTeam Unit Tests
    def test_new_competition_team(self):
        app = create_app()  # Initialize the Flask app
        with app.app_context():  # Ensure we are within the application context
            db.drop_all()
            db.create_all()

            # Create a new CompetitionTeam instance
            competition_team = CompetitionTeam(comp_id=1, name="Scrum Lords")

            # Add the competition_team to the database and commit
            db.session.add(competition_team)
            db.session.commit()

            # Assert that the competition_team attributes are set correctly
            assert competition_team.comp_id == 1
            assert competition_team.name == "Scrum Lords"
            assert competition_team.hasResult is False  # Default value for hasResult

    def test_competition_team_get_json(self):
        app = create_app()  # Initialize the Flask app
        with app.app_context():  # Ensure we are within the application context
            db.drop_all()
            db.create_all()

            # Create a new CompetitionTeam instance
            competition_team = CompetitionTeam(comp_id=1, name="Scrum Lords")

            # Add the competition_team to the database and commit
            db.session.add(competition_team)
            db.session.commit()

            # Expected JSON output
            expected_json = {
                "id": competition_team.id,  # ID will be auto-generated after committing to the DB
                "competition_id": 1,
                "name": "Scrum Lords",
                "result": [],  # Assuming no results for this team
                "members": []  # Assuming no members yet
            }

            # Assert that get_json returns the expected dictionary
            self.assertDictEqual(competition_team.get_json(), expected_json)

