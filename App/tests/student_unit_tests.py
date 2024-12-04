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
    
    #Student Unit Tests
    def test_new_student(self):
        # Create the app and set up the app context
        app = create_app()  # Adjust if you don't use an app factory
        with app.app_context():  # Push an application context
            db.drop_all()
            db.create_all()
            
            student = Student("james", "jamespass")
            assert student.username == "james"
            
    def test_student_get_json(self):
        app = create_app()
        with app.app_context():
            # Recreate the database schema
            db.drop_all()
            db.create_all()

            # Create a new student instance and add to the database
            student = Student(username="james", password="jamespass")
            db.session.add(student)
            db.session.commit()  # Commit to generate the ID

            # Define the expected output
            expected_json = {
                "id": student.id,  # The ID will now be auto-generated
                "username": "james",
                "rating_score": 0,  # Default value
                "curr_rank": 0,     # Default value
                "prev_rank": 0,     # Default value
            }

            # Assert that `get_json` returns the expected dictionary
            self.assertDictEqual(student.get_json(), expected_json)
