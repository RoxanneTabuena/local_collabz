from flask_app import app
from flask import Flask, render_template, redirect, session, request, flash
from flask_app.models.project import Project
from flask_app.models.skill import Skill
from flask_app.models.user import User
from flask_app.models.role import Role
from flask_app.models.notification import Notification
from flask_app.models.conversation import Conversation

@app.route('/add_organizer/<int:id>', methods=['POST'])
def add_organizer(id):
    data = {
        'user_id' : request.form['user_id'],
        'project_id' : id
    }
    Role.organize(data)
    Project.add_organizer(data)
    teammate = User.retrieve_via_id(session['user_id'])
    project = Project.get_one(id)
    data = {
            'reciever_id' : request.form['user_id'],
            'notification' : f"{teammate.alias} has made you an organizer for {project.title}",
            'type' : "organizer",
            'project_id' : id,
            'teammate_alias' : teammate.alias,
            'teammate_id' : teammate.id,
            'role_id' : '0'
        }
    Notification.create(data)
    return redirect('/project/edit/' + str(id))

@app.route('/add_role/<int:id>', methods = ['POST'])
def new_role(id):
    data = {
        'project_id' : id,
        'title' : request.form['title'],
        'description' : request.form['description']
    }
    Role.add(data)
    return redirect('/project/edit/' + str(id))

@app.route('/create_skill/roles/<int:id>', methods=['POST'])
def create_skill_for_role(id):
    skill = request.form['skill'].lower()
    data = {'skill' : skill,
            'id' : request.form['user_id']}
    Skill.create(data)
    return redirect('/project/edit/' + str(id))

@app.route('/add_skillset/<int:id>', methods = ['POST'])
def add_role_skillset(id):
    data = {
        'role_id' : request.form['role_id'],
        'skill_id' : request.form['skill']
    }
    Role.add_skillset(data)
    return redirect('/project/edit/' + str(id))

@app.route('/delete_skillset/<int:id>', methods = ['POST'])
def delete_skillset(id):
    data = {
        'role_id' : request.form['role_id'],
        'skill_id' : request.form['skill_id']
    }
    Role.delete_skillset(data)
    return redirect('/project/edit/' + str(id))

@app.route('/accept_volunteer/<int:id>', methods = ['POST'])
def accept_volunteer(id):
    role = Role.get_role(request.form['role_id'])
    teammate = User.retrieve_via_id(request.form['user_id'])
    project = Project.get_one(id)
    user = User.retrieve_via_id(session['user_id'])
    data = {
        'reciever_id' : teammate.id,
        'notification' : f"You have been accepted as the new {role.title} for {project.title}",
        'type' : "accepted",
        'project_id' : id,
        'teammate_alias' : user.alias,
        'teammate_id' : user.id,
        'role_id' : role.id
    }
    Notification.create(data)
    associated = User.get_team(id)
    for member in associated:
        data = {
            'reciever_id' : member.id,
            'notification' : f"{teammate.alias} is now a {role.title} on {project.title}",
            'type' : "team updates",
            'project_id' : id,
            'teammate_alias' : teammate.alias,
            'teammate_id' : teammate.id,
            'role_id' : role.id
        }
        Notification.create(data)
    data = {
        'user_id' : teammate.id,
        'project_id' : id
    }
    Project.associate(data)
    data = {
        'role_id' : role.id,
        'user_id' : teammate.id
    }
    Role.fill(data)
    Role.volun_clear(data)
    # add to project chat
    chat = Conversation.project_chat(id)
    data = {
        'conversation_id' : chat,
        'user_id' : teammate.id
    }
    Conversation.add_person(data)
    return redirect('/project/edit/' + str(id))

@app.route('/reject_volunteer/<int:id>', methods = ['POST'])
def reject_volunteer(id):
    data = {
        'role_id' : request.form['role_id'],
        'user_id' : request.form['user_id']
    }
    Role.volun_clear(data)
    return redirect('/project/edit/' + str(id))

