from flask_app import app
from flask import render_template, redirect, request, session, flash

# Import the User class from models file
from flask_app.models.user import User

# Import the Job class from models file
from flask_app.models.job import Job


# Import
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template('index.html')


# ======================================
# Register Route
# ======================================
@app.route("/register", methods=["POST"])
def register():
    # Step 1: Validating form information
    data = {
        # Request.form requests data from the form (["first_name"] has to be the same as in the HTML form.)
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": request.form["password"],
        "pass_conf": request.form["pass_conf"],
    }

    # If validation fails redirects user to ("/")
    if not User.validate_register(data):
        return redirect("/")
    
    # Step 2: bcrypt Password
    data["password"] = bcrypt.generate_password_hash(request.form["password"])

    # Step 3: save new user to database
    new_user_id = User.create_user(data) # create a new user using data

    # Step 4: enter user id into session and redirect to dashboard
    session["user_id"] = new_user_id
    return redirect("/dashboard")


# ======================================
# Login Route
# ======================================
@app.route("/login", methods=["POST"])
def login():
    #1 - Validate login info

    #1a - get data from form (user input)
    data = {
        "email": request.form["email"],
        "password": request.form["password"]
    }

    #1b - validation of data object (user input)
    # if user not found redirect to login and registration  page
    if not User.validate_login(data):
        return redirect("/")

    #2 - query for user info based on email
    user = User.get_by_email(data)
    #3 - put user id into session and redirect to dashboard
    session["user_id"] = user.id
    return redirect("/dashboard")

# ======================================
# Render Dashboard Route
# ======================================
@app.route("/dashboard")
def dashboard():
    # Checks to see if someone is logged in
    if "user_id" not in session:
        flash("Please login or register before entering the site!")
        return redirect("/")

    # grabs data entered into session
    data = {
        "user_id" : session["user_id"]
    }

    #after collecting data from session. create a new query
    user = User.get_by_id(data)

    # gets all the jobs from the database
    all_jobs = Job.get_all() 

    # Everything we want to render on the page has to be passed in here
    return render_template("dashboard.html", user=user, all_jobs = all_jobs)

# ======================================
# Logout Route
# ======================================
@app.route("/logout")
def logout():
    session.clear()
    flash("Succesfully logged out!")
    return redirect("/")
