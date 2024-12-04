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

    #Competition Unit Tests
    def test_new_competition(self):
      db.drop_all()
      db.create_all()
      competition = Competition("RunTime", datetime.strptime("09-02-2024", "%d-%m-%Y"), "St. Augustine", 1, 25)
      assert competition.name == "RunTime" and competition.date.strftime("%d-%m-%Y") == "09-02-2024" and competition.location == "St. Augustine" and competition.level == 1 and competition.max_score == 25

    def test_competition_get_json(self):
            app = create_app()  # Initialize the Flask app
            with app.app_context():  # Ensure we are within the application context
                db.drop_all()
                db.create_all()

                # Create a new competition instance
                competition = Competition(
                    name="RunTime", 
                    date=datetime.strptime("09-02-2024", "%d-%m-%Y"), 
                    location="St. Augustine", 
                    level=1, 
                    max_score=25
                )

                # Add the competition to the database and commit
                db.session.add(competition)
                db.session.commit()

                # Expected JSON output
                expected_json = {
                    "id": competition.id,  # ID will be auto-generated after committing to the DB
                    "name": "RunTime",
                    "date": "09-02-2024",
                    "location": "St. Augustine",
                    "level": 1,
                    "max_score": 25,
                    "moderators": [],  # Assuming no moderators yet
                    "teams": []  # Assuming no teams yet
                }

                # Assert that `get_json` returns the expected dictionary
                self.assertDictEqual(competition.get_json(), expected_json)