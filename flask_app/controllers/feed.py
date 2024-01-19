from flask_app import app
from flask import Flask, render_template, redirect, session, request, flash
from flask_app.models.project import Project
from flask_app.models.skill import Skill
from flask_app.models.user import User
from flask_app.models.user_short import User_short
from flask_app.models.role import Role
from flask_app.models.notification import Notification
from flask_app.models.conversation import Conversation

@app.route('/feed')
def oldfeed():
    id = session['user_id']
    return redirect ('/feed/' + str(id))

@app.route('/feed/<int:id>')
def feed(id):
    user = User.retrieve_via_id(id)
    attention = False
    messages = Notification.new_roles(id)
    if messages:
        attention = True
    project_updates= Notification.check_4_updates(id)
    # collect and display notifications
    if project_updates != False:
        attention = True
        mentioned = []
        update_list = []
        for project in project_updates:
            if project.project_id not in mentioned:
                mentioned.append(project.project_id)
                project_name = Project.get_one(project.project_id).title
                update_list.append(project_name)
        project_updates = update_list
    active_chats = []
    chats = Conversation.my_messages(id)
    for chat in chats:
        id = chat.id
        data = {'user_id': user.id,
                'conversation_id' : id}
        last_visit = Conversation.last_visit(data)
        if last_visit != False:
            if last_visit < chat.updated_at:
                chat.visited = False
        last_poster = Conversation.last_poster(id)
        if last_poster == user.id:
            chat.visited = True
        if chat.visited == False:
            active_chats.append(chat.title)
    # display project matching skills
    # get user skillset
    user_skills = Skill.user_skillset(user.id)
    if user_skills:
        # find projects in need of skill and rate them on relevance to user
        attention = True
        project_match = {}
        for skill in user_skills:
            data = { "skill_id": skill}
            new_matches = Skill.match_projects(data)
            if new_matches:
                for match in new_matches:
                    if match in project_match:
                        project_match[match] += 1
                    else:
                        project_match[match] = 1
        # sort by found relevance
        if project_match != {}:
            project_match = dict(reversed(sorted(project_match.items(), key=lambda x:x[1])))
            projects = []
            for item in project_match:
                projects.append(item)
            featured_project = Project.get_one(projects[0])
            featured_project.team = User.get_team(featured_project.id)
            featured_project.roles_needed = Role.unfilled_roles(featured_project.id)
            skills= []
            for role in featured_project.roles_needed:
                role.skillset = Skill.get_role_skillset(role.id)
                for skill in role.skillset:
                    if skill.id in user_skills:
                        skill.has = True
                    skills.append(skill)
            featured_project.skills_needed = skills
        else: featured_project = False
        return render_template('feed.html', user=user, messages = messages, project_updates=project_updates, active_chats=active_chats, project=featured_project, attention = attention, project_match=project_match)

@app.route('/dismiss/<int:id>', methods = ['POST'])
def dismiss(id):
    Notification.dismiss(id)
    id = session['user_id']
    return redirect ('/feed/' + str(id))