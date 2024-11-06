from App.database import db
from App.models import User

class Moderator(User):

    
    def __init__(self, username, password):
        super().__init__(username, password)

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username,
            'competitions': [comp.name for comp in self.competitions]
        }

  
    def __repr__(self):
        return f'{self.username}'
