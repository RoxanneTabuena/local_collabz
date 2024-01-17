from flask_app import app
from flask import Flask, render_template, redirect, session, request, flash
from flask_bcrypt import Bcrypt
from flask_app.models.user import User
from flask_app.models.skill import Skill
from flask_app.models.interest import Interest
from flask_app.models.city import City
from flask_app.models.project import Project
from flask_app.models.role import Role
from flask_app.models.notification import Notification
from flask_app.models.user_short import User_short
from flask_app.models.message import Message
from flask_app.models.conversation import Conversation
bcrypt = Bcrypt(app)

@app.route('/people')
def browse_people():
    skills = Skill.get_all()
    interests = Interest.get_all()
    user = User.retrieve_via_id(session['user_id'])
    liked = User.get_liked_profiles(session['user_id'])
    watched = User.get_watched_profiles(session['user_id'])
    profiles = User.get_all()
    people =[]
    for person in profiles:
        person = User.retrieve_via_id(person.id)
        person.skillset = User.get_skills(person.id)
        person.interests = User.get_interests(person.id)
        person.associated_projects = Project.associated_projects(person.id)
        if person.city_id:
            person.location = City.get_city(person.city_id)
        if person.id in liked:
            person.liked = True
        if person.id in watched:
            person.watched = True
        people.append(person)
    return render_template('people.html', user=user, people=people, skills = skills, interests = interests)

@app.route('/watchlist/people/<int:id>')
def watched_people(id):
    skills = Skill.get_all()
    interests = Interest.get_all()
    user = User.retrieve_via_id(id)
    liked = User.get_liked_profiles(id)
    watched = User.get_watched_profiles(id)
    profiles = User.get_watched(id)
    people =[]
    for person in profiles:
        person = User.retrieve_via_id(person.id)
        person.skillset = User.get_skills(person.id)
        person.interests = User.get_interests(person.id)
        person.associated_projects = Project.associated_projects(person.id)
        if person.city_id:
            person.location = City.get_city(person.city_id)
        if person.id in liked:
            person.liked = True
        if person.id in watched:
            person.watched = True
        people.append(person)
    return render_template('watch_people.html', user=user, people=people, skills = skills, interests = interests)

@app.route('/people/skills/<int:id>')
def browse_skilled_people(id):
    skills = Skill.get_all()
    interests = Interest.get_all()
    user = User.retrieve_via_id(session['user_id'])
    data = {'skill_id': id}
    people = User.get_all_skill(data)
    liked = User.get_liked_profiles(session['user_id'])
    watched = User.get_watched_profiles(session['user_id'])
    if people != False:
        for person in people:
            person.skillset = User.get_skills(person.id)
            person.interests = User.get_interests(person.id)
            person.associated_projects = Project.associated_projects(person.id)
            if person.city_id:
                person.location = City.get_city(person.city_id)
            if person.id in liked:
                person.liked = True
            if person.id in watched:
                person.watched = True
    return render_template('people.html', user=user, people=people, skills = skills, interests = interests)

@app.route('/people/interests/<int:id>')
def browse_interested_people(id):
    skills = Skill.get_all()
    interests = Interest.get_all()
    user = User.retrieve_via_id(session['user_id'])
    data = {'interest_id': id}
    people = User.get_all_interest(data)
    liked = User.get_liked_profiles(session['user_id'])
    watched = User.get_watched_profiles(session['user_id'])
    if people != False:
        for person in people:
            person.skillset = User.get_skills(person.id)
            person.interests = User.get_interests(person.id)
            person.associated_projects = Project.associated_projects(person.id)
            if person.city_id:
                person.location = City.get_city(person.city_id)
            if person.id in liked:
                person.liked = True
            if person.id in watched:
                person.watched = True
    return render_template('people.html', user=user, people=people, skills = skills, interests = interests)

@app.route('/people/new')
def browse_new_people():
    skills = Skill.get_all()
    interests = Interest.get_all()
    user = User.retrieve_via_id(session['user_id'])
    people = User.get_all_new()
    liked = User.get_liked_profiles(session['user_id'])
    watched = User.get_watched_profiles(session['user_id'])
    for person in people:
        person.skillset = User.get_skills(person.id)
        person.interests = User.get_interests(person.id)
        person.associated_projects = Project.associated_projects(person.id)
        if person.city_id:
            person.location = City.get_city(person.city_id)
        if person.id in liked:
            person.liked = True
        if person.id in watched:
            person.watched = True
    return render_template('people.html', user=user, people=people, skills = skills, interests = interests)

