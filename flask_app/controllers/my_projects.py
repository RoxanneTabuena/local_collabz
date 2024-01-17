from flask_app import app
from flask import Flask, render_template, redirect, session, request, flash
from flask_app.models.project import Project
from flask_app.models.skill import Skill
from flask_app.models.interest import Interest
from flask_app.models.user import User
from flask_app.models.role import Role
from flask_app.models.notification import Notification
from flask_app.models.conversation import Conversation

@app.route('/projects/user/<int:id>')
def my_projects(id):
    user = User.retrieve_via_id(id)
    projects = Project.associated_projects(id)
    for project in projects:
        id = project.id
        data = {
            'user_id': user.id,
            'project_id' :id
        }
        project.news = Notification.project_news(data)
        project.team = User.get_team(id)
        project.organizers = Project.get_organizers(id)
        for person in project.team:
            data = {
                'user_id' : person.id,
                'project_id' : id
            }
            person.roles = Role.get_roles(data)
        project.needed_roles = Role.get_project(id)
        for role in project.needed_roles:
            role.skillset = Skill.get_role_skillset(role.id)
        project.volunteers = Project.count_volunteers(id)
    return render_template('/my_projects.html', projects = projects, user=user)

@app.route('/dismiss/projectpage/<int:id>', methods = ['POST'])
def dismiss_update(id):
    Notification.dismiss(id)
    id = request.form['project']
    return redirect ('/project/' + str(id))

@app.route('/projects/new/<int:id>')
def new_project(id):
    user = User.retrieve_via_id(id)
    # user.has_organized = Project.has_organized(id)
    types = Interest.get_all()
    return render_template('/new_project.html', user=user, types = types)

@app.route('/create_project/<int:id>', methods=['POST'])
def create_project(id):
    data= {
        'title' : request.form['title'],
        'mission' : request.form['mission']
    }
    # Creating and retrieve project Chat
    Conversation.new(data)
    chat = Conversation.get_from_title(data)
    # create and retrieve project
    Project.create(data)
    project = Project.retrieve(data)
    # add project founder, associate project to creator, and assign creator as an organizer
    data = {
        'user_id': id,
        'project_id': project.id
    }
    Project.found(data)
    Project.associate(data)
    Role.organize(data)
    # add creator to project chat
    data = {
        'user_id' : session['user_id'],
        'conversation_id' : chat.id
    }
    Conversation.add_person(data)
    # associate project with chat
    data = {
        'id' : project.id,
        'chat_id' : chat.id
    }
    Project.associate_chat(data)
    return redirect('/project/'+ str(project.id))

@app.route('/project/edit/<int:id>')
def edit_project(id):
    user = User.retrieve_via_id(session['user_id'])
    project = Project.get_one(id)
    roles = Project.get_roles(id)
    p_roles = ['organizer']
    project.roles = []
    for role in roles:
        if role.title not in p_roles:
            project.roles.append(role)
            p_roles.append(role.title)
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
        role.volunteers = Role.get_volunteers(role.id)
    liked = User.get_liked_projects(user.id)
    watched = User.get_watched_projects(user.id)
    if project.id in liked:
        project.liked = True
    if project.id in watched:
        project.watched = True
    types = Interest.get_all()
    skills = Skill.get_all()
    return render_template('/edit_project.html', project = project, user=user, types=types, skills=skills)

@app.route('/update_project/<int:id>', methods = ['POST'])
def update_project(id):
    data= {
        'title' : request.form['title'],
        'mission' : request.form['mission'],
        'project_id' : id,
        'about' : request.form['about']
    }
    Project.update(data)
    Project.about(data)
    flash('Project updated')
    return redirect('/project/edit/' + str(id))
@app.route('/project/about/<int:id>', methods = ['POST'])

@app.route('/make_public/<int:id>', methods = ['POST'])
def public(id):
    Project.make_public(id)
    return redirect('/project/edit/' + str(id))

@app.route('/make_private/<int:id>', methods = ['POST'])
def private(id):
    Project.make_private(id)
    return redirect('/project/edit/' + str(id))

@app.route('/update_status/<int:id>', methods = ['POST'])
def status(id):
    data = {
        'id': id,
        'status' : request.form['status']
    }
    Project.update_status(data)
    project = Project.get_one(id)
    user = User.retrieve_via_id(session['user_id'])
    associated = User.get_team(id)
    for member in associated:
        data = {
            'reciever_id' : member.id,
            'notification' : f"{user.alias} has updated {project.title}'s status to {project.status}",
            'type' : "status updates",
            'project_id' : id,
            'teammate_alias' : user.alias,
            'teammate_id' : user.id,
            'role_id' : '0'
        }
        Notification.create(data)
    return redirect('/project/edit/' + str(id))

@app.route('/update_type/<int:id>', methods = ['POST'])
def type(id):
    data = { 'id' :request.form['type']}
    type = Interest.get_by_id(data)
    data = {
        'id': id,
        'type' : type.interest
    }
    Project.update_type(data)
    data = {
        'id' : type.id
    }
    interest = Interest.get_by_id(data)
    score = interest.score + 1
    data['score'] = score
    Interest.update_score(data)
    project = Project.get_one(id)
    user = User.retrieve_via_id(session['user_id'])
    associated = User.get_team(id)
    for member in associated:
        data = {
            'reciever_id' : member.id,
            'notification' : f"{user.alias} has updated {project.title}'s project type to {project.type}",
            'type' : "updates",
            'project_id' : id,
            'teammate_alias' : user.alias,
            'teammate_id' : user.id,
            'role_id' : '0'
        }
        Notification.create(data)
    return redirect('/project/edit/' + str(id))

@app.route('/recruit/<int:id>', methods = ['POST'])
def recruit(id):
    Project.recruit(id)
    return redirect('/project/edit/' + str(id))

@app.route('/dont_recruit/<int:id>', methods = ['POST'])
def dont_recruit(id):
    Project.dont_recruit(id)
    return redirect('/project/edit/' + str(id))

@app.route('/project/about/<int:id>', methods = ['POST'])
def about(id):
    data = {
        'id' : id,
        'about' : request.form['about']
    }
    Project.about(data)
    return redirect('/project/edit/' + str(id))

@app.route('/create_type/<int:p_id>', methods=['POST'])
def create_type(p_id):
    user = User.retrieve_via_id(session['user_id'])
    interest = request.form['interest'].lower()
    data = {'interest' : interest,
            'id' : user.id}
    Interest.create(data)
    interest = Interest.get_one(interest)
    data['interest_id'] = interest.id
    data['user_id'] = id
    User.add_interest(data)
    user.score += 2
    data = {
        'id' : user.id,
        'score' : user.score
    }
    User.update_score(data)
    data = {
        'id': p_id,
        'type' : interest.interest
    }
    Project.update_type(data)
    return redirect ('/project/edit/'+str(p_id))
