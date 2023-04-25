from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user_model import User
from flask import flash,request

class Anime:
    db = "original_animes"
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.cover = data['cover']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = data['user_id']
        self.chapter = []

    @classmethod
    def save(cls,data):
        query = """INSERT INTO animes (title,description,cover,user_id) VALUES (%(title)s,%(description)s,%(cover)s,%(user_id)s);"""
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def update_anime(cls,data):
        print(data['id'])
        query = """UPDATE animes SET title =%(title)s, description = %(description)s, cover = %(cover)s WHERE id = %(id)s;"""
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def get_all_animes(cls):
        query ="""SELECT * FROM animes LEFT JOIN users ON animes.user_id = users.id;"""
        results = connectToMySQL(cls.db).query_db(query)
        all_animes =[]
        for one in results:
            user = User({ 
                "id": one['user_id'],
                "first_name": one['first_name'],
                "last_name": one['last_name'],
                "email": one['email'],
                "password": one['password'],
                "created_at": one['created_at'],
                "updated_at": one['updated_at']
            })
            new_anime = Anime({ 
                "id" : one['id'],
                "title" : one['title'],
                "description" : one['description'],
                "cover" : one['cover'],
                "created_at" : one['created_at'],
                "updated_at" : one['updated_at'],
                "user_id" : user
            })
            all_animes.append(new_anime)
        return all_animes
    
    @classmethod
    def get_anime_by_user(cls,data):
        query = """SELECT * FROM animes WHERE user_id = %(id)s;"""
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def delete(cls,id):
        query ="""DELETE from animes WHERE id = %(id)s;"""
        return connectToMySQL(cls.db).query_db(query,{'id':id})
    
    @classmethod
    def get_anime_by_id(cls,data):
        query = """SELECT * FROM animes WHERE id = %(id)s;"""
        return connectToMySQL(cls.db).query_db(query,data)
    
    @staticmethod
    def validate_anime(anime):
        is_valid = True
        if anime['title'] == 0 or anime['description'] == 0:
            flash("Fields must not be blank", "anime")
            is_valid = False
        if len(anime['title']) < 3:
            flash("Title must be 3 characters", "anime")
            is_valid = False
        if len(anime['description']) < 100:
            flash("Anime needs to be 100 characters", "anime")
            is_valid = False
        if 'cover' not in request.files:
            flash("No file", "anime")
            is_valid = False
        return is_valid