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
        'city' : request.form['city'],
        'area' : request.form['area'],
        'creator_id' : id,
    }
    City.request(data)
    flash('request recieved, well add that to the list ASAP')
    return redirect('/edit_profile/'+str(id))
