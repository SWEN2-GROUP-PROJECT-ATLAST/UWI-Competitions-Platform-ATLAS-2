from App.database import db
from datetime import datetime

class RankHistory(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime,default=datetime.utcnow)
    rank = db.Column(db.Integer)
    rating = db.Column(db.Integer)

    def _init_(self,student_id,rank,rating):
        self.student_id = student_id
        self.rank = rank
        self.rating = rating

    def get_json(self):
        return {
            'student_id': self.student_id,
            'rank': self.rank,
            'date': self.date
        }
