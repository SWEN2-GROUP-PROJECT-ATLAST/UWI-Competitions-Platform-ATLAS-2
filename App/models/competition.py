from App.database import db
from datetime import datetime
from .competition_moderator import *
from .competition_team import *

class Competition(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String, nullable=False, unique=True)
    date = db.Column(db.DateTime, default= datetime.utcnow)
    location = db.Column(db.String(120), nullable=False)
    level = db.Column(db.Float, default=1)
    max_score = db.Column(db.Integer, default=25)
    teams = db.relationship('CompetitionTeam',backref='competition',lazy=True)
    moderators = db.relationship('Moderator',secondary='competition_moderator',backref=db.backref('competition',lazy=True))

    def __init__(self, name, date, location, level, max_score):
        self.name = name
        self.date = date
        self.location = location
        self.level = level
        self.max_score = max_score
    
    

    def get_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "date": self.date.strftime("%d-%m-%Y"),
            "location": self.location,
            "level" : self.level,
            "max_score" : self.max_score,
            "moderators": [mod.username for mod in self.moderators],
            "teams": [team.name for team in self.teams]
        }

    def toDict(self):
        return {
            "ID": self.id,
            "Name": self.name,
            "Date": self.date,
            "Location": self.location,
            "Level" : self.level,
            "Max Score" : self.max_score,
            "Moderators": [mod.username for mod in self.moderators],
            "Teams": [team.name for team in self.teams]
        }

    def __repr__(self):
        return f'<Competition {self.id} : {self.name}>'