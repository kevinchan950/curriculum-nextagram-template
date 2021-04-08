from flask import Blueprint, render_template, request, flash, redirect, url_for
from instagram_web.util.google_oauth import oauth
from werkzeug.security import check_password_hash, generate_password_hash
from models.user import User
from flask_login import login_user, logout_user, current_user
import os

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


@sessions_blueprint.route('/google_login')
def google_login():
    redirect_url = url_for('sessions.authorize', _external = True)
    return oauth.google.authorize_redirect(redirect_url)


@sessions_blueprint.route("/authorize/google")
def authorize():
    oauth.google.authorize_access_token()
    # print(oauth.google.get('https://www.googleapis.com/oauth2/v2/photoslibrary').json())
    name = oauth.google.get('https://www.googleapis.com/oauth2/v2/userinfo').json()['name']
    email = oauth.google.get('https://www.googleapis.com/oauth2/v2/userinfo').json()['email']
    user = User.get_or_none(User.email == email)
    if user:
        login_user(user)
        flash("Successfully Login!")
        return redirect(url_for('users.show', username=current_user.name))
    else:
        password = os.urandom(8)
        password_hashed = generate_password_hash(password)
        create_user = User(name = name , email = email, password_hash = password_hashed)
        create_user.save()
        login_user(create_user)
        flash("Successfully Login!")
        return redirect(url_for('users.show', username=current_user.name))