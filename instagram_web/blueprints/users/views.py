from flask import Blueprint, render_template, redirect, request, session
from flask.helpers import flash, url_for
from flask.wrappers import Request
from models.user import User
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')

@users_blueprint.route('/', methods=['POST'])
def create():
    username = request.form.get('user_name')
    email = request.form.get('user_email')
    password = request.form.get('user_password')
    hashed_password = generate_password_hash(password)
    user = User(name=username, email=email, password_hash=hashed_password, password=password)

    if user.save():
        flash("Successfully sign up")
        login_user(user)
        return redirect(url_for('users.show', username=username))
    else:
        return render_template('users/new.html', errors=user.errors)


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    return render_template("users/profile.html")


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
