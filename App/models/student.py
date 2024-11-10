from App.database import db
from App.models import User

class Student(User):

    rating = db.Column(db.Integer, nullable=False, default=0)
    curr_rank = db.Column(db.Integer, nullable=False, default=0)
    prev_rank = db.Column(db.Integer, nullable=False, default=0)
    notifications = db.relationship('Notification',backref='student',lazy=True)
    competition_teams = db.relationship('CompetitionTeam',secondary='team_member',backref=db.backref('members',lazy=True))
    __mapper_args__ = {
        'polymorphic_identity': 'student'
    }

    def __init__(self, username, password):
        super().__init__(username, password)

   

    def get_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "rating_score": self.rating,
            "curr_rank" : self.curr_rank,
            'prev_rank':self.prev_rank
        }

 

    def __repr__(self):
        return f'<Student {self.id} : {self.username}>'