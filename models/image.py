from datetime import datetime
from enum import unique
from models.base_model import BaseModel
from models.user import User
import peewee as pw

class Image(BaseModel):
    caption = pw.TextField(null=True)
    url = pw.TextField()
    user = pw.ForeignKeyField(User, backref='images', on_delete="CASCADE")


# on_delete = "CASCADE" means when user is deleted, all the images will be deleted as well