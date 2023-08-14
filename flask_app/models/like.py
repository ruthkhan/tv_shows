from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user

class Like: # change class object name

    db = 'tv_shows' # change DB

    def __init__(self, data): # check against values in ERD
        self.id = data['id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.show_id = data['show_id']

    @classmethod
    def save_like(cls, show_id, user_id):
        data = {
            'show_id': show_id,
            'user_id': user_id
        }
        query = """
            INSERT INTO likes(created_at, updated_at, user_id, show_id)
            VALUES(NOW(), NOW(), %(user_id)s, %(show_id)s);
            """
        result = connectToMySQL(cls.db).query_db(query, data) 
        return result # returns id no of new like
    
    @classmethod
    def del_like(cls, show_id, user_id):
        data = {
            'show_id': show_id,
            'user_id': user_id
        }
        query = """
            DELETE FROM likes
            WHERE user_id = %(user_id)s
            AND show_id = %(show_id)s;
            """
        connectToMySQL(cls.db).query_db(query, data) 

    @classmethod
    def get_likes_for_show(cls, id): # get all likes for a single show
        query = """
            SELECT user_id FROM likes
            WHERE show_id = %(id)s; 
            """
        results = connectToMySQL(cls.db).query_db(query, {'id':id}) 
        users_who_like_show = []
        for i in results: 
            users_who_like_show.append(i['user_id'])
        return users_who_like_show # returns list of user_ids that like the show
    
    @staticmethod
    def count_likes(list): 
        like_count = len(list)
        return like_count