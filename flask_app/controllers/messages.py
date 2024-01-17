from flask_app import app
from flask import Flask, render_template, redirect, session, request, flash
from flask_app.models.project import Project
from flask_app.models.user import User
from flask_app.models.user_short import User_short
from flask_app.models.message import Message
from flask_app.models.conversation import Conversation
from flask_app.models.role import Role

@app.route('/conversation/<int:id>')
def conversation(id):
    members = User_short.get_members(id)
    allowed = []
    for member in members:
        allowed.append(member.id)
    user = User.retrieve_via_id(session['user_id'])
    if user.id not in allowed:
        session.clear()
        flash('this conversation does not include you, you have been logged out')
        return redirect('/')
    conversation = Conversation.get_one(id)
    messages = Message.get_messages(id)
    watchlist = User_short.get_watchlist(user.id)
    mems = []
    user.watchlist = []
    for member in members:
        mems.append(member.id)
    for person in watchlist:
        if person.id not in mems:
            user.watchlist.append(person)
    data = {'conversation_id' : id,
            'user_id' : user.id }
    Conversation.visit(data)
    return render_template('conversation.html', user=user, members = members, messages = messages, conversation = conversation)

@app.route('/conversation/project/<int:id>')
def project_chat(id):
    project = Project.get_one(id)
    project.team = User.get_team(id)
    for person in project.team:
        data = {
            'user_id' : person.id,
            'project_id' : id
        }
        person.roles = Role.get_roles(data)
    id = Conversation.project_chat(id)
    members = User_short.get_members(id)
    allowed = []
    for member in members:
        allowed.append(member.id)

    user = User.retrieve_via_id(session['user_id'])
    if user.id not in allowed:
        session.clear()
        flash('this conversation does not include you, you have been logged out')
        return redirect('/')
    conversation = Conversation.get_one(id)
    messages = Message.get_messages(id)
    watchlist = User_short.get_watchlist(user.id)
    mems = []
    user.watchlist = []
    for member in members:
        mems.append(member.id)
    for person in watchlist:
        if person.id not in mems:
            user.watchlist.append(person)
    data = {'conversation_id' : id,
            'user_id' : user.id }
    Conversation.visit(data)
    return render_template('project_chat.html', user=user, members = members, messages = messages, conversation = conversation, project = project)

@app.route('/new_message/<int:id>', methods=['POST'])
def new_msg(id):
    data = {
        'message' : request.form['message'],
        'user_id' : session['user_id'],
        'conversation_id' : id
    }
    Message.new(data)
    Conversation.update(id)
    return redirect ('/conversation/' + str(id))

@app.route('/change_title/<int:id>', methods=['POST'])
def change_title(id):
    data = {
        'id' : id,
        'title' : request.form['title']
    }
    Conversation.change_title(data)
    return redirect ('/conversation/' + str(id))

@app.route('/add_2_chat/<int:id>', methods=['POST'])
def add_2_chat(id):
    data = {
        'conversation_id' : id,
        'user_id' : request.form['user_id']
    }
    Conversation.add_person(data)
    return redirect ('/conversation/' + str(id))

@app.route('/conversation/<int:id>/exit')
def confirm_exit(id):
    conversation = Conversation.get_one(id)
    user = User.retrieve_via_id(session['user_id'])
    return render_template('exit.html', conversation = conversation, user = user)

@app.route('/exit_chat/<int:id>', methods=['POST'])
def exit_chat(id):
    data = {
        'user_id' : session['user_id'],
        'conversation_id' : id
    }
    Conversation.exit(data)
    return redirect('/feed')

@app.route('/create_chat', methods=['POST'])
def create_chat():
    data = {'title' : request.form['title']}
    Conversation.new(data)
    conversation = Conversation.get_from_title(data)
    data = {
        'message' : request.form['message'],
        'user_id' : request.form['user_id'],
        'conversation_id' : conversation.id
    }
    Conversation.add_person(data)
    data['user_id'] = session['user_id']
    Message.new(data)
    Conversation.add_person(data)
    return redirect('/conversation/' + str(conversation.id))

@app.route('/new_project_chat/<int:id>', methods=['POST'])
def chat_with_organizers(id):
    data = {'title' : request.form['title']}
    Conversation.new(data)
    conversation = Conversation.get_from_title(data)
    data = {
        'message' : request.form['message'],
        'user_id' : session['user_id'],
        'conversation_id' : conversation.id
    }
    Message.new(data)
    Conversation.add_person(data)
    organizers = Project.get_organizers(id)
    for organizer in organizers:
        data['user_id'] = organizer
        Conversation.add_person(data)
    return redirect('/conversation/' + str(conversation.id))

@app.route('/messages/<int:id>')
def my_messages(id):
    user = User.retrieve_via_id(id)
    watched_people = User.get_watched(id)
    conversations = Conversation.my_messages(id)
    for chat in conversations:
        id = chat.id
        chat.members = User_short.get_members(id)
        data = {'user_id': user.id,
                'conversation_id' : id}
        last_visit = Conversation.last_visit(data)
        if last_visit != False:
            if last_visit < chat.updated_at:
                chat.visited = False
        last_poster = Conversation.last_poster(id)
        if last_poster == user.id:
            chat.visited = True
        print(chat.visited)
    return render_template('my_messages.html', user=user, watched_people=watched_people, conversations = conversations)