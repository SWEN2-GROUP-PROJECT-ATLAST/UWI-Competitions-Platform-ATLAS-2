import csv
import click, pytest, sys
from flask import Flask
from datetime import datetime, date

from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.main import create_app
from App.controllers import *


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    db.drop_all()
    db.create_all()

    # Create students from CSV
    with open("students.csv") as student_file:
        reader = csv.DictReader(student_file)
        for student in reader:
            create_student(student['username'], student['password'])
    
    # Create moderators from CSV
    with open("moderators.csv") as moderator_file:
        reader = csv.DictReader(moderator_file)
        for moderator in reader:
            create_moderator(moderator['username'], moderator['password'])
    
    # Create competitions from CSV
    with open("competitions.csv") as competition_file:
        reader = csv.DictReader(competition_file)
        for competition in reader:
            create_competition(
                competition['mod_name'], competition['comp_name'], competition['date'],
                competition['location'], competition['level'], competition['max_score']
            )
    
    # Add teams and results from CSV
    with open("results.csv") as results_file:
        reader = csv.DictReader(results_file)
        for result in reader:
            students = [result['student1'], result['student2'], result['student3']]
            create_team( result['comp_name'], result['team_name'], students)
            add_result(result['mod_name'], result['comp_name'], result['team_name'], int(result['score']))

    # Update ratings and rankings for competitions
    with open("competitions.csv") as competitions_file:
        reader = csv.DictReader(competitions_file)
        for competition in reader:
            if competition['comp_name'] != 'TopCoder':
                update_ratings(competition['mod_name'], competition['comp_name'])
        update_rankings()

    print('Database initialized')


# Student CLI commands
student_cli = AppGroup("student", help="Student commands")

@student_cli.command("create", help="Creates a student")
@click.argument("username")
@click.argument("password")
def create_student_command(username, password):
    create_student(username, password)

@student_cli.command("update", help="Updates a student's username")
@click.argument("id")
@click.argument("username")
def update_student_command(id, username):
    update_student(id, username)

@student_cli.command("list", help="Lists students in the database")
@click.argument("format", default="string")
def list_students_command(format):
    if format == 'string':
        print(get_all_students())
    else:
        print(get_all_students_json())

@student_cli.command("display", help="Displays student profile")
@click.argument("username")
def display_student_info_command(username):
    print(display_student_info(username))

@student_cli.command("notifications", help="Gets all notifications")
@click.argument("username")
def display_notifications_command(username):
    print(display_notifications(username))

app.cli.add_command(student_cli)


# Moderator CLI commands
mod_cli = AppGroup("mod", help="Moderator commands")

@mod_cli.command("create", help="Creates a moderator")
@click.argument("username")
@click.argument("password")
def create_moderator_command(username, password):
    create_moderator(username, password)

@mod_cli.command("addMod", help="Adds a moderator to a competition")
@click.argument("mod1_name")
@click.argument("comp_name")
@click.argument("mod2_name")
def add_mod_to_comp_command(mod1_name, comp_name, mod2_name):
    add_moderatr_to_competition(mod1_name, comp_name, mod2_name)

@mod_cli.command("addResults", help="Adds results for a team in a competition")
@click.argument("mod_name")
@click.argument("comp_name")
@click.argument("team_name")
@click.argument("student1")
@click.argument("student2")
@click.argument("student3")
@click.argument("score", type=int)
def add_results_command(mod_name, comp_name, team_name, student1, student2, student3, score):
    students = [student1, student2, student3]
    create_team(comp_name, team_name, students)
    add_result(mod_name, comp_name, team_name, score)

@mod_cli.command("confirm", help="Confirms results for all teams in a competition")
@click.argument("mod_name")
@click.argument("comp_name")
def update_rankings_command(mod_name, comp_name):
    update_ratings(mod_name, comp_name)
    update_rankings()

@mod_cli.command("rankings", help="Displays overall rankings")
def display_rankings_command():
    display_rankings()

@mod_cli.command("list", help="Lists moderators in the database")
@click.argument("format", default="string")
def list_moderators_command(format):
    if format == 'string':
        print(get_all_moderators())
    else:
        print(get_all_moderators_json())

app.cli.add_command(mod_cli)


# Competition CLI commands
comp_cli = AppGroup("comp", help="Competition commands")

@comp_cli.command("create", help="Creates a competition")
@click.argument("mod_name")
@click.argument("name")
@click.argument("date")
@click.argument("location")
@click.argument("level", type=int)
@click.argument("max_score", type=int)
def create_competition_command(mod_name, name, date, location, level, max_score):
    create_competition(mod_name, name, date, location, level, max_score)

@comp_cli.command("details", help="Displays competition details")
@click.argument("name")
def display_competition_details_command(name):
    comp = get_competition_by_name(name)
    print(comp.get_json())

@comp_cli.command("list", help="Lists all competitions")
def list_competition_command():
    print(get_all_competitions_json())

@comp_cli.command("results", help="Displays competition results")
@click.argument("name")
def display_competition_results_command(name):
    print(display_competition_results(name))

app.cli.add_command(comp_cli)


# Test CLI commands
test = AppGroup('test', help='Testing commands')

@test.command("app", help="Run tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "IntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))

app.cli.add_command(test)