@app.route('/people/hot')
def browse_hot_people():
    skills = Skill.get_all()
    interests = Interest.get_all()
    user = User.retrieve_via_id(session['user_id'])
    people = User.get_all_hot()
    liked = User.get_liked_profiles(session['user_id'])
    watched = User.get_watched_profiles(session['user_id'])
    for person in people:
        person.skillset = User.get_skills(person.id)
        person.interests = User.get_interests(person.id)
        person.associated_projects = Project.associated_projects(person.id)
        if person.city_id:
            person.location = City.get_city(person.city_id)
        if person.id in liked:
            person.liked = True
        if person.id in watched:
            person.watched = True
    return render_template('people.html', user=user, people=people, skills = skills, interests = interests)

@app.route('/people/location/<int:id>')
def browse_close_people(id):
    skills = Skill.get_all()
    interests = Interest.get_all()
    user = User.retrieve_via_id(session['user_id'])
    added = []
    people = []
    data = {'city_id' : id }
    city = User.get_city(data)
    for homie in city:
        people.append(homie)
        added.append(homie.id)
    area = City.get_area(data)
    data = {'area' : area}
    area = User.get_area(data)
    for homie in area:
        if homie.id not in added:
            people.append(homie)
            added.append(homie.id)
    others = User.get_all_hot()
    for homie in others:
        if homie.id not in added:
            people.append(homie)
            added.append(homie.id)
    liked = User.get_liked_profiles(session['user_id'])
    watched = User.get_watched_profiles(session['user_id'])
    for person in people:
        person.skillset = User.get_skills(person.id)
        person.interests = User.get_interests(person.id)
        person.associated_projects = Project.associated_projects(person.id)
        if person.city_id:
            person.location = City.get_city(person.city_id)
        if person.id in liked:
            person.liked = True
        if person.id in watched:
            person.watched = True
    return render_template('people.html', user=user, people=people, skills = skills, interests = interests)

@app.route('/profile/<int:id>')
def profile(id):
    user = User.retrieve_via_id(session['user_id'])
    person = User.retrieve_via_id(id)
    person.skillset = User.get_skills(id)
    person.interests = User.get_interests(id)
    if person.city_id:
        person.location = City.get_city(person.city_id)
    person.associated_projects = Project.associated_projects(id)
    liked_people = User.get_liked_profiles(session['user_id'])
    if id in liked_people:
        person.liked = True
    watched_people = User.get_watched_profiles(session['user_id'])
    if id in watched_people:
        person.watched = True
    for project in person.associated_projects:
        id = project.id
        project.team = Role.get_team(id)
        project.needed_roles = Role.get_project(id)
        for role in project.needed_roles:
            role.skillset = Skill.get_role_skillset(role.id)
    return render_template('profile.html', user=user, person=person, watched_people=watched_people)

@app.route('/profile/like/<int:id>', methods=['POST'])
def like_profile(id):
    data = {
        'liker_id' : session['user_id'],
        'likee_id' : id
    }
    User.like_profile(data)
    user = User.retrieve_via_id(session['user_id'])
    user.score += 1
    data = {
        'id' : user.id,
        'score' : user.score
    }
    User.update_score(data)
    return redirect('/profile/'+str(id))

@app.route('/profile/unlike/<int:id>', methods=['POST'])
def unlike_profile(id):
    data = {
        'liker_id' : session['user_id'],
        'likee_id' : id
    }
    User.unlike_profile(data)
    return redirect('/profile/'+str(id))

@app.route('/profile/watch/<int:id>', methods=['POST'])
def watch_profile(id):
    data = {
        'watcher_id' : session['user_id'],
        'watchee_id' : id
    }
    User.watch_profile(data)
    user = User.retrieve_via_id(session['user_id'])
    user.score += 1
    data = {
        'id' : user.id,
        'score' : user.score
    }
    User.update_score(data)
    return redirect('/profile/'+str(id))

@app.route('/profile/unwatch/<int:id>', methods=['POST'])
def unwatch_profile(id):
    data = {
        'watcher_id' : session['user_id'],
        'watchee_id' : id
    }
    User.unwatch_profile(data)
    return redirect('/profile/'+str(id))

