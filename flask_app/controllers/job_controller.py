from flask_app import app
from flask import render_template, redirect, request, session, flash

# Import the User class from models file
from flask_app.models.job import Job



# ======================================
# Create New Job Routes
# ======================================
@app.route("/new_job")
def new_job():
    # Checks to see if someone is logged in
    if "user_id" not in session:
        flash("Please login or register before entering the site!")
        return redirect("/")

    return render_template("new_job.html")

@app.route("/create_job", methods = ["POST"])
def create_job():
    # 1 - Validate form data

    #1a - collect data 
    data = {
        "contractor_name" : request.form["contractor_name"],
        "contractor_number" : request.form["contractor_number"],
        "address" : request.form["address"],
        "start_date" : request.form["start_date"],
        "end_date" : request.form["end_date"],
        "number_of_floors" : request.form["number_of_floors"],
        "price_per_floor" : request.form["price_per_floor"],
        "total_price" : request.form["total_price"],
        "check_if_paid" : request.form["check_if_paid"],
        "partial_payment" : request.form["partial_payment"],
        "remaining_payment" : request.form["remaining_payment"],
        "expenses" : request.form["expenses"],
        "management_name" : request.form["management_name"],
        "management_number" : request.form["management_number"],
        "user_id" : session["user_id"],
    }

    # 1b - Run validations
    if not Job.validate_job(data):
        return redirect("/new_job")

    # 2 - save new job to database
    Job.create_job(data)

    # 3 - redirect back to dashboard
    return redirect("/dashboard")

# ======================================
# Show one job route
# ======================================
@app.route("/job/<int:job_id>")
def show_job(job_id):
    # Checks to see if someone is logged in
    # use this to stop user from using website without logging in
    if "user_id" not in session:
        flash("Please login or register before entering the site!")
        return redirect("/")

    # 1 - query for job info w/ associated info of user
    data = {
        "job_id" : job_id
    }
    # Get Job by using the data above
    job = Job.get_job_by_id(data)

    # 2 - send info to show_job page
    return render_template("show_job.html", job=job)

# ======================================
# Edit Job Route
# ======================================
@app.route("/job/<int:job_id>/edit")
def edit_job(job_id): # passed in job_id because it's in our url.
    # 1 - Query for the job we want to edit
    # our data
    data = {
        "job_id" : job_id
    }

    # to get our job we want to edit
    job = Job.get_job_by_id(data)

    # 2 - pass info to our html page
    return render_template("edit_job.html", job=job)

# Processing the updates (processing routes always have a method)
@app.route("/job/<int:job_id>/update", methods=["POST"])
def update_job(job_id): # passed in job_id because it is in our url.

    # 1 - Validate our form data

    # 1a - Gets our data from the form using request.form
    data = {
        "contractor_name" : request.form["contractor_name"],
        "contractor_number" : request.form["contractor_number"],
        "address" : request.form["address"],
        "start_date" : request.form["start_date"],
        "end_date" : request.form["end_date"],
        "number_of_floors" : request.form["number_of_floors"],
        "price_per_floor" : request.form["price_per_floor"],
        "total_price" : request.form["total_price"],
        "check_if_paid" : request.form["check_if_paid"],
        "partial_payment" : request.form["partial_payment"],
        "remaining_payment" : request.form["remaining_payment"],
        "expenses" : request.form["expenses"],
        "management_name" : request.form["management_name"],
        "management_number" : request.form["management_number"],
        "job_id" : job_id # id passed here to so we can specify in the query(Query is in job.py file), which job to update.
    }

    # 1b - Validates our data. We are going to re-use the same validations from the create_job method
    if not Job.validate_job(data): # if validation fails based on data collected from the form, redirect top the same page and display the errors.
        return redirect(f"/job/{job_id}/edit")

    # 2 - update information
    Job.update_job_info(data) # update job info based on the data passed in.
    # 3 - redirect to dashboard page
    return redirect("/dashboard")

# ======================================
# Delete Job Route
# ======================================\
@app.route("/job/<int:job_id>/delete") # just a processing route, not a post route because we didn't hit submit on a form (meaning no methods=["POST"] necessary)
def delete_job(job_id): # passed in job_id because it's in our url.
    # 1 - Delete the job 

    # 1a - Collect data
    data = {
        "job_id" : job_id
    }

    # 1b - Delete the job
    Job.delete_job(data) # delete job using classmethod called delete_job in job.py file

    # 2 - Redirect back to the dashboard
    return redirect("/dashboard")