from App.database import db

class CompetitionTeam(db.Model):
    __tablename__ = 'competition_team'
    id = db.Column(db.Integer, primary_key=True)
    comp_id = db.Column(db.Integer, db.ForeignKey('competition.id'), nullable=False)
    name =  db.Column(db.String, nullable=False)
    hasResult = db.Column(db.Boolean, nullable=False)
    result = db.relationship('CompetitionResult',backref='team',lazy=True)
   

    def __init__(self, comp_id, name):
      self.comp_id = comp_id
      self.name = name
      self.hasResult = False


    def get_json(self):
      return {
          "id" : self.id,
          "competition_id" : self.comp_id,
          "name" : self.name,
          "result" : self.result,
          "members": self.members
      }

    