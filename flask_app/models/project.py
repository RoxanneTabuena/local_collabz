from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.role import Role
from flask_app.models.user import User

class Project:
    DB = "local_collabz_schema"
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.type = data['type']
        self.mission = data['mission']
        self.about = data ['about']
        self.is_recruiting = data['is_recruiting']
        self.is_public = data['is_public']
        self.status = data['status']
        self.score = data['score']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.chat_id = data['chat_id']

        self.creators = None
        self.roles_needed = None
        self.skills_needed = None
        self.liked = False
        self.watched = False
        self.role = None
        self.organizers = None
        self.volunteers = None
        self.roles = None
        self.news = False

    @classmethod
    def create(cls,data):
        query = "INSERT INTO projects (title, mission) VALUES (%(title)s, %(mission)s)"
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def found(cls, data):
        query = "INSERT INTO founded_projects (user_id, project_id) VALUES (%(user_id)s, %(project_id)s)"
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def associate(cls, data):
        query = "INSERT INTO associated_projects (user_id, project_id) VALUES (%(user_id)s, %(project_id)s)"
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def disassociate(cls, data):
        query = "DELETE FROM associated_projects WHERE user_id = %(user_id)s AND project_id = %(project_id)s"
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def retrieve(cls, data):
        query ="SELECT * FROM PROJECTS WHERE title = %(title)s AND mission = %(mission)s"
        return cls(connectToMySQL(cls.DB).query_db(query, data)[0])

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM PROJECTS WHERE is_public = 'yes'"
        results = connectToMySQL(cls.DB).query_db(query)
        projects = []
        for row in results:
            project = cls(row)
            projects.append(project)
        return projects

    @classmethod
    def get_one(cls, id):
        data = {'id': id }
        query = "SELECT * FROM projects WHERE id = %(id)s"
        return  cls(connectToMySQL(cls.DB).query_db(query, data)[0])

    @classmethod
    def get_by_user(cls, id):
        data = {'user_id': id}
        query = "SELECT * FROM founded_projects LEFT JOIN projects ON founded_projects.project_id = projects.id WHERE user_id = %(user_id)s"
        results = connectToMySQL(cls.DB).query_db(query, data)
        projects = []
        for row in results:
            project = cls(row)
            projects.append(project)
        return projects

    @classmethod
    def get_roles(cls,id):
        data = {'id':id}
        query = "SELECT * FROM roles WHERE project_id = %(id)s"
        results =  connectToMySQL(cls.DB).query_db(query, data)
        roles = []
        for row in results:
            role = Role(row)
            roles.append(role)
        return roles

    @classmethod
    def update_score(cls, data):
        query = "UPDATE projects SET score= %(score)s WHERE id = %(id)s"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def associated_projects(cls, id):
        data = {'user_id' : id}
        query = "SELECT * FROM associated_projects LEFT JOIN projects ON project_id = projects.id WHERE user_id = %(user_id)s GROUP BY project_id"
        results = connectToMySQL(cls.DB).query_db(query, data)
        projects = []
        for row in results:
            project = cls(row)
            projects.append(project)
        return projects

    @classmethod
    def get_watched(cls,id):
        data = {'user_id' : id}
        query = "SELECT * FROM project_watchlist LEFT JOIN projects ON project_id = projects.id WHERE user_id = %(user_id)s ORDER BY score DESC"
        results = connectToMySQL(cls.DB).query_db(query, data)
        projects = []
        for row in results:
            project = cls(row)
            projects.append(project)
        return projects

    @classmethod
    def get_organizers(cls,id):
        data = {'project_id' : id}
        query="SELECT * FROM founded_projects WHERE project_id = %(project_id)s"
        results = connectToMySQL(cls.DB).query_db(query, data)
        organizers = []
        for row in results:
            organizer = row['user_id']
            organizers.append(organizer)
        return organizers

    @classmethod
    def has_organized(cls,id):
        data = {'user_id' : id}
        query = "SELECT * FROM founded_projects WHERE user_id = %(user_id)s"
        results = connectToMySQL(cls.DB).query_db(query, data)
        if len(results) < 1:
            return False
        return True

    @classmethod
    def add_organizer(cls,data):
        query = "INSERT INTO founded_projects (user_id, project_id) VALUES (%(user_id)s, %(project_id)s)"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def remove_organizer(cls,data):
        query = "DELETE FROM founded_projects WHERE user_id = %(user_id)s AND project_id = %(project_id)s"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def get_organized_projects(cls, id):
        data = {'id' : id }
        query = "SELECT * FROM users JOIN founded_projects ON users.id = user_id JOIN projects ON project_id = projects.id WHERE users.id = %(id)s"
        results = connectToMySQL(cls.DB).query_db(query, data)
        projects = []
        for row in results:
            projects.append = cls(row)
        return projects

    @classmethod
    def update(cls, data):
        query = "UPDATE projects SET title = %(title)s, mission = %(mission)s WHERE id = %(project_id)s"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def update_status(cls, data):
        query = "UPDATE projects SET status = %(status)s WHERE id = %(id)s"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def update_type(cls, data):
        query = "UPDATE projects SET type = %(type)s WHERE id = %(id)s"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def make_public (cls, id):
        data = {'id' : id}
        query= "UPDATE projects SET is_public = 'yes' WHERE id = %(id)s"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def make_private (cls, id):
        data = {'id' : id}
        query= "UPDATE projects SET is_public = 'no' WHERE id = %(id)s"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def recruit (cls, id):
        data = {'id' : id}
        query= "UPDATE projects SET is_recruiting = 'yes' WHERE id = %(id)s"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def dont_recruit (cls, id):
        data = {'id' : id}
        query= "UPDATE projects SET is_recruiting = 'no' WHERE id = %(id)s"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def about (cls, data):
        query= "UPDATE projects SET about = %(about)s WHERE id = %(id)s"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def count_volunteers(cls, id):
        data = {'project_id' : id}
        query = "SELECT * FROM roles JOIN volunteers ON roles.id = role_id WHERE project_id = %(project_id)s"
        volunteers = 0
        results = connectToMySQL(cls.DB).query_db(query,data)
        for row in results:
            volunteers += 1
        if volunteers == 0:
            return False
        return volunteers

    @classmethod
    def associate_chat(cls, data):
        query = "UPDATE projects SET chat_id = %(chat_id)s WHERE id = %(id)s;"
        return connectToMySQL(cls.DB).query_db(query,data)

