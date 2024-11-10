from App.database import db

class TeamMember(db.Model):
    __tablename__ = 'team_member'

    id = db.Column(db.Integer,primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comp_team_id = db.Column(db.Integer,db.ForeignKey('competition_team.id'), nullable=False)


    def __init__(self,student_id,comp_team_id):
        self.student_id = student_id
        self.comp_team_id = comp_team_id

    def get_json(self):
        return {
            'student_id': self.student_id,
            'comp_team_id': self.comp_team_id
        }