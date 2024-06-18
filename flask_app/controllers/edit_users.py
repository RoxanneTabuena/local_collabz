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

@app.route('/')
def index():
    session['logged_in'] = False
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    if request.form['alias'] == '':
        alias = request.form['f_name']
    else: alias = request.form['alias']
    data = {
        'alias': alias,
        'f_name': request.form['f_name'],
        'l_name': request.form['l_name'],
        'email': request.form['email'],
        'password': pw_hash,
        'password_conf' : request.form['password_conf'],
        'unhashed_pw' : request.form['password']
    }
    if not User.validate(data):
        session['reg_attempt'] = True
        return redirect('/')
    User.create(data)
    user = User.retrieve_via_email(data)
    session['logged_in'] = True
    session['user_id'] = user.id
    return redirect('/new_user/' + str(user.id))

@app.route('/new_user/<int:id>')
def new_user(id):
    user = User.retrieve_via_id(id)
    skills = Skill.get_all()
    interests = Interest.get_all()
    return render_template('new_user.html', user=user, skills = skills, interests = interests)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    data = {'email' : request.form['email']}
    user = User.retrieve_via_email(data)
    if user == False or not bcrypt.check_password_hash(user.password, request.form['password']):
        session['login_attempt'] = True
        flash('Invalid password/email combo')
        return redirect('/')
    session['logged_in'] = True
    session['user_id'] = user.id
    user.score += 1
    data = {
        'id' : user.id,
        'score' : user.score
    }
    User.update_score(data)
    return redirect('/feed/' + str(user.id))

@app.route('/edit_profile/<int:id>')
def edit_profile(id):
    user = User.retrieve_via_id(id)
    user.skillset = User.get_skills(id)
    user.interests = User.get_interests(id)
    user.location = City.get_city(user.city_id)
    user.associated_projects = Project.associated_projects(id)
    for project in user.associated_projects:
        id = project.id
        project.team = Role.get_team(id)
        project.needed_roles = Role.get_project(id)
        for role in project.needed_roles:
            role.skillset = Skill.get_role_skillset(role.id)
    skills = Skill.get_all()
    has_skills = []
    if user.skillset != 'No_Skillz':
        for skill in user.skillset:
            has_skills.append(skill.id)
    interests = Interest.get_all()
    has_interests = []
    if user.interests != 'Boring':
        for interest in user.interests:
            has_interests.append(interest.id)
    cities = City.get_all()
    return render_template('edit_profile.html', user=user, skills=skills, interests=interests, cities=cities, has_interests=has_interests, has_skills=has_skills)

@app.route('/update/<int:id>', methods=['POST'])
def update_profile(id):
    data={
        'id' : id,
        'alias' : request.form['alias'],
        'city_id' : request.form['city_id'],
        'mission' : request.form['mission'],
        'about' : request.form['about'],
    }
    if request.form['mission'] == 'Enter a short description of how youd like to distinguish yourself. Could be a motto, personal mantra, or just your job title.':
        data['mission'] = 'False'
    if request.form['city_id'] == '':
        data['city_id'] = 'False'
    User.update(data)
    return redirect('/edit_profile/'+str(id))

@app.route('/update/skills/<int:id>', methods=['POST'])
def update_skills(id):
    data = {
        'user_id' : id,
        'skill_id' : request.form['skill_id']
    }
    User.add_skill(data)
    data = {
        'id' : request.form['skill_id']
    }
    skill = Skill.get_by_id(data)
    score = skill.score + 1
    data['score'] = score
    Skill.update_score(data)
    flash('skill added:)')
    user = User.retrieve_via_id(session['user_id'])
    user.score += 2
    data = {
        'id' : user.id,
        'score' : user.score
    }
    User.update_score(data)
    return redirect('/edit_profile/' + str(id))

