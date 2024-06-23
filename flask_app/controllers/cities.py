from flask_app import app
from flask import Flask, render_template, redirect, session, request, flash
from flask_app.models.project import Project
from flask_app.models.skill import Skill
from flask_app.models.user import User
from flask_app.models.city import City
from flask_app.models.notification import Notification
from flask_app.models.conversation import Conversation

@app.route('/city_request/<int:id>', methods=['POST'])
def city_request(id):
    data = {
        'city' : request.form['city'].upper(),
        'area' : request.form['area'].upper(),
        'id' : id,
    }
    City.request(data)
    flash('request recieved, well add that to the list ASAP')
    return redirect('/edit_profile/'+str(id))

@app.route('/new_city/<int:id>', methods=['POST'])
def new_city(id):
    data = {
        'city' : request.form['city'].upper(),
        'area' : request.form['area'].upper(),
        'id' : id,
    }
    City.request(data)
    City.add(data)
    city = City.get_by_name(data)
    print(city.id)
    data['city_id'] = city.id
    User.add_city(data)
    return redirect('/new_user/'+str(id))
