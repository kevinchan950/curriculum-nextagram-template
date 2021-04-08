from flask import Blueprint, request
from flask.helpers import url_for
from flask.templating import render_template
from werkzeug.utils import redirect
from models.follow import Follow
from models.request import Requested
from models.user import User
from flask_login import current_user

follows_blueprint = Blueprint('follows', __name__)

@follows_blueprint.route("/<fans_id>", methods=["POST","GET"])
def create_follow(fans_id):
    fan_id = fans_id
    idol_id = current_user.id
    follow = Follow(idol_id=idol_id, fan_id=fan_id)
    follow.save()
    request_delete = Requested.delete().where(Requested.idol_id == idol_id, Requested.fan_id == fan_id)
    request_delete.execute()
    return redirect(url_for('users.show', username=current_user.name))


@follows_blueprint.route("/delete/<idols_id>", methods=["POST","GET"])
def delete_follow(idols_id):
    user = User.get_by_id(idols_id)
    fan_id = current_user.id
    idol_id = idols_id
    follow_delete = Follow.delete().where(Follow.idol_id == idol_id, Follow.fan_id == fan_id)
    follow_delete.execute()
    return redirect(url_for('users.show', username=user.name))