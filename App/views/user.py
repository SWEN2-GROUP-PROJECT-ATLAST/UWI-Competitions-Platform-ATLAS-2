from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for, session
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required

from flask_login import login_required, login_user, current_user, logout_user

from.index import index_views

from App.controllers import *

user_views = Blueprint('user_views', __name__, template_folder='../templates')

# @user_views.route('/users', methods=['GET'])
# def get_user_page():
#     users = get_all_users()
#     return render_template('users.html', users=users)

@user_views.route('/api/users', methods=['GET'])
def get_users_action():
    users = get_all_students_json()
    return jsonify(users)

'''
@user_views.route('/api/users', methods=['POST'])
def create_user_endpoint():
    data = request.json
    response = create_user(data['username'], data['password'])
    if response:
        return (jsonify({'message': f"user created"}),201)
    return (jsonify({'error': f"error creating user"}),500)
'''
@user_views.route('/host_join', methods=['POST'])
def join_competition():
    data = request.json
    Hosting  = join_comp(data['username'], data['CompName'])
    if Hosting is None:
      return jsonify({'message': f"Error"}), 409
    return jsonify({'message': f" {Hosting.username} has joined {Hosting.CompName}"})

@user_views.route('/Create_Host', methods=['POST'])
def create_host_action():
    data = request.json
    Host  = create_host(data['username'], data['password'],data['host_id'])
    if Host is None:
      return jsonify({'message': f"user {data['username']} already exists"}), 409
    return jsonify({'message': f"user {Host.username} created"})

@user_views.route('/static/users', methods=['GET'])
def static_user_page():
  return send_from_directory('static', 'static-user.html')

@user_views.route('/tester', methods=['GET'])
def random_function():
    flash(f"hello user this test has been successful") 
    return "yes"

@user_views.route('/all_rankings', methods=['GET'])
def get_user_rankings():
    users = display_rankings()
    rankings = [u.to_dict() for u in users]
    return jsonify(rankings)

@user_views.route('/users/competitions/<string:username>', methods=['GET'])
def get_user_comps(username):
    # Call the display_student_info function with the provided username
    profile_info = display_student_info(username)
    
    if not profile_info:
        return jsonify({"error": f"User '{username}' not found or no competitions"}), 404
    
    # Return the student's profile information and competitions
    return jsonify(profile_info), 200



@user_views.route('/api/students', methods=['POST'])
def create_student_endpoint():
    data = request.json
    student  = create_student(data['username'], data['password'])
    if student is None:
      return jsonify({'message': f"user {data['username']} already exists"}), 409
    return jsonify({'message': f"user {student.username} created"})

@user_views.route('/create_competition', methods=['POST'])
def create_competition():
    data = request.json
    admin = Admin.query.filter_by(staff_id=data['CreatorId']).first()
    if admin:
      comp=get_competition_by_name(data['name'])
      if comp is None:
        comp=create_competition(data['name'], data['CreatorId'])
        return jsonify({'message': f"Competition {comp.name} created"})
      return jsonify({'message': f"Competition {comp.name} already exists"}), 409
    return jsonify({'message': f"Admin {data['CreatorId']} does not exist! Stop the shenanigans students"}), 409

@user_views.route('/AllNotifications', methods=['GET'])
def get_all_notifications():
    notifications = display_notifications()
    return jsonify(notifications)

@user_views.route('/students/<string:username>/rank-history', methods=['GET'])
def get_rank_history(username):
    student = get_student_by_username(username)

    if not student:
        return jsonify({"error": f"Student '{username}' not found!"}), 404

    rank_history = (
        RankHistory.query
        .filter_by(student_id=student.id)
        .order_by(RankHistory.date.desc())
        .all()
    )

    if not rank_history:
        return jsonify({"message": f"No rank history found for student '{username}'!"}), 200

    history_json = [rank.get_json() for rank in rank_history]

    return jsonify({"rank_history": history_json}), 200


from App.controllers.student import create_student

@user_views.route('/signup_student', methods=['POST'])
def signup_student():
    # Parse the input data
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Validate required fields
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    # Call the create_student function
    student = create_student(username, password)

    if student:
        return jsonify({'message': f'Student {student.username} created successfully!'}), 201
    return jsonify({'error': 'Error creating student'}), 500


@user_views.route('/login_refactored', methods=['POST'])
def user_login_api_refactored():
    data = request.json

    # Call the jwt_authenticate function to check username and password
    token = jwt_authenticate(data['username'], data['password'])
    
    if not token:
        return jsonify(error='bad username or password given'), 401
    
    # If authentication is successful, return the access token
    return jsonify(access_token=token)