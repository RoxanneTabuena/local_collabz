from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Role:
    DB = "local_collabz_schema"
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.is_filled = data['is_filled']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.project_id = data['project_id']

        self.skillset = None
        self.teammate = None
        self.offered = False
        self.volunteers = None

    @classmethod
    def get_role(cls, id):
        data = {'id': id }
        query = "SELECT * FROM roles WHERE id = %(id)s"
        return cls(connectToMySQL(cls.DB).query_db(query, data)[0])

    @classmethod
    def get_project(cls,id):
        data = {'project_id' : id}
        query = "SELECT * FROM roles WHERE project_id =%(project_id)s"
        results = connectToMySQL(cls.DB).query_db(query, data)
        added_roles= []
        roles = []
        for row in results:
            role = cls(row)
            if role.title not in added_roles and role.is_filled == 'no':
                roles.append(role)
                added_roles.append(role.title)
        return roles

    @classmethod
    def get_team(cls, id):
        data = {'project_id' : id}
        query = "SELECT * FROM roles JOIN users ON roles.user_id = users.id WHERE project_id = %(project_id)s"
        results = connectToMySQL(cls.DB).query_db(query,data)
        team = []
        for row in results:
            role = cls (row)
            teammate = {
                'id' : row['users.id'],
                'alias': row['alias'],
            }
            role.teammate = teammate
            team.append(role)
        return team

    @classmethod
    def volunteer(cls,data):
        query= "INSERT INTO volunteers (role_id, user_id) VALUES (%(role_id)s, %(user_id)s)"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def volunteered(cls, data):
        query="SELECT * FROM volunteers WHERE role_id = %(role_id)s and user_id = %(user_id)s"
        results = connectToMySQL(cls.DB).query_db(query,data)
        if len(results) < 1:
            return False
        return True

    @classmethod
    def get_titles(cls,data):
        query = "SELECT title FROM roles WHERE project_id = %(project_id)s and user_id = %(user_id)s"
        results = connectToMySQL(cls.DB).query_db(query,data)
        titles = []
        for row in results:
            title = row['title']
            titles.append(title)
        return titles

    @classmethod
    def organize(cls,data):
        query="INSERT INTO Roles (title, description, is_filled, user_id, project_id) VALUES ('organizer', 'project organizer', 'yes', %(user_id)s, %(project_id)s)"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def add(cls,data):
        query="INSERT INTO Roles (title, description, is_filled, project_id) VALUES (%(title)s, %(description)s, 'no', %(project_id)s)"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def add_skillset(cls,data):
        query="INSERT INTO role_skillset (role_id, skill_id) VALUES (%(role_id)s, %(skill_id)s)"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def delete_skillset(cls,data):
        query= "DELETE FROM role_skillset WHERE role_id = %(role_id)s AND skill_id = %(skill_id)s"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def get_volunteers(cls, id):
        data = {"role_id" : id}
        query = "SELECT id, alias FROM volunteers LEFT JOIN users ON user_id = users.id WHERE role_id = %(role_id)s"
        results = connectToMySQL(cls.DB).query_db(query,data)
        if len(results) < 1:
            return False
        volunteers = []
        for row in results:
            volunteer = {
                'id' : row['id'],
                'alias' : row['alias']
            }
            volunteers.append(volunteer)
        return volunteers

    @classmethod
    def get_roles(cls, data):
        query = "SELECT * FROM roles WHERE project_id =%(project_id)s and user_id= %(user_id)s"
        results = connectToMySQL(cls.DB).query_db(query,data)
        roles = []
        for row in results:
            role = cls(row)
            roles.append(role)
        return roles

    @classmethod
    def fill(cls, data):
        query="UPDATE roles SET is_filled = 'yes', user_id = %(user_id)s WHERE id = %(role_id)s"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def unassign(cls, data):
        query="UPDATE roles SET is_filled = 'no', user_id = NULL WHERE id = %(role_id)s"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def volun_clear(cls, data):
        query = "DELETE FROM volunteers WHERE role_id = %(role_id)s AND user_id = %(user_id)s"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def delete(cls, id):
        data = {'id': id}
        query = "DELETE FROM roles WHERE id = %(id)s"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def edit(cls, data):
        query = "UPDATE roles SET title = %(title)s, description = %(description)s WHERE title = %(current_title)s and project_id = %(project_id)s"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def on_project(cls, data):
        query = "SELECT * FROM roles WHERE project_id = %(project_id)s AND user_id = %(user_id)s"
        results = connectToMySQL(cls.DB).query_db(query,data)
        if len(results) < 1:
            return False
        return True

    @classmethod
    def unfilled_roles(cls, id):
        data = {'project_id' : id}
        query ="""SELECT roles.id, roles.title, roles.description, roles.is_filled,
            roles.created_at, roles.updated_at, roles.user_id, roles.project_id
            FROM projects JOIN roles on projects.id = project_id
            WHERE is_filled = 'no' AND projects.id = %(project_id)s"""
        results = connectToMySQL(cls.DB).query_db(query,data)
        if len(results) < 1:
            return False
        roles = []
        for row in results:
            roles.append(cls(row))
        return roles

