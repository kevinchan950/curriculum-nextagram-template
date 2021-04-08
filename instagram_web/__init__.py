import datetime
from app import app
from flask import render_template
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.sessions.views import sessions_blueprint
from instagram_web.blueprints.payments.views import payments_blueprint
from instagram_web.blueprints.requests.views import requests_blueprint
from instagram_web.blueprints.follows.views import follows_blueprint
from instagram_web.util.google_oauth import oauth
from flask_assets import Environment, Bundle
from .util.assets import bundles
from models.user import User
from models.image import Image
import peewee as pw

assets = Environment(app)
assets.register(bundles)
oauth.init_app(app)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")
app.register_blueprint(payments_blueprint, url_prefix= "/payments")
app.register_blueprint(requests_blueprint, url_prefix="/requests")
app.register_blueprint(follows_blueprint, url_prefix="/follows")

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route("/")
def home():
    # user = User.select().where(User.created_at > '2021-04-02').group_by(User.id).order_by(User.name)
    user_all = User.select().group_by(User.id).order_by(User.name)
    images = Image.select()
    user_with_images = pw.prefetch(user_all,images)
    return render_template('home.html', user_with_images=user_with_images)