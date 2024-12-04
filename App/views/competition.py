from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for, session
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required
#from datetime import datetime

from.index import index_views

from App.controllers import *

comp_views = Blueprint('comp_views', __name__, template_folder='../templates')

##return the json list of competitions fetched from the db
@comp_views.route('/competitions', methods=['GET'])
def get_competitions():
    if request.headers.get('Accept') == 'application/json':  # Check if JSON is expected
        competitions = get_all_competitions_json()
        return jsonify(competitions), 200
    else:
        return render_template('competitions.html', competitions=get_all_competitions(), user=current_user)
'''
##add new competition to the db
@comp_views.route('/competitions', methods=['POST'])
def add_new_comp():
    data = request.json
    response = create_competition(data['name'], data['date'], data['location'], data['level'], data['max score'])
    if response:
        return (jsonify({'message': "Competition created!"}), 201)
    return (jsonify({'error': "Error creating competition"}),500)
'''

#create new comp
@comp_views.route('/createcompetition', methods=['POST'])
@login_required
def create_comp():
    data = request.form
    
    if session['user_type'] == 'moderator':
        moderator = Moderator.query.filter_by(id=current_user.id).first()
    else:
        moderator = None

    date = data['date']
    date = date[8] + date[9] + '-' + date[5] + date[6] + '-' + date[0] + date[1] + date[2] + date[3]
    
    response = create_competition(moderator.username, data['name'], date, data['location'], data['level'], data['max_score'])
    return render_template('competitions.html', competitions=get_all_competitions(), user=current_user)
    #return (jsonify({'message': "Competition created!"}), 201)
    #return (jsonify({'error': "Error creating competition"}),500)
    #return render_template('competitions.html', competitions=get_all_competitions())

#page to create new comp
@comp_views.route('/createcompetition', methods=['GET'])
def create_comp_page():
    return render_template('competition_creation.html', user=current_user)

"""
@comp_views.route('/competitions/moderator', methods=['POST'])
def add_comp_moderator():
    data = request.json
    response = add_mod()
    if response: 
        return (jsonify({'message': f"user added to competition"}),201)
    return (jsonify({'error': f"error adding user to competition"}),500)
"""
@comp_views.route('/competitions/<int:id>', methods=['GET'])
def competition_details(id):
    competition = get_competition(id)
    if not competition:
        return render_template('404.html')
    
    #team = get_all_teams()

    #teams = get_participants(competition_name)
    if current_user.is_authenticated:
        if session['user_type'] == 'moderator':
            moderator = Moderator.query.filter_by(id=current_user.id).first()
        else:
            moderator = None
    else:
        moderator = None
    
    leaderboard = display_competition_results(competition.name)
    return render_template('competition_details.html', competition=competition, moderator=moderator, leaderboard=leaderboard, user=current_user)#, team=team)

    #teams = get_participants(competition_name)
    #return render_template('Competition_Details.html', competition=competition)
    """
@index_views.route('/competition/<string:name>', methods=['GET'])
def competition_details(name):
    competition = get_competition_by_name(name)
    if not competition:
        return render_template('404.html')

    #teams = get_participants(competition_name)
    return render_template('competition_details.html', competition=competition)
"""
@comp_views.route('/competition/<string:name>', methods=['GET'])
def competition_details_by_name(name):
    competition = get_competition_by_name(name)
    if not competition:
        return render_template('404.html')

    #teams = get_participants(competition_name)
    if current_user.is_authenticated:
        if session['user_type'] == 'moderator':
            moderator = Moderator.query.filter_by(id=current_user.id).first()
        else:
            moderator = None
    else:
        moderator = None
    
    leaderboard = display_competition_results(name)

    return render_template('competition_details.html', competition=competition, moderator=moderator, leaderboard=leaderboard, user=current_user)
    
    """
@comp_views.route('/competitions/results', methods=['POST'])
def add_comp_results():
    data = request.json
    response = add_results(data['mod_name'], data['comp_name'], data['team_name'], data['score'])
    if response:
        return (jsonify({'message': "Results added successfully!"}),201)
    return (jsonify({'error': "Error adding results!"}),500)

@comp_views.route('/competitions/results/<int:id>', methods =['GET'])
def get_results(id):
    competition = get_competition(id)
    leaderboard = display_competition_results(competition.name)
    if not leaderboard:
        return jsonify({'error': 'Leaderboard not found!'}), 404 
    return (jsonify(leaderboard),200)
"""
#page to comp upload comp results
@comp_views.route('/add_results/<int:comp_id>', methods=['GET'])
def add_results_page(comp_id):
    competition = get_competition(comp_id)
    if session['user_type'] == 'moderator':
        moderator = Moderator.query.filter_by(id=current_user.id).first()
    else:
        moderator = None

    leaderboard = display_competition_results(competition.name)

    return render_template('competition_results.html', competition=competition, moderator=moderator, leaderboard=leaderboard, user=current_user)

