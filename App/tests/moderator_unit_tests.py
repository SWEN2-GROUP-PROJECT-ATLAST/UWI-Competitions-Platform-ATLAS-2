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

    #Moderator Unit Tests
    def test_new_moderator(self):
        # Create and set up the Flask application context
        app = create_app()
        with app.app_context():
            # Recreate the database schema
            db.drop_all()
            db.create_all()

            # Create a new Moderator instance
            mod = Moderator("robert", "robertpass")

            # Assert the Moderator's username
            assert mod.username == "robert"

    def test_moderator_get_json(self):
        app = create_app()  # Create the Flask app
        with app.app_context():  # Push the application context
            # Recreate the database schema
            db.drop_all()
            db.create_all()

            # Create a new Moderator instance
            mod = Moderator("robert", "robertpass")
            db.session.add(mod)
            db.session.commit()  # Commit to generate an ID

            # Expected JSON output
            expected_json = {
                "id": mod.id,          # ID will be auto-generated
                "username": "robert",  # Username is set
                "competitions": []     # Default value for competitions
            }

            # Assert that `get_json` returns the expected dictionary
            self.assertDictEqual(mod.get_json(), expected_json)
    