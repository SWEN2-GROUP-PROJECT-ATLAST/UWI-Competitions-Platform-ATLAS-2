from App.database import db
from App.models import Competition, Moderator, CompetitionTeam, CompetitionModerator, Student#, Student, Admin, competition_student
from datetime import datetime
from . import moderator

def create_competition(mod_name, comp_name, date, location, level, max_score):
    comp = get_competition_by_name(comp_name)
    if comp:
        print(f'{comp_name} already exists!')
        return None
    
    mod = moderator.get_moderator_by_username(mod_name)
    
    if mod:
        newComp = Competition(name=comp_name, date=datetime.strptime(date, "%d-%m-%Y"), location=location, level=level, max_score=max_score)
        # comp_mod = CompetitionModerator(newComp.id,mod.id)
        try:
            newComp.add_mod(mod.id)
            db.session.add(newComp)
            db.session.commit()
            print(f'New Competition: {comp_name} created!')
            return newComp
        except Exception as e:
            db.session.rollback()
            print("Something went wrong!")
            return None
    else:
        print("Invalid credentials!")

def get_competition_by_name(name):
    return Competition.query.filter_by(name=name).first()

def get_competition(id):
    return Competition.query.get(id)

def get_all_competitions():
    return Competition.query.all()

def get_all_competitions_json():
    competitions = Competition.query.all()

    if not competitions:
        return []
    else:
        return [comp.get_json() for comp in competitions]

def display_competition_results(name):
    comp = get_competition_by_name(name)
    
    if not comp:
        print(f'{name} was not found!')
        return None
    elif len(comp.teams) == 0:
        print(f'No teams found for {name}!')
        return []
    else:
        comp_teams = CompetitionTeam.query.filter_by(comp_id=comp.id,hasResult = True).all()
        comp_teams.sort(key=lambda x: x.result[0].score, reverse=True)

        leaderboard = []
        count = 1
        curr_high = comp_teams[0].result[0].score
        curr_rank = 1
        
        for comp_team in comp_teams:
            if curr_high != comp_team.result[0].score:
                curr_rank = count
                curr_high = comp_team.result[0].score

           
            leaderboard.append({"placement": curr_rank, "team": comp_team.name, "members" : [student.username for student in comp_team.members], "score":comp_team.result[0].score})
            count += 1
        
        return leaderboard