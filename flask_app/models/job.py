# Import connectToMySQL to run the queries. Queries are not going to run without it.
from flask_app.config.mysqlconnection import connectToMySQL

# Import flash to see the validation errors.
from flask import flash

# Import user.py so we can use it in for loop
from flask_app.models import user

class Job:
    def __init__(self, data):
        self.id = data["id"]

        self.contractor_name = data["contractor_name"]
        self.contractor_number = data["contractor_number"]
        self.address = data["address"]
        self.start_date = data["start_date"]
        self.end_date = data["end_date"]
        self.number_of_floors = data["number_of_floors"]
        self.price_per_floor = data["price_per_floor"]
        self.total_price = data["total_price"]
        self.check_if_paid = data["check_if_paid"]
        self.partial_payment = data["partial_payment"]
        self.remaining_payment = data["remaining_payment"]
        self.expenses = data["expenses"]
        self.management_name = data["management_name"]
        self.management_number = data["management_number"]
        self.user_id = data["user_id"]

        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        
        # places holder (here we are indicating that our job will have a single user)
        self.user = {}

# Reminder: @staticmethods are always validators.
            # @classmethods are always queries.
    @staticmethod
    def validate_job(data):
        is_valid = True

        # Validation for Contractor's Name field
        if len(data["contractor_name"]) < 2:
            flash("Contractor's Name must be at least 2 characters long!")
            is_valid = False

        # Validation for Job's Address field
        if len(data["address"]) < 2:
            flash("Address must be at least 2 characters long!")
            is_valid = False
        
        # Validation for Number of floors field. If no number of floors are entered.
        if data["number_of_floors"] == "":
            flash("Please enter a number of floors!")
            is_valid = False

        # Validation for Number of floors field (int used to type cast it into integer)
        elif int(data["number_of_floors"]) < 2:
            flash("Floors must be at least 2!")
            is_valid = False

        return is_valid

    @classmethod
    def create_job(cls, data):
        # our query
        query = "INSERT INTO jobs (contractor_name, contractor_number, address, start_date, end_date, number_of_floors, price_per_floor, total_price, check_if_paid, partial_payment, remaining_payment, expenses, management_name, management_number, user_id, created_at) VALUES(%(contractor_name)s, %(contractor_number)s, %(address)s, %(start_date)s, %(end_date)s, %(number_of_floors)s, %(price_per_floor)s, %(total_price)s, %(check_if_paid)s, %(partial_payment)s, %(remaining_payment)s, %(expenses)s, %(management_name)s, %(management_number)s, %(user_id)s, NOW());"
        # run Query 
        results = connectToMySQL("fire_escape").query_db(query, data)

        return results

    @classmethod
    def get_all(cls):

        # Our Query
        query = "SELECT * FROM jobs LEFT JOIN users ON jobs.user_id = users.id;"

        # Run our Query (Don't include data because we don't have any)
        results = connectToMySQL("fire_escape").query_db(query)

        all_jobs = []

        # ========== For Loop Start ==========
        for row in results: # for loops gets new job, new user and adds it to the list
            # cls creates an instant of the class we are in currently
            job = cls(row)

            # users data
            user_data = {
                "id" : row["users.id"],

                "first_name" : row ["first_name"],
                "last_name" : row["last_name"],
                "email" : row["email"],
                "password" : row["password"],

                "created_at" : row["users.created_at"],
                "updated_at" : row["users.updated_at"]
            }

            # we are overlapping the job.user field with the above user_data.
            job.user = user.User(user_data) # Here we are replacing the placeholder above in the "def __init__(self, data):"
            all_jobs.append( job )
        return all_jobs
        # ========== For Loop End ==========

    @classmethod
    def get_job_by_id(cls, data):
        # Our query
        query = "SELECT * FROM jobs LEFT JOIN users ON jobs.user_id = users.id WHERE jobs.id = %(job_id)s;"

        # Run our Query 
        results = connectToMySQL("fire_escape").query_db(query, data)

        job = cls(results[0])

        # users data
        user_data = {
            "id" : results[0]["users.id"],

            "first_name" : results[0] ["first_name"],
            "last_name" : results[0]["last_name"],
            "email" : results[0]["email"],
            "password" : results[0]["password"],

            "created_at" : results[0]["users.created_at"],
            "updated_at" : results[0]["users.updated_at"]
        }

        job.user = user.User(user_data)

        return job

    @classmethod
    def update_job_info(cls, data):

        # query for our updates
        query = "UPDATE jobs SET contractor_name = %(contractor_name)s, contractor_number = %(contractor_number)s, address = %(address)s, start_date = %(start_date)s, end_date = %(end_date)s, number_of_floors = %(number_of_floors)s, price_per_floor = %(price_per_floor)s, total_price = %(total_price)s, check_if_paid = %(check_if_paid)s, partial_payment = %(partial_payment)s, remaining_payment = %(remaining_payment)s, expenses = %(expenses)s, management_name = %(management_name)s, management_number = %(management_number)s, updated_at = NOW() WHERE id = %(job_id)s;"

        # Run our Query based on the data
        results = connectToMySQL("fire_escape").query_db(query, data)

        return # update queries don't return anything, so here don't return anything (to indicate end of the method).

    @classmethod
    def delete_job(cls, data):
        
        # Our query to delete a job
        query = "DELETE FROM jobs WHERE id = %(job_id)s;"

        # Run our Query 
        results = connectToMySQL("fire_escape").query_db(query, data)

        return # delete queries don't return anything, so here don't return anything (to indicate end of the method).
