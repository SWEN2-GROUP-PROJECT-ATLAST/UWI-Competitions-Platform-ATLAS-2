from App.database import db

class CompetitionResult(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    comp_team_id = db.Column(db.Integer, db.ForeignKey('competition_team'),nullable=False)
    score = db.Column(db.Integer,nullable=False)

    def __init__(self,comp_team_id,score):
        self.comp_team_id = comp_team_id
        self.score =score

    def get_json(self):
        return {
            'Team ID': self.comp_team_id,
            'Score': self.score
        }