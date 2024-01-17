from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.role import Role

class Skill:
    DB = "local_collabz_schema"
    def __init__(self, data):
        self.id = data['id']
        self.skill = data['skill']
        self.score = data['score']
        self.creator_id = data['creator_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls, data):
        query = "INSERT INTO skills (skill, score, creator_id) VALUES ( %(skill)s, '1', %(id)s)"
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM skills ORDER BY score desc"
        results = connectToMySQL(cls.DB).query_db(query)
        skills = []
        for row in results:
            skill = cls(row)
            skills.append(skill)
        return skills

    @classmethod
    def get_one(cls, skill):
        data = {'skill' : skill}
        query = "SELECT * FROM skills WHERE skill = %(skill)s"
        result = connectToMySQL(cls.DB).query_db(query, data)
        return cls(result[0])

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM skills WHERE id = %(id)s"
        result = connectToMySQL(cls.DB).query_db(query, data)
        return cls(result[0])

    @classmethod
    def update_score(cls, data):
        query = "UPDATE skills SET score = %(score)s, updated_at = NOW() WHERE id = %(id)s"
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def get_role_skillset(cls, id):
        data = {'role_id': id }
        query = "SELECT * FROM role_skillset LEFT JOIN skills ON role_skillset.skill_id = skills.id WHERE role_id = %(role_id)s"
        results = connectToMySQL(cls.DB).query_db(query, data)
        skillset = []
        for row in results:
            skill = cls(row)
            skillset.append(skill)
        return skillset

    @classmethod
    def user_skillset(cls, id):
        data = {'user_id': id}
        query = "SELECT * FROM user_skillset WHERE user_id = %(user_id)s"
        results = connectToMySQL(cls.DB).query_db(query, data)
        if len(results) < 1:
            return False
        skillset = []
        for row in results:
            skillset.append(row['skill_id'])
        return skillset
    
    @classmethod
    def match_projects(cls, data):
        query = "SELECT projects.id FROM role_skillset JOIN roles on role_id = roles.id JOIN projects ON project_id = projects.id WHERE is_filled = 'no' AND skill_id = %(skill_id)s"
        results = connectToMySQL(cls.DB).query_db(query, data)
        if len(results) < 1:
            return False
        projects = []
        for row in results:
            projects.append(row['id'])
        return projects
