from flask import session, flash
from flask_bcrypt import Bcrypt
import re 
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL

bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User: 

    db = 'tv_shows' # change DB path

    def __init__(self, data): # initialise object - match against ERD fields
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save_user(cls, data): # insert user into DB; hash password first
        data_dict = dict(data)
        data_dict['password'] = bcrypt.generate_password_hash(data['password'])
        query = """
            INSERT INTO users (first_name, last_name, email, password, created_at, updated_at)
            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());
            """
        result = connectToMySQL(cls.db).query_db(query, data_dict)
        return result # returns user id

    @classmethod
    def get_user(cls, id): # get user by id
        query = """
            SELECT * FROM users
            WHERE id = %(id)s;
            """
        results = connectToMySQL(cls.db).query_db(query, {'id':id})
        return cls(results[0])
    
    @classmethod
    def get_userid(cls, data): # get user by email usually for login
        query = """
            SELECT id FROM users
            WHERE email = %(email)s;
            """
        result = connectToMySQL(cls.db).query_db(query, data)
        return result[0]['id'] #returns userid
    
    @staticmethod
    def valid_reg(data): # validate registration
        is_valid = True
        if len(data['first_name'].strip()) < 2: 
            is_valid = False
            flash('First name must be at least 2 characters', 'register')
        if len(data['last_name'].strip()) < 2: 
            is_valid = False
            flash('Last name must be at least 2 characters', 'register')
        if not EMAIL_REGEX.match(data['email']): 
            is_valid = False
            flash('Email missing / Invalid email format', 'register')
        if len(data['password'].strip()) < 1: 
            is_valid = False
            flash('Password is required', 'register')
        if data['password'] != data['confirm_pw']: 
            is_valid = False
            flash('Password and Confirm PW do not match', 'register')
        return is_valid
    
    @staticmethod
    def valid_login(data): 
        is_valid = True 
        # check if user exists in DB
        query = """
            SELECT password FROM users
            WHERE email = %(email)s; 
            """
        result = connectToMySQL(User.db).query_db(query, data)
        if not result: 
            is_valid = False
            flash('Invalid email/password', 'login')
        elif not bcrypt.check_password_hash(result[0]['password'], data['password']): # check password if user exists
            is_valid = False
            flash('Invalid email/password', 'login')
        return is_valid