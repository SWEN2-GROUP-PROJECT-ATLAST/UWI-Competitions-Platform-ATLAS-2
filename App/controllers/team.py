from App.database import db
from App.models import CompetitionTeam, Competition, Student, Moderator,TeamMember

def create_team(comp_name,team_name, students):
    competiton = Competition.query.filter_by(name=comp_name).first()
    if not competiton:
        return None

    team = CompetitionTeam(comp_id=competiton.id,name=team_name)
    competition_team = CompetitionTeam.query.filter_by(comp_id=competiton.id,name=team_name).first()
    if  competition_team:
        return None
   
    db.session.add(team)
    count = 0
    for s in students:
        stud = Student.query.filter_by(username=s).first()
        if stud:
            teamMember = TeamMember(student_id=stud.id,comp_team_id=team.id)
            db.session.add(teamMember)
        else:
            count += 1
            print(f'{s} was not found!')
    
    if count == 3:
        return None
    else:
        try:
            db.session.commit()
            print(f'New Team: {team_name} created!')
            return team
        except Exception as e:
            db.session.rollback()
            print("Something went wrong!")
            return None

def get_team_by_name(name):
    return CompetitionTeam.query.filter_by(name=name).first()

def get_team(id):
    return CompetitionTeam.query.get(id)

def get_all_teams():
    return CompetitionTeam.query.all()

def get_all_teams_json():
    teams = CompetitionTeam.query.all()

    if not teams:
        return []
    else:
        return [team.get_json() for team in teams]
    
def find_team(team_name, students):
    teams = CompetitionTeam.query.filter_by(name=team_name).all()
    
    for team in teams:
        team_stud = []
        for stud in team.members:
            team_stud.append(stud.username)
        
        if set(team_stud) == set(students):
            return team

    return None



"""
def add_results(mod_name, comp_name, team_name, students, score):
    add_team(mod_name, comp_name, team_name, students)
    
    mod = Moderator.query.filter_by(username=mod_name).first()
    comp = Competition.query.filter_by(name=comp_name).first()
    teams = Team.query.filter_by(name=team_name).all()

    if not mod:
        print(f'{mod_name} was not found!')
        return None
    else:
        if not comp:
            print(f'{comp_name} was not found!')
            return None
        elif comp.confirm:
            print(f'Results for {comp_name} have already been finalized!')
            return None
        elif mod not in comp.moderators:
            print(f'{mod_name} is not authorized to add results for {comp_name}!')
            return None
        else:
            for team in teams:
                comp_team = CompetitionTeam.query.filter_by(comp_id=comp.id, team_id=team.id).first()

                if comp_team:
                    comp_team.points_earned = score
                    comp_team.rating_score = (score/comp.max_score) * 20 * comp.level
                    try:
                        db.session.add(comp_team)
                        db.session.commit()
                        print(f'Score successfully added for {team_name}!')
                        return comp_team
                    except Exception as e:
                        db.session.rollback()
                        print("Something went wrong!")
                        return None
"""