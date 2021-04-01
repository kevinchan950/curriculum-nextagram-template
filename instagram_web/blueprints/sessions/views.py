from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import check_password_hash
from models.user import User
from flask_login import login_user, logout_user

sessions_blueprint = Blueprint('sessions',__name__,template_folder='templates')

@sessions_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('sessions/new.html')


@sessions_blueprint.route('/', methods=['POST'])
def create():
    # get data from the form for log in process
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.get_or_none(User.name == username)

    if user:
        result = check_password_hash(user.password_hash, password)
        if result: 
            flash("Successfully Login!")
            login_user(user)
            return redirect(url_for('users.show', username=username))
        else:
            flash(u"Incorrect password!","error")
            return render_template("sessions/new.html", error=True)


@sessions_blueprint.route('/delete', methods=['GET','POST'])
def destroy():
    logout_user()
    flash("logout successful","success")
    return redirect(url_for('home'))