@app.route('/update/interests/<int:id>', methods=['POST'])
def update_interests(id):
    data = {
        'user_id' : id,
        'interest_id' : request.form['interest_id']
    }
    User.add_interest(data)
    data = {
        'id' : request.form['interest_id']
    }
    interest = Interest.get_by_id(data)
    score = interest.score + 1
    data['score'] = score
    Interest.update_score(data)
    flash('interest added:)')
    user = User.retrieve_via_id(session['user_id'])
    user.score += 2
    data = {
        'id' : user.id,
        'score' : user.score
    }
    User.update_score(data)
    return redirect('/edit_profile/' + str(id))

@app.route('/create_skill/<int:id>', methods=['POST'])
def create_skill(id):
    skill = request.form['skill'].lower()
    data = {'skill' : skill,
            'id' :id}
    Skill.create(data)
    skill = Skill.get_one(skill)
    data['skill_id'] = skill.id
    data['user_id'] = id
    User.add_skill(data)
    flash('skill added:)')
    user = User.retrieve_via_id(session['user_id'])
    user.score += 2
    data = {
        'id' : user.id,
        'score' : user.score
    }
    User.update_score(data)
    return redirect ('/edit_profile/'+str(id))

@app.route('/new/create_skill/<int:id>', methods=['POST'])
def create_skill_new(id):
    skill = request.form['skill'].lower()
    data = {'skill' : skill,
            'id' :id}
    Skill.create(data)
    skill = Skill.get_one(skill)
    data['skill_id'] = skill.id
    data['user_id'] = id
    User.add_skill(data)
    flash('skill added:)')
    user = User.retrieve_via_id(session['user_id'])
    user.score += 2
    data = {
        'id' : user.id,
        'score' : user.score
    }
    User.update_score(data)
    return redirect ('/new_user/'+str(id))

@app.route('/create_interest/<int:id>', methods=['POST'])
def create_interest(id):
    interest = request.form['interest'].lower()
    data = {'interest' : interest,
            'id' :id}
    Interest.create(data)
    interest = Interest.get_one(interest)
    data['interest_id'] = interest.id
    data['user_id'] = id
    User.add_interest(data)
    flash('interest added:)')
    user = User.retrieve_via_id(session['user_id'])
    user.score += 2
    data = {
        'id' : user.id,
        'score' : user.score
    }
    User.update_score(data)
    return redirect ('/edit_profile/'+str(id))

@app.route('/new/create_interest/<int:id>', methods=['POST'])
def create_interest_new(id):
    interest = request.form['interest'].lower()
    data = {'interest' : interest,
            'id' :id}
    Interest.create(data)
    interest = Interest.get_one(interest)
    data['interest_id'] = interest.id
    data['user_id'] = id
    User.add_interest(data)
    flash('interest added:)')
    user = User.retrieve_via_id(session['user_id'])
    user.score += 2
    data = {
        'id' : user.id,
        'score' : user.score
    }
    User.update_score(data)
    return redirect ('/new_user/'+str(id))

@app.route('/new_city/<int:id>', methods=['POST'])
def request_city(id):
    data = {
        'city' : request.form['city'],
        'area' : request.form['area'],
        'creator_id' : id
    }
    User.city_request(data)
    flash('City Requested<3')
    return redirect ('/edit_profile/'+str(id))

@app.route('/volunteer/<int:id>', methods=['POST'])
def volunteer(id):
    user = User.retrieve_via_id(session['user_id'])
    project = Project.get_one(id)
    role = Role.get_role(request.form['role_id'])
    data = {
        'user_id' : user.id,
        'role_id' : role.id,
    }
    Role.volunteer(data)
    organizers = Project.get_organizers(id)
    for organizer in organizers:
        data = {
            'reciever_id' : organizer,
            'notification' : f" has volunteered for {role.title} on {project.title}",
            'type' : "volunteer",
            'project_id' : id,
            'teammate_alias' : user.alias,
            'teammate_id' : user.id,
            'role_id' : role.id
        }
        Notification.create(data)
    return redirect ('/project/' + str(id))