@app.route('/unassign/verify/<int:p_id>/<int:u_id>/<int:r_id>')
def verify_unassign(p_id, u_id, r_id):
    project = Project.get_one(p_id)
    user = User.retrieve_via_id(u_id)
    organizers = Project.get_organizers(p_id)
    if user.id == session['user_id'] and len(organizers) == 1:
        flash('You may not unassign yourself as you are this projects only organizer.')
        flash('If you wish to abandon this project: please set status to concluded, and archive it')
        return redirect('/project/edit/' + str(p_id))
    if user.id in organizers:
        user.organized_project = True
    role = Role.get_role(r_id)
    data = {
        'project_id' : project.id,
        'user_id' : user.id
    }
    roles = Role.get_roles(data)
    if len(roles) <= 1:
        remove = True
    else:
        remove = False
    return render_template('unassign.html', project = project, user = user, role = role, remove=remove)

@app.route('/unassign/<int:id>', methods = ['POST'])
def unassign(id):
    role = Role.get_role(request.form['role_id'])
    data = {'role_id' : role.id}
    Role.unassign(data)
    return redirect('/project/edit/' + str(id))

@app.route('/unassign/remove/<int:id>', methods = ['POST'])
def unassign_remove(id):
    role = Role.get_role(request.form['role_id'])
    data = {'role_id' : role.id}
    Role.unassign(data)
    teammate = User.retrieve_via_id(request.form['user_id'])
    data = {
        'user_id' : teammate.id,
        'project_id' : id
    }
    Project.disassociate(data)
    Notification.clear(data)
    return redirect('/project/edit/' + str(id))

@app.route('/unassign/organizer/<int:id>', methods = ['POST'])
def unassign_organizer(id):
    role = Role.get_role(request.form['role_id'])
    data = {'role_id' : role.id}
    Role.unassign(data)
    teammate = User.retrieve_via_id(request.form['user_id'])
    data = {
        'user_id' : teammate.id,
        'project_id' : id
    }
    Project.remove_organizer(data)
    Role.delete(role.id)
    return redirect('/project/edit/' + str(id))

@app.route('/unassign/organizer/remove/<int:id>', methods = ['POST'])
def unassign_remove_organizer(id):
    role = Role.get_role(request.form['role_id'])
    data = {'role_id' : role.id}
    Role.unassign(data)
    teammate = User.retrieve_via_id(request.form['user_id'])
    data = {
        'user_id' : teammate.id,
        'project_id' : id
    }
    Project.disassociate(data)
    Notification.clear(data)
    Project.remove_organizer(data)
    Role.delete(role.id)
    return redirect('/project/edit/' + str(id))

@app.route('/verify/withdraw/<int:r_id>/<int:p_id>')
def verify_withdraw(r_id, p_id):
    user = User.retrieve_via_id(session['user_id'])
    role = Role.get_role(r_id)
    project = Project.get_one(p_id)
    organizers = Project.get_organizers(p_id)
    if len(organizers) == 1 and role.title == 'organizer':
        flash('You may not unassign yourself as you are this projects only organizer.')
        flash('If you wish to abandon this project: please set status to concluded, and archive it')
        return redirect('/project/edit/' + str(p_id))
    data = {
        'project_id' : project.id,
        'user_id' : user.id
    }
    roles = Role.get_roles(data)
    if len(roles) <= 1:
        remove = True
    else:
        remove = False
    return render_template('withdraw.html', role = role, user = user, project = project, remove = remove)


@app.route('/edit_role/<int:id>', methods=['POST'])
def edit_role(id):
    data = {
        'current_title' : request.form['current_title'],
        'title' : request.form['title'],
        'description' : request.form['description'],
        'project_id' : id,
    }
    Role.edit(data)
    team = User.get_role(data)
    teammate = User.retrieve_via_id(session['user_id'])
    project = Project.get_one(id)
    for member in team:
        data = {
            'reciever_id' : member.id,
            'notification' : f"{teammate.alias} has made changes to your role in {project.title}",
            'type' : "role updates",
            'project_id' : id,
            'teammate_alias' : teammate.alias,
            'teammate_id' : teammate.id,
            'role_id' : 0
        }
        Notification.create(data)
    return redirect('/project/edit/' + str(id))

