from enum import unique
from logging import NullHandler

from models.base_model import BaseModel
import peewee as pw
import re
from flask_login import UserMixin

class User(UserMixin,BaseModel):
    name = pw.CharField(index=True, unique=True)
    email = pw.CharField(unique=True)
    password_hash = pw.CharField(null=False)
    password = None
    profile_picture = pw.CharField(default='https://i.stack.imgur.com/l60Hf.png')
    description = pw.CharField(default="None")
    is_private = pw.BooleanField(default=False, null=True)

    def validate(self):
        duplicate_email = User.get_or_none(User.email == self.email)
        duplicate_name = User.get_or_none(User.name == self.name)

        if duplicate_name: 
            self.errors.append('Username exists!')

        if duplicate_email:
            self.errors.append('Email has been registered!')

        if len(self.name.strip())==0:
            self.errors.append('Username cannot be blank!')
        
        if len(self.email.strip())==0:
            self.errors.append('Email cannot be blank!')
   
        if self.password == None:
            pass
        else:    
            if len(self.password.strip())==0:
                self.errors.append('Password cannot be blank!')

            elif len(self.password.strip())<6:
                self.errors.append('Password need at least 6 characters!')

            elif any(letter.isupper() for letter in self.password) and any(letter.islower() for letter in self.password) and any(re.search("\W{1,}", letter) for letter in self.password):
                pass

            else:
                self.errors.append('Password must consists of at least one uppercase, one lowercase and one special character')        

