# Import connectToMySQL to run the queries. Queries are not going to run without it.
from flask_app.config.mysqlconnection import connectToMySQL


# Import flash to see the validation errors.
from flask import flash

from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# Import for email validation
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$')

# User Class
class User:
    def __init__(self,data):

        # Columns in here should match your columns exactly in workbench.
        self.id =data["id"]

        self.first_name = data["first_name"]
        self.last_name =data["last_name"]
        self.email =data["email"]
        self.password =data["password"]

        self.created_at =data["created_at"]
        self.updated_at =data["updated_at"]


# Reminder: @staticmethods are always validators.
            # @classmethods are always queries.

    @staticmethod
    def validate_register(data):
        # set is_valid to true
        is_valid = True

        # ====== Validations for First and Last Name ======

        # If statement to see if length of first name is less than 3 characters
        if len(data["first_name"]) < 3: # data["first_name"] has to match the data in user_controller.py
            flash("First Name must be at least 3 characters long!")
            is_valid = False

        # If statement to see if length of last name is less than 3 characters
        if len(data["last_name"]) < 3:
            flash("Last Name must be at least 3 characters long!")
            is_valid = False

        # ====== Validations for email ====== 

        # If statement to see the email entered is valid?
        if not EMAIL_REGEX.match(data["email"]):
            flash("Invalid Email!")
            is_valid = False

        # If user already exists flash the following message
        if User.get_by_email(data):
            flash("Email already in use! Please register with a different email or login!")
            is_valid = False

        # ====== Validations for password and password confirmation

        # If statement to see if length of last name is less than 8 characters
        if len(data["password"]) < 8:
            flash("Password must be at least 8 characters long!")
            is_valid = False

        # If password and confirm password do not match
        if data["password"] != data["pass_conf"]:
            flash("Passwords do not match!")
            is_valid = False

        # return is_valid (can be true or false depending on if statements above)
        return is_valid # end of the validate_register method.

    @staticmethod
    def validate_login(data):
        # is valid true to begin with
        is_valid = True

        # 
        user_in_db = User.get_by_email(data)
        # if statement if user is not registered in database
        if not user_in_db: # if user is not registered in database
            # Flash message
            flash("Invalid Email/Password")
            is_valid = False
        
        # This line checks password with database
        elif not bcrypt.check_password_hash(user_in_db.password, data["password"]): #user_in_db gets password from database and checks it against password from data (user input)
        #if we get False after checking the password
            flash("Invalid Email/Password")
            is_valid = False

        # return is_valid after all the validation 
        return is_valid

    # Checks to see if the user already exists in the database
    @classmethod
    def get_by_email(cls,data):
        query= "SELECT * FROM users WHERE email = %(email)s;"

        # fire_escape is the database name
        result = connectToMySQL("fire_escape").query_db(query,data)
        # Didn't find a matching user
        if len(result)<1:
            return False
        return cls(result[0])

    # gets user by id
    @classmethod
    def get_by_id(cls,data):
        query= "SELECT * FROM users WHERE id = %(user_id)s;"
        # fire_escape is the database name
        result = connectToMySQL("fire_escape").query_db(query,data)
        # Didn't find a matching user
        if len(result)<1:
            return False
        return cls(result[0])

    # query to create a new user
    @classmethod # classmethod because it's a query
    def create_user(cls,data):
        # Query to insert user into database
        query = "INSERT INTO users (first_name, last_name, email, password, created_at) VALUES (%(first_name)s, %(last_name)s, %(email)s,%(password)s,NOW());"

        # Connect to database to run the query
        results = connectToMySQL("fire_escape").query_db(query, data)
        return results