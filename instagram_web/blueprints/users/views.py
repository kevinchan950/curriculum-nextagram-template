from operator import methodcaller
from flask import Blueprint, render_template, redirect, request, session
from flask.helpers import flash, url_for
from flask.wrappers import Request
from peewee import Update
from models.base_model import db
from models.user import User
from models.image import Image
from models.donation import Donation
from models.request import Requested
from models.follow import Follow
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, current_user, logout_user
import boto3
import os
import peewee as pw
import datetime

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


@users_blueprint.route('/<username>')
def show(username):
    user = User.get(name=username)
    if user.description =="None":
        user.description = "No Info"

    image_all = Image.select().where(Image.user_id==user.id)
    
    requested = Requested.select().join(User, on=(User.id==Requested.fan_id)).where(Requested.idol_id == user.id)

    followers = Follow.select().join(User, on=(User.id==Follow.fan_id)).where(Follow.idol_id == user.id)
    
    if not current_user.is_authenticated:
        return render_template("users/profile.html", user=user, image_all=image_all, requested=requested, followers=followers)
    
    if user.name != current_user.name:    
        is_requested = Requested.get_or_none(fan_id=current_user.id, idol_id=user.id)
        is_follower = Follow.get_or_none(fan_id=current_user.id, idol_id=user.id)
        return render_template("users/profile.html", user=user, image_all=image_all, is_requested=is_requested, is_follower=is_follower, followers=followers)
    else:
        return render_template("users/profile.html", user=user, image_all=image_all, requested=requested, followers=followers)


@users_blueprint.route('/<username>/newsfeed')
def newsfeed(username):
    weeks_ago = datetime.date.today() - datetime.timedelta(days=7)
    images = Image.select().where(Image.created_at >= weeks_ago)
    users = User.select().join(Follow, on=(Follow.idol_id == User.id)).where(Follow.fan_id == current_user.id)
    user_with_images = pw.prefetch(users,images)
    return render_template('users/newsfeed.html', user_with_images=user_with_images)


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
    if request.form.get('new_description').strip("") == "":
        pass
    else:
        update = User.update(description=request.form.get('new_description')).where(User.name==current_user.name)
        update.execute()
    if request.form.get('privacy')== None:
        update2 = User.update(is_private=False).where(User.name==current_user.name)
        update2.execute()
    else:
        update2 = User.update(is_private=True).where(User.id==current_user.id)
        update2.execute()
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


@users_blueprint.route('/<username>/<image_id>', methods=["GET"])
def show_image(username,image_id):
    image = Image.get_by_id(image_id)
    donations = Donation.select().join(Image).join(User).where(Image.id == image_id)
    total_donation = 0 
    for donation in donations:
        total_donation += donation.amount
    return render_template('users/image.html', image=image, donations = donations, total_donation=total_donation)

# @users_blueprint.route('/', methods=["GET"])
# def index():
#     return "USERS"


# @users_blueprint.route('/<id>/edit', methods=['GET'])
# def edit(id):
#     pass


# @users_blueprint.route('/<id>', methods=['POST'])
# def update(id):
#     pass

