from flask_wtf.csrf import CSRFProtect
import os
import config
from flask import Flask
from models.base_model import db

web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'instagram_web')

app = Flask('NEXTAGRAM', root_path=web_dir)

app.secret_key = b"~4AO\xceX\xbd\xd3\xd5C\xa6\xc2\xcb\xe16a\xa4'\xde\xd5\xec\xe1\x05\xc4=\xec;zX;}-"
csrf = CSRFProtect(app)

if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")


@app.before_request
def before_request():
    db.connect()


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        print(db)
        print(db.close())
    return exc
