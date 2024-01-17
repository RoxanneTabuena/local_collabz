from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.skill import Skill
from flask_app.models.interest import Interest
import re
EMAIL_REGREX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    DB = "local_collabz_schema"
    def __init__(self, data):
        self.id = data['id']
        self.alias = data['alias']
        self.f_name = data['f_name']
        self.l_name = data['l_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.mission = data['mission']
        self.about = data['about']
        self.updated_at = data['updated_at']
        self.city_id = data['city_id']
        self.score = data['score']

        self.location = None
        self.city = None
        self.area = None
        self.liked = False
        self.watched = False
        self.skillset = None
        self.interests = None
        self.associated_projects = None
        self.organized_project = False
        self.roles = None
        self.on_project = False
        self.watchlist = None

    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (alias, f_name, l_name, email, password) VALUES ( %(alias)s, %(f_name)s, %(l_name)s, %(email)s, %(password)s)"
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users"
        results = connectToMySQL(cls.DB).query_db(query)
        people = []
        for row in results:
            person = User(row)
            people.append(person)
        return people

    @classmethod
    def get_all_skill(cls, data):
        query = "SELECT * FROM user_skillset JOIN users ON user_skillset.user_id = users.id WHERE skill_id = %(skill_id)s ORDER BY score DESC"
        results = connectToMySQL(cls.DB).query_db(query,data)
        if len(results) <1:
            return False
        people = []
        for row in results:
            person = User(row)
            people.append(person)
        return people

    @classmethod
    def get_all_interest(cls, data):
        query = "SELECT * FROM user_interests JOIN users ON user_interests.user_id = users.id WHERE interest_id = %(interest_id)s ORDER BY score DESC"
        results = connectToMySQL(cls.DB).query_db(query,data)
        if len(results) <1:
            return False
        people = []
        for row in results:
            person = User(row)
            people.append(person)
        return people

    @classmethod
    def get_all_new(cls):
        query = "SELECT * FROM users ORDER BY created_at DESC"
        results = connectToMySQL(cls.DB).query_db(query)
        people = []
        for row in results:
            person = User(row)
            people.append(person)
        return people

    @classmethod
    def get_all_hot(cls):
        query = "SELECT * FROM users ORDER BY score DESC"
        results = connectToMySQL(cls.DB).query_db(query)
        people = []
        for row in results:
            person = User(row)
            people.append(person)
        return people

    @classmethod
    def get_city(cls,data):
        query = "SELECT * FROM users WHERE city_id = %(city_id)s ORDER BY score DESC"
        results = connectToMySQL(cls.DB).query_db(query, data)
        people = []
        for row in results:
            person = User(row)
            people.append(person)
        return people

    @classmethod
    def get_area(cls,data):
        query = "SELECT * FROM users LEFT JOIN cities ON users.city_id = cities.id WHERE area = %(area)s ORDER BY score DESC"
        results = connectToMySQL(cls.DB).query_db(query, data)
        people = []
        for row in results:
            person = User(row)
            people.append(person)
        return people

    @classmethod
    def retrieve_via_email(cls, data):
        query  = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.DB).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def retrieve_via_id(cls, id):
        data = {'id' : id}
        query  = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(cls.DB).query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_skills(cls, id):
        data = {'id': id}
        query = """
                SELECT * FROM user_skillset LEFT JOIN skills 
                ON user_skillset.skill_id = skills.id 
                WHERE user_skillset.user_id = %(id)s
                """
        results = connectToMySQL(cls.DB).query_db(query,data)
        skillset = []
        if len(results) < 1:
            return 'No_Skillz'
        for row in results:
            skill = Skill(row)
            skillset.append(skill)
        return skillset

    @classmethod
    def get_interests(cls, id):
        data = {'id': id}
        query = """
                SELECT * FROM user_interests LEFT JOIN interests 
                ON user_interests.interest_id = interests.id 
                WHERE user_interests.user_id = %(id)s
                """
        results = connectToMySQL(cls.DB).query_db(query,data)
        interests = []
        if len(results) < 1:
            return 'Boring'
        for row in results:
            interest = Interest(row)
            interests.append(interest)
        return interests

    @classmethod
    def update(cls, data):
        query = "UPDATE users SET alias = %(alias)s, city_id = %(city_id)s, mission= %(mission)s, about=%(about)s WHERE id = %(id)s"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def add_skill(cls, data):
        query = "INSERT INTO user_skillset (user_id, skill_id) VALUES (%(user_id)s, %(skill_id)s)"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def add_interest(cls, data):
        query = "INSERT INTO user_interests (user_id, interest_id) VALUES (%(user_id)s, %(interest_id)s)"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def like_profile(cls, data):
        query = "INSERT INTO profile_likes (liker_id, likee_id) VALUES (%(liker_id)s, %(likee_id)s)"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def unlike_profile(cls, data):
        query = "DELETE FROM profile_likes WHERE liker_id = %(liker_id)s AND likee_id = %(likee_id)s"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def get_liked_profiles(cls, id):
        data = {'id' : id}
        query = "SELECT likee_id FROM profile_likes WHERE liker_id = %(id)s"
        results = connectToMySQL(cls.DB).query_db(query,data)
        liked_profiles = []
        for row in results:
            liked_profiles.append(row['likee_id'])
        return liked_profiles

    @classmethod
    def watch_profile(cls, data):
        query = "INSERT INTO profile_watchlist (watcher_id, watchee_id) VALUES (%(watcher_id)s, %(watchee_id)s)"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def unwatch_profile(cls, data):
        query = "DELETE FROM profile_watchlist WHERE watcher_id = %(watcher_id)s AND watchee_id = %(watchee_id)s"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def get_watched_profiles(cls, id):
        data = {'id' : id}
        query = "SELECT watchee_id FROM profile_watchlist WHERE watcher_id = %(id)s"
        results = connectToMySQL(cls.DB).query_db(query,data)
        watched_profiles = []
        for row in results:
            watched_profiles.append(row['watchee_id'])
        return watched_profiles
    
    @classmethod
    def get_watched(cls,id):
        data = {'id' : id}
        query = "SELECT * FROM profile_watchlist LEFT JOIN users ON watchee_id = users.id WHERE watcher_id = %(id)s ORDER BY score DESC"
        results = connectToMySQL(cls.DB).query_db(query,data)
        profiles = []
        for row in results:
            person = cls(row)
            profiles.append(person)
        return profiles

    @classmethod
    def add_city(cls, data):
        query = "UPDATE users SET city_id = %(city_id) WHERE id = %(id)s"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def city_request(cls, data):
        query = "INSERT INTO city_requests (city, area, creator_id) VALUES (%(city)s, %(area)s, %(creator_id)s)"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def update_score(cls, data):
        query = "UPDATE users SET score= %(score)s WHERE id = %(id)s"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def like_project(cls, data):
        query = "INSERT INTO project_likes (user_id, project_id) VALUES (%(user_id)s, %(project_id)s)"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def unlike_project(cls, data):
        query = "DELETE FROM project_likes WHERE user_id = %(user_id)s AND project_id = %(project_id)s"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def get_liked_projects(cls, id):
        data = {'id' : id}
        query = "SELECT project_id FROM project_likes WHERE user_id = %(id)s"
        results = connectToMySQL(cls.DB).query_db(query,data)
        liked_projects = []
        for row in results:
            liked_projects.append(row['project_id'])
        return liked_projects

    @classmethod
    def watch_project(cls, data):
        query = "INSERT INTO project_watchlist (user_id, project_id) VALUES (%(user_id)s, %(project_id)s)"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def unwatch_project(cls, data):
        query = "DELETE FROM project_watchlist WHERE user_id = %(user_id)s AND project_id = %(project_id)s"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def get_watched_projects(cls, id):
        data = {'id' : id}
        query = "SELECT project_id FROM project_watchlist WHERE user_id = %(id)s"
        results = connectToMySQL(cls.DB).query_db(query,data)
        watched_projects = []
        for row in results:
            watched_projects.append(row['project_id'])
        return watched_projects

    @classmethod
    def get_team(cls, id):
        data = {'id' : id,
                }
        query = "SELECT users.id, alias, f_name, l_name, email, password, mission, about, users.created_at, users.updated_at, city_id, score FROM roles LEFT JOIN users on user_id = users.id WHERE project_id = %(id)s AND is_filled = 'yes' GROUP BY id ORDER BY created_at ASC"
        results = connectToMySQL(cls.DB).query_db(query,data)
        if len(results) < 1:
            return False
        team = []
        for row in results:
            teammate = cls(row)
            team.append(teammate)
        return team

    @classmethod
    def get_role(cls, data):
        query = "SELECT * FROM roles JOIN users on user_id = users.id WHERE title = %(title)s and project_id = %(project_id)s"
        results = connectToMySQL(cls.DB).query_db(query,data)
        team = []
        for row in results:
            team.append(cls(row))
        return team

    @staticmethod
    def validate(data):
        is_valid = True
        if len(data['f_name']) < 3 or data['f_name'].isalpha() == False:
            flash("Enter a valid first name!")
            is_valid = False
        elif len(data['l_name']) < 3 or data['l_name'].isalpha() == False:
            flash("Enter a valid last name!")
            is_valid = False
        elif len(data['email']) == 0 or not EMAIL_REGREX.match(data['email']):
            flash("Enter a valid email!")
            is_valid = False
        elif User.retrieve_via_email(data) != False:
            flash("We already have a user under that email")
            is_valid = False
        elif len(data['password']) < 8:
            flash('Enter a longer password')
            is_valid = False
        elif data['unhashed_pw'] != data['password_conf']:
            flash("Dem passwords dont match")
            is_valid = False
        return is_valid
