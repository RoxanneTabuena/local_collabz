from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGREX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class City:
    DB = "local_collabz_schema"
    def __init__(self, data):
        self.id = data['id']
        self.city = data['city']
        self.area = data['area']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM cities"
        results = connectToMySQL(cls.DB).query_db(query)
        cities = []
        for row in results:
            city = cls(row)
            cities.append(city)
        return cities

    @classmethod
    def get_city(cls, city_id):
        data = {'city_id' : city_id }
        query = "SELECT * FROM cities WHERE id = %(city_id)s"
        result = connectToMySQL(cls.DB).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_area (cls, data):
        query = "SELECT * FROM cities WHERE id = %(city_id)s"
        area = cls(connectToMySQL(cls.DB).query_db(query, data)[0]).area
        return area

    @classmethod
    def request(cls, data):
        query = "INSERT INTO city_requests (city, area, creator_id) VALUES ( %(city)s, %(area)s, %(id)s)"
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def add(cls, data):
        query = "INSERT INTO cities (city, area) VALUES (%(city)s, %(area)s); "
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def get_by_name(cls, data):
        query = "SELECT * FROM cities WHERE city = %(city)s and area = %(area)s"
        result = connectToMySQL(cls.DB).query_db(query, data)
        return cls(result[0])
