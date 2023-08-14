from flask import session, flash
from datetime import datetime
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user, like

class Show: # change class object name

    db = 'tv_shows' # change DB

    def __init__(self, data): # check against values in ERD
        self.id = data['id']
        self.title = data['title']
        self.network = data['network']
        self.release_date = data['release_date']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = data['user']
        self.likes = data['likes']
    
    @classmethod
    def save_show(cls, data): # add new show
        query = """
            INSERT INTO shows(title, network, release_date, description, created_at, updated_at, user_id)
            VALUES(%(title)s, %(network)s, %(release_date)s, %(description)s, NOW(), NOW(), %(user_id)s);
            """
        result = connectToMySQL(cls.db).query_db(query, data) # returns id no of new like
        return result 
    
    @classmethod
    def get_all(cls): # get all to display in a dashboard incl likes, rename results as nec
        query = """
            SELECT * FROM shows
            ORDER BY title ASC;
            """
        results = connectToMySQL(cls.db).query_db(query)
        all_shows = []
        if results: 
            for i in results: 
                i['release_date'] = i['release_date'].strftime("%B %d %Y")
                i['user'] = user.User.get_user(i['user_id'])
                i['likes'] = like.Like.get_likes_for_show(i['id'])
                all_shows.append(cls(i))
        return all_shows # returns all shows incl user data 

    @classmethod
    def get_one(cls, id): # get one show for detail page and edit page
        query = """
            SELECT * FROM shows 
            WHERE shows.id = %(id)s;
            """
        results = connectToMySQL(cls.db).query_db(query, {'id':id})
        show = results[0]
        show['user'] = user.User.get_user(show['user_id'])
        show['likes'] = like.Like.get_likes_for_show(show['id'])
        show = cls(show)
        return show

    @classmethod
    def update_show(cls,data): # update an existing show
        query = """
            UPDATE shows
            SET title = %(title)s, network = %(network)s, release_date = %(release_date)s, description = %(description)s, updated_at = NOW()
            WHERE id = %(id)s; 
            """
        connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete(cls, id): # delete an existing show
        query = """
            DELETE FROM shows
            WHERE id = %(id)s;
            """
        connectToMySQL(cls.db).query_db(query, {'id':id})
    
    @staticmethod
    def validate_show(data): # validate for both new and update shows
        is_valid = True
        for key, val in data.items(): 
            field = key.replace('_',' ').title()
            if len(val.strip()) < 1: 
                is_valid = False 
                flash(f'{field} must not be blank', 'add')
            elif key in ['title', 'network', 'description'] and len(val.strip()) < 3: 
                is_valid = False
                flash(f'{field} must be at least 3 characters', 'add')
        return is_valid