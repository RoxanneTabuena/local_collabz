from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Conversation:
    DB = "local_collabz_schema"
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.members = None
        self.visited = True
        self.last_post = None

    @classmethod
    def get_one(cls, id):
        data = {'id': id}
        query = "SELECT * FROM conversations WHERE id = %(id)s"
        return cls(connectToMySQL(cls.DB).query_db(query,data)[0])

    @classmethod
    def change_title(cls, data):
        query = "UPDATE conversations set title=%(title)s, updated_at = NOW() WHERE id = %(id)s"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def add_person(cls, data):
        query = "INSERT INTO members (conversation_id, user_id) VALUES (%(conversation_id)s, %(user_id)s)"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def exit(cls, data):
        query = "DELETE FROM members WHERE user_id = %(user_id)s and %(conversation_id)s"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def new(cls, data):
        query = "INSERT INTO conversations (title, created_at) VALUES (%(title)s, NOW());"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def get_from_title(cls, data):
        query="SELECT * FROM conversations where title = %(title)s and created_at = NOW();"
        return cls(connectToMySQL(cls.DB).query_db(query,data)[0])

    @classmethod
    def my_messages(cls, id):
        data = { 'id' : id }
        query = "SELECT * FROM members JOIN conversations ON conversation_id = conversations.id WHERE user_id = %(id)s ORDER BY updated_at DESC"
        chats = []
        results = connectToMySQL(cls.DB).query_db(query,data)
        for row in results:
            chats.append(cls(row))
        return chats

    @classmethod
    def update(cls, id):
        data = { 'id' : id }
        query = "UPDATE conversations SET updated_at = NOW() WHERE id = %(id)s"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def visit(cls, data):
        query = "INSERT INTO chat_visits (user_id, conversation_id, last_visit) VALUES (%(user_id)s, %(conversation_id)s, NOW())"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def last_visit(cls, data):
        query = "SELECT last_visit FROM chat_visits WHERE user_id = %(user_id)s and conversation_id = %(conversation_id)s ORDER BY last_visit DESC"
        last_visit = connectToMySQL(cls.DB).query_db(query,data)
        if len(last_visit) < 1:
            return False
        return last_visit[0]['last_visit']

    @classmethod
    def last_poster(cls, id):
        data = {'id' : id}
        query = "SELECT user_id FROM messages WHERE conversation_id = %(id)s ORDER BY created_at DESC"
        return connectToMySQL(cls.DB).query_db(query,data)[0]['user_id']

    @classmethod
    def project_chat(cls, id):
        data = {'id': id}
        query = "SELECT chat_id FROM projects WHERE id = %(id)s"
        return connectToMySQL(cls.DB).query_db(query,data)[0]['chat_id']

