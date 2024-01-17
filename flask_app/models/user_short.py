from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class User_short:
    DB = "local_collabz_schema"
    def __init__(self, data):
        self.id = data['id']
        self.alias = data['alias']

    @classmethod
    def get_members(cls, id):
        data = {'id': id}
        query = "SELECT users.id, alias FROM conversations JOIN members on conversations.id = conversation_id JOIN users on user_id = users.id WHERE conversations.id = %(id)s"
        results = connectToMySQL(cls.DB).query_db(query,data)
        members = []
        for row in results:
            members.append(cls(row))
        return members

    @classmethod
    def get_watchlist(cls,id):
        data = {'id': id}
        query = "SELECT id, alias FROM profile_watchlist JOIN users on watchee_id = users.id WHERE watcher_id = %(id)s"
        results = connectToMySQL(cls.DB).query_db(query,data)
        list = []
        for row in results:
            list.append(cls(row))
        return list
