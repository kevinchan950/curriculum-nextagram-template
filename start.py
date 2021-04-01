from flask.globals import session
from flask.templating import render_template
from app import app
import instagram_api
import instagram_web

if __name__ == '__main__':
    app.run()







# SESSION 

# from flask import Flask, session, render_template
# app = Flask(__name__)
# app.serect_key = asdadfaf

# @app.route('/')
# def index():
#     #session["name"] = "Kevin" # this will like saving name = kevin into session and stay there
#     return render_template('index.html')

# @app.route("/login", methods=["POST"])
# def login():
#     username = request.form["username"]
#     password = request.form["password"]
#     user = User.get(User.username == username)
#     if check_password_hash(user.hashed_password, password):
#         session["user_id"] = user.id
#     else: 
#         pass

# @app.route("/profile")
# def profile():
#     if session["user_id"]:
#         user = User.get_by_id(session["user_id"])
#         return render_template("profile.html")
#     else:
#         return render_template("index.html")

# app.run()    


# # HANDLING ERRORS

# @app.errorhandler(500)
# def handle_500(error):
#     return render_template('500.html')