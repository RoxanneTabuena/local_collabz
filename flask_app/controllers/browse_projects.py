from flask_app import app
from flask import Flask, render_template, redirect, session, request, flash
from flask_app.models.project import Project
from flask_app.models.skill import Skill
from flask_app.models.interest import Interest
from flask_app.models.user import User
from flask_app.models.role import Role
from flask_app.models.notification import Notification
from flask_app.models.conversation import Conversation

@app.route('/project/<int:id>')
def project(id):
    user = User.retrieve_via_id(session['user_id'])
    project = Project.get_one(id)
    data = {
        'project_id' : project.id,
        'user_id' : user.id
    }
    user.on_project = Role.on_project(data)
    notifications = False
    project.news = Notification.project_news(data)
    if project.news:
        notifications = Notification.project_notifications(data)
    if not project.about:
        project.about = False
    else:
        project.aboutfmat = project.about.split('\r\n\r\n')
    project.team = User.get_team(id)
    for person in project.team:
        data = {
            'user_id' : person.id,
            'project_id' : id
        }
        person.roles = Role.get_roles(data)
    project.needed_roles = Role.get_project(id)
    project.organizers = Project.get_organizers(id)
    for role in project.needed_roles:
        role.skillset = Skill.get_role_skillset(role.id)
        data = {
            'user_id' : session['user_id'],
            'role_id' : role.id
        }
        role.offered = Role.volunteered(data)
    liked = User.get_liked_projects(user.id)
    watched = User.get_watched_projects(user.id)
    if project.id in liked:
        project.liked = True
    if project.id in watched:
        project.watched = True
    types = Interest.get_all()
    skills = Skill.get_all()
    return render_template('/project.html', project = project, user=user, types=types, skills=skills, notifications = notifications)

@app.route('/projects')
def browse_projects():
    user = User.retrieve_via_id(session['user_id'])
    projects = Project.get_all()
    for project in projects:
        id = project.id
        project.team = User.get_team(id)
        project.needed_roles = Role.get_project(id)
        for role in project.needed_roles:
            role.skillset = Skill.get_role_skillset(role.id)
        liked = User.get_liked_projects(user.id)
        watched = User.get_watched_projects(user.id)
        if project.id in liked:
            project.liked = True
        if project.id in watched:
            project.watched = True
    return render_template('/projects.html', projects = projects, user=user)

@app.route('/watchlist/projects/<int:id>')
def watched_projects(id):
    user = User.retrieve_via_id(session['user_id'])
    projects = Project.get_watched(id)
    for project in projects:
        id = project.id
        project.team = Role.get_team(id)
        project.needed_roles = Role.get_project(id)
        for role in project.needed_roles:
            role.skillset = Skill.get_role_skillset(role.id)
        liked = User.get_liked_projects(user.id)
        watched = User.get_watched_projects(user.id)
        if project.id in liked:
            project.liked = True
        if project.id in watched:
            project.watched = True
    return render_template('/watch_projects.html', projects = projects, user=user)

@app.route('/project/like/<int:id>', methods=['POST'])
def like_project(id):
    data = {
        'user_id' : session['user_id'],
        'project_id' : id
    }
    User.like_project(data)
    project = Project.get_one(id)
    project.score += 1
    data = {
        'id' : project.id,
        'score' : project.score
    }
    Project.update_score(data)
    return redirect('/project/'+str(id))

@app.route('/project/unlike/<int:id>', methods=['POST'])
def unlike_project(id):
    data = {
        'user_id' : session['user_id'],
        'project_id' : id
    }
    User.unlike_project(data)
    return redirect('/project/'+str(id))

@app.route('/project/watch/<int:id>', methods=['POST'])
def watch_project(id):
    data = {
        'user_id' : session['user_id'],
        'project_id' : id
    }
    User.watch_project(data)
    project = Project.get_one(id)
    project.score += 1
    data = {
        'id' : project.id,
        'score' : project.score
    }
    Project.update_score(data)
    return redirect('/project/'+str(id))

@app.route('/project/unwatch/<int:id>', methods=['POST'])
def unwatch_project(id):
    data = {
        'user_id' : session['user_id'],
        'project_id' : id
    }
    User.unwatch_project(data)
    return redirect('/project/'+str(id))

