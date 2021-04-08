from flask import Blueprint, render_template, redirect, url_for
from models.user import User
from models.request import Requested
from flask_login import current_user

requests_blueprint = Blueprint('requests', __name__)

@requests_blueprint.route('/<idols_id>', methods=["POST","GET"])
def create_request(idols_id):
    user = User.get_by_id(idols_id)
    idol_id = idols_id
    fan_id = current_user.id
    request = Requested(idol_id = idol_id , fan_id = fan_id)
    request.save()
    return redirect(url_for('users.show', username=user.name))

@requests_blueprint.route("/delete/<fans_id>", methods=["POST","GET"])
def delete_request(fans_id):
    fan_id = fans_id
    idol_id = current_user.id
    request_delete = Requested.delete().where(Requested.idol_id == idol_id, Requested.fan_id == fan_id)
    request_delete.execute()
    return redirect(url_for('users.show', username=current_user.name))
