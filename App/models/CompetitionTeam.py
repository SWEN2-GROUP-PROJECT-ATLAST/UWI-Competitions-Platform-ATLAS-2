from App.database import db

class CompetitionTeam(db.Model):
    __tablename__ = 'competition_team'
    id = db.Column(db.Integer, primary_key=True)
    comp_id = db.Column(db.Integer, db.ForeignKey('competition.id'), nullable=False)
    name =  db.Column(db.String, nullable=False)
   

    def __init__(self, comp_id, name):
      self.comp_id = comp_id
      self.name = name


    def get_json(self):
      return {
          "id" : self.id,
          "team_id" : self.team_id,
          "competition_id" : self.comp_id,
          "points_earned" : self.points_earned,
          "rating_score" : self.rating_score
      }

    