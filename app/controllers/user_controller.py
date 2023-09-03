from flask import render_template, request, redirect, url_for
from models.user_model import User
from app import app

@app.route("/", methods=["GET"])
def homepage():
    users = User.get_all()
    return render_template("homepage.html", users=users)

@app.route("/create_user", methods=["POST"])
def create_user():
    name = request.form.get("name")
    surname = request.form.get("surname")
    user = User(name, "example@gmail.com", surname)
    user.create_user()
    return redirect(url_for("homepage"))