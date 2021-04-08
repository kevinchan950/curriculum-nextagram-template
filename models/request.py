from datetime import datetime
from models.base_model import BaseModel
from models.user import User
import peewee as pw 


class Requested(BaseModel):
    idol = pw.ForeignKeyField(User, on_delete="CASCADE")
    fan = pw.ForeignKeyField(User, on_delete="CASCADE")
    