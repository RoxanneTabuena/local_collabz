from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Notification:
    DB = "local_collabz_schema"
    def __init__(self, data):
        self.id = data['id']
        self.reciever_id = data['reciever_id']
        self.notification = data['notification']
        self.type = data['type']
        self.dismissed = data['dismissed']
        self.project_id = data['project_id']
        self.teammate_id = data['teammate_id']
        self.teammate_alias = data['teammate_alias']
        self.role_id = data['role_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls, data):
        query = "INSERT INTO notifications (reciever_id, notification, type, project_id, teammate_alias, teammate_id, role_id) VALUES (%(reciever_id)s, %(notification)s, %(type)s, %(project_id)s, %(teammate_alias)s, %(teammate_id)s, %(role_id)s)"
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def new_roles(cls, id):
        data = {'id': id}
        query = "SELECT * FROM notifications WHERE reciever_id = %(id)s AND type = 'accepted' AND dismissed = 'no'"
        results = connectToMySQL(cls.DB).query_db(query, data)
        if len(results)<0:
            return False
        messages = []
        for row in results:
            messages.append( cls(row))
        return messages

    @classmethod
    def dismiss(cls, id):
        data = {'id': id}
        query = "UPDATE notifications SET dismissed = 'yes' WHERE id = %(id)s"
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def check_4_updates(cls, id):
        data = {'id': id}
        query = "SELECT * FROM notifications WHERE reciever_id = %(id)s AND type = 'team updates' AND dismissed = 'no'"
        results = connectToMySQL(cls.DB).query_db(query, data)
        if len(results)<0:
            return False
        updates = []
        for row in results:
            updates.append( cls(row))
        return updates

    @classmethod
    def project_news(cls, data):
        query = "SELECT * FROM notifications WHERE reciever_id = %(user_id)s AND dismissed = 'no' AND project_id = %(project_id)s AND type NOT LIKE 'volunteer'"
        results = connectToMySQL(cls.DB).query_db(query, data)
        if len(results)> 0:
            return True
        return False

    @classmethod
    def project_notifications(cls, data):
        query = "SELECT * FROM notifications WHERE reciever_id = %(user_id)s AND dismissed = 'no' AND project_id = %(project_id)s AND type NOT LIKE 'volunteer'"
        results = connectToMySQL(cls.DB).query_db(query, data)
        notifications = []
        for row in results:
            notifications.append(cls(row))
        return notifications
    
    @classmethod
    def clear(cls, data):
        query= "UPDATE notifications SET dismissed = 'yes' WHERE reciever_id = %(user_id)s and project_id = %(project_id)s"
        return connectToMySQL(cls.DB).query_db(query, data)




