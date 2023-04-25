from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user_model import User
from flask_app.models.anime_model import Anime
from flask import flash

class Chapter:
    db ="original_animes"
    def __init__(self,data):
        self.id = data['id']
        self.chapter_title = data['chapter_title']
        self.story = data['story']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.anime = data['anime_id']

    @classmethod
    def save(cls,data):
        query ="""INSERT INTO chapters (chapter_title,story,anime_id) VALUES (%(chapter_title)s, %(story)s, %(anime_id)s);"""
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def all_chapters_by_id(cls,data):
        query = """SELECT * FROM chapters WHERE anime_id = %(id)s;"""
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def select_all_chapters(cls,data):
        query = """ SLECT * FROM chapters LEFT JOIN animes ON chapters.anime_id = animes.id
        LEFT JOIN users ON animes.user_id = users.id;"""
        return connectToMySQL(cls.db).query_db(query,data)
    
    @staticmethod
    def validate_chapter(chapter):
        is_valid = True
        if chapter['chapter_title'] == 0 or chapter['story'] == 0:
            flash("Fields must not be blank", "chapter")
            is_valid = False
        if len(chapter['chapter_title']) < 3:
            flash("Title must be 3 characters", "chapter")
            is_valid = False
        if len(chapter['story']) < 100:
            flash("Chapter needs to be 100 characters", "chapter")
            is_valid = False
        return is_valid