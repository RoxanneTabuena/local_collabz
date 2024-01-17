from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Message:
    DB = "local_collabz_schema"
    def __init__(self, data):
        self.id = data['id']
        self.message = data['message']
        self.user_id = data['user_id']
        self.conversation_id = data['conversation_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.alias = None

    @classmethod
    def get_messages(cls, id):
        data = {'id': id}
        query = "SELECT messages.id, messages.message, messages.user_id, messages.conversation_id, messages.created_at, messages.updated_at, alias FROM messages JOIN users on user_id = users.id WHERE conversation_id = %(id)s ORDER BY created_at DESC"
        results = connectToMySQL(cls.DB).query_db(query,data)
        messages = []
        for row in results:
            message = cls(row)
            message.alias = row['alias']
            messages.append(message)
        return messages

    @classmethod
    def new(cls,data):
        query = "INSERT INTO messages (message, user_id, conversation_id) VALUES (%(message)s , %(user_id)s , %(conversation_id)s)"
        return connectToMySQL(cls.DB).query_db(query,data)