@comp_views.route('/add_results/<string:comp_name>', methods=['POST'])
def add_competition_results(comp_name):
    competition = get_competition_by_name(comp_name)
    if session['user_type'] == 'moderator':
        moderator = Moderator.query.filter_by(id=current_user.id).first()
    else:
        moderator = None
        
    #if request.method == 'POST':
    data = request.form
    
    students = [data['student1'], data['student2'], data['student3']]
    response = add_team(moderator.username, comp_name, data['team_name'], students)

    if response:
        response = add_results(moderator.username, comp_name, data['team_name'], int(data['score']))
    #response = add_results(data['mod_name'], data['comp_name'], data['team_name'], int(data['score']))
    #if response:
    #    return (jsonify({'message': "Results added successfully!"}),201)
    #return (jsonify({'error': "Error adding results!"}),500)
    
    leaderboard = display_competition_results(comp_name)

    return render_template('competition_details.html', competition=competition, moderator=moderator, leaderboard=leaderboard, user=current_user)
    
@comp_views.route('/confirm_results/<string:comp_name>', methods=['GET', 'POST'])
def confirm_results(comp_name):
    if session['user_type'] == 'moderator':
        moderator = Moderator.query.filter_by(id=current_user.id).first()
    else:
        moderator = None
    
    competition = get_competition_by_name(comp_name)

    if update_ratings(moderator.username, competition.name):
        update_rankings()

    leaderboard = display_competition_results(comp_name)

    return render_template('competition_details.html', competition=competition, moderator=moderator, leaderboard=leaderboard, user=current_user)
"""
@comp_views.route('/confirm_results/<string:comp_name>', methods=['POST'])
def confirm_results(comp_name):
    pass
"""

@comp_views.route('/competitions_postman', methods=['GET'])
def get_competitions_postman():
    competitions = get_all_competitions_json()
    return (jsonify(competitions),200)

@comp_views.route('/createcompetition_postman', methods=['POST'])
def create_comp_postman():
    print(f"Request Method: {request.method}")  # Log the request method
    if request.method == 'GET':
        return "GET method received but not supported", 405
    data = request.json
    response = create_competition('robert', data['name'], data['date'], data['location'], data['level'], data['max_score'])
    if response:
        return jsonify({'message': "Competition created!"}), 201
    return jsonify({'error': "Error creating competition"}), 500

@comp_views.route('/competitions_postman/<int:id>', methods=['GET'])
def competition_details_postman(id):
    competition = get_competition(id)
    if not competition:
        return (jsonify({'error': "Competition not found"}),404)
    
    
    if current_user.is_authenticated:
        if session['user_type'] == 'moderator':
            moderator = Moderator.query.filter_by(id=current_user.id).first()
        else:
            moderator = None
    else:
        moderator = None
    
    leaderboard = display_competition_results(competition.name)
    return (jsonify(competition.toDict()),200)

# Display Competition Result of given comp name
@comp_views.route('/competitions/<string:name>/results', methods=['GET'])
def get_competition_results(name):
    leaderboard = display_competition_results(name)

    if leaderboard is None:
        return jsonify({"error": f"Competition '{name}' not found!"}), 404
    elif len(leaderboard) == 0:
        return jsonify({"message": f"No teams found for competition '{name}'!"}), 200

    return jsonify({"leaderboard": leaderboard}), 200

@comp_views.route('/add_results_postman/<string:comp_name>', methods=['POST'])
def add_competition_results_postman(comp_name):
    competition = get_competition_by_name(comp_name)
    
    data = request.json
    
    students = [data['student1'], data['student2'], data['student3']]
    response = add_team('robert', comp_name, data['team_name'], students)

    if response:
        response = add_results('robert', comp_name, data['team_name'], int(data['score']))
    if response:
        return (jsonify({'message': "Results added successfully!"}),201)
    return (jsonify({'error': "Error adding results!"}),500)


from App.models import Moderator
from App.controllers.moderator import create_moderator

@comp_views.route('/create_moderator', methods=['POST'])
def create_moderator_postman():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Ensure that both username and password are provided
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    mod = create_moderator(username, password)
    if mod:
        return jsonify({'message': f'Moderator {mod.username} created successfully!'}), 201
    return jsonify({'error': 'Error creating moderator'}), 500


from App.models import Competition
from App.controllers.moderator import get_moderator_by_username
from App.controllers.competition import create_competition

@comp_views.route('/create_competition_refactored', methods=['POST'])
def create_comp_refactored():
    # Parse input data
    data = request.json
    mod_name = data.get('mod_name')
    comp_name = data.get('comp_name')
    date = data.get('date')
    location = data.get('location')
    level = data.get('level')
    max_score = data.get('max_score')

    # Validate required fields
    if not mod_name or not comp_name or not date or not location or not level or not max_score:
        return jsonify({'error': 'All fields are required'}), 400

    # Call the create_competition function
    competition = create_competition(mod_name, comp_name, date, location, level, max_score)

    if competition:
        return jsonify({'message': f'Competition {competition.name} created successfully!'}), 201
    return jsonify({'error': 'Error creating competition'}), 500


@comp_views.route('/add_competition_results_refactored', methods=['POST'])
def add_comp_results():
    data = request.json
    # Validate that all necessary data is provided
    if 'mod_name' not in data or 'comp_name' not in data or 'team_name' not in data or 'score' not in data:
        return jsonify({'error': 'Missing data'}), 400

    print(f"Received data: {data}")  # Debugging output

    # Call the add_result method from the controller
    response = add_result(data['mod_name'], data['comp_name'], data['team_name'], data['score'])

    if response:
        return jsonify({'message': "Results added successfully!"}), 201
    return jsonify({'error': "Error adding results!"}), 500

