from flask import Blueprint, render_template, redirect, request
from flask.helpers import flash, url_for
from flask.wrappers import Request
from models.user import User
from werkzeug.security import generate_password_hash


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
    user = User(name=username, email=email, password=hashed_password)

    if user.save():
        flash("Successfully sign up")
        return redirect(url_for('users.new'))
    else:
        return render_template('users/new.html', errors=user.errors)

@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
