from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGREX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Interest:
    DB = "local_collabz_schema"
    def __init__(self, data):
        self.id = data['id']
        self.interest = data['interest']
        self.score = data['score']
        self.creator_id = data['creator_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls, data):
        query = "INSERT INTO interests (interest, score, creator_id) VALUES ( %(interest)s, '1', %(id)s)"
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM interests ORDER BY score DESC"
        results = connectToMySQL(cls.DB).query_db(query)
        interests = []
        for row in results:
            interest = cls(row)
            interests.append(interest)
        return interests

    @classmethod
    def get_one(cls, interest):
        data = {'interest' : interest}
        query = "SELECT * FROM interests WHERE interest = %(interest)s"
        result = connectToMySQL(cls.DB).query_db(query, data)
        if len(result) <1:
            return 'interest not found'
        return cls(result[0])

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM interests WHERE id = %(id)s"
        result = connectToMySQL(cls.DB).query_db(query, data)
        return cls(result[0])

    @classmethod
    def update_score(cls, data):
        query = "UPDATE interests SET score = %(score)s, updated_at = NOW() WHERE id = %(id)s"
        return connectToMySQL(cls.DB).query_db(query, data)