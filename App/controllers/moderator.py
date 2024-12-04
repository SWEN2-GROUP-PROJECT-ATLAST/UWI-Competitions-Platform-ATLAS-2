from App.database import db
from App.models import Moderator, Competition, CompetitionResult, CompetitionTeam
from sqlalchemy.exc import IntegrityError

def create_moderator(username, password):
    mod = get_moderator_by_username(username)
    if mod:
        print(f'{username} already exists!')
        return None

    newMod = Moderator(username=username, password=password)

    try:
        db.session.add(newMod)
        db.session.commit()
        print(f'New Moderator: {newMod.username} created!')
        return newMod
    except IntegrityError as e:
        db.session.rollback()
        print(f'Something went wrong creating {username}')
        return None

def get_moderator_by_username(username):
    return Moderator.query.filter_by(username=username).first()

def get_moderator(id):
    return Moderator.query.get(id)

def get_all_moderators():
    return Moderator.query.all()

def get_all_moderators_json():
    mods = Moderator.query.all()
    if not mods:
        return []
    mods_json = [mod.get_json() for mod in mods]
    return mods_json

def update_moderator(id, username):
    mod = get_moderator(id)
    if mod:
        mod.username = username
        try:
            db.session.add(mod)
            db.session.commit()
            print("Username was updated!")
            return mod
        except IntegrityError as e:
            db.session.rollback()
            print("Username was not updated!")
            return None
    print("ID: {id} does not exist!")
    return None

def add_moderatr_to_competition(mod1_name, comp_name, mod2_name):
    mod1 = Moderator.query.filter_by(username=mod1_name).first()
    comp = Competition.query.filter_by(name=comp_name).first()
    mod2 = Moderator.query.filter_by(username=mod2_name).first()

    if not mod1:
        print(f'Moderator: {mod1_name} not found!')
        return None
    elif not comp:
        print(f'Competition: {comp_name} not found!')
        return None
    elif not mod2:
        print(f'Moderator: {mod2_name} not found!')
        return None
    elif not mod1 in comp.moderators:
        print(f'{mod1_name} is not authorized to add results for {comp_name}!')
        return None
    else:
        return comp.add_mod(mod2)
                
def add_result(moderator_name, competition_name, team_name, score):
    # Step 1: Validate the moderator
    moderator = get_moderator_by_username(moderator_name)
    if not moderator:
        print(f"Moderator '{moderator_name}' not found!")
        return None

    # Step 2: Validate the competition
    competition = Competition.query.filter_by(name=competition_name).first()
    if not competition:
        print(f"Competition '{competition_name}' not found!")
        return None

    # Step 3: Check if the moderator is associated with the competition
    if moderator not in competition.moderators:
        print(f"Moderator '{moderator_name}' is not associated with competition '{competition_name}'")
        return None

    # Step 4: Validate the team within the competition
    team = CompetitionTeam.query.filter_by(name=team_name, comp_id=competition.id).first()
    if not team:
        print(f"Team '{team_name}' not found in competition '{competition_name}'")
        return None

    # Step 5: Check for existing result for the team in the same competition
    existing_result = CompetitionResult.query.filter_by(comp_team_id=team.id).first()
    if existing_result:
        print(f"Updating existing result for team '{team_name}' in competition '{competition_name}'")
        existing_result.score = score  # Update the score
        db.session.commit()
        return existing_result  # Return the updated result

    # Step 6: Add the competition result if no existing result is found
    team.hasResult = True
    new_result = CompetitionResult(comp_team_id=team.id, score=score)
    db.session.add(new_result)
    db.session.add(team)
    db.session.commit()
    print(f"Result added for team '{team_name}' with score {score}")
    return new_result




def update_ratings(mod_name, comp_name):
    mod = Moderator.query.filter_by(username=mod_name).first()
    comp = Competition.query.filter_by(name=comp_name).first()

    if not mod:
        print(f'{mod_name} was not found!')
        return None
    elif not comp:
        print(f'{comp_name} was not found!')
        return None
    elif mod not in comp.moderators:
        print(f'{mod_name} is not authorized to add results for {comp_name}!')
        return None
    elif len(comp.teams) == 0:
        print(f'No teams found. Results can not be confirmed!')
        return None
    else:
        comp_teams = CompetitionTeam.query.filter_by(comp_id=comp.id,hasResult = True).all()

        for comp_team in comp_teams:

            for stud in comp_team.members:
                stud.rating += round((comp_team.result[0].score / comp.max_score) * 10,0)
                try:
                    db.session.add(stud)
                    db.session.commit()
                except IntegrityError as e:
                    db.session.rollback()

        
        print("Results finalized!")
        return True
