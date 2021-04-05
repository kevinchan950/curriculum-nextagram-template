from flask import Blueprint, render_template, redirect, request, session
from flask.helpers import flash, url_for
from flask.wrappers import Request
from peewee import Update
from models.base_model import db
from models.user import User
from models.image import Image
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, current_user, logout_user
import boto3
import os
import peewee as pw

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
)


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
    user = User.get(name=username)
    if user.description =="None":
        user.description = "No Info"

    image_all = Image.select().where(Image.user_id==user.id)

    return render_template("users/profile.html", user=user, image_all=image_all)


@users_blueprint.route('/<username>/upload/profile', methods=["GET"])
def upload_profile(username):
    return render_template('users/upload_profile.html')


@users_blueprint.route('/<username>/upload/profile', methods=["POST"])
def create_profile(username):
    file = request.files.get('upload_profile')
    bucket_name = os.getenv('S3_BUCKET')
    s3.upload_fileobj(
        file,
        bucket_name,
        file.filename,
        ExtraArgs={
            "ACL":"public-read",
            "ContentType":file.content_type
        }
    )

    update = User.update(profile_picture=f'https://kevinchan950-nextagram-flask.s3-ap-southeast-1.amazonaws.com/{file.filename}').where(User.name==current_user.name)
    update.execute()
    return redirect(url_for('users.show',username=current_user.name))


@users_blueprint.route('/<username>/new/description', methods=["GET"])
def new_description(username):
    return render_template('users/new_description.html')


@users_blueprint.route('/<username>/update/description', methods=["POST"])
def update_description(username):
    update = User.update(description=request.form.get('new_description')).where(User.name==current_user.name)
    update.execute()
    return redirect(url_for('users.show', username=current_user.name))


@users_blueprint.route('/<username>/upload/image', methods=["GET"])
def upload_image(username):
    return render_template('users/upload_image.html')


@users_blueprint.route('/<username>/upload/image', methods=["POST"])
def create_image(username):
    if "upload_image" not in request.flies:
        flash("No Image selected", "warning")
        return redirect(url_for('users.upload_image', username=current_user.name))
    else:
        file = request.files.get('upload_image')
        bucket_name = os.getenv('S3_BUCKET')
        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL":"public-read",
                "ContentType":file.content_type
            }
        )

        image = Image(caption=request.form.get('caption'), url=f'https://kevinchan950-nextagram-flask.s3-ap-southeast-1.amazonaws.com/{file.filename}', user = current_user.id)
        if image.save():
            flash("Image upload successfully", "success")
            return redirect(url_for('users.show', username=current_user.name))
        else: 
            flash("Upload failed, please try again")
            return render_template('users/upload_image.html')    


# @users_blueprint.route('/', methods=["GET"])
# def index():
#     return "USERS"


# @users_blueprint.route('/<id>/edit', methods=['GET'])
# def edit(id):
#     pass


# @users_blueprint.route('/<id>', methods=['POST'])
# def update(id):
#     pass

