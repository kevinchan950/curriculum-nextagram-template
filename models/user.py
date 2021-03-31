from enum import unique
from models.base_model import BaseModel
import peewee as pw
import re

class User(BaseModel):
    name = pw.CharField(index=True)
    email = pw.CharField(unique=True)
    password = pw.CharField(null=False)

    def validate(self):
        duplicate_email = User.get_or_none(User.email == self.email)

        if len(self.name.strip())==0:
            self.errors.append('Username cannot be blank!')
        
        if len(self.email.strip())==0:
            self.errors.append('Email cannot be blank!')
   
        if len(self.password.strip())==0:
            self.errors.append('Password cannot be blank!')

        elif len(self.password.strip())<6:
            self.errors.append('Password need at least 6 characters!')

        elif (any(letter.isupper() for letter in self.password)) and (any(letter.islower() for letter in self.password)) and (any(re.search("\W{1,}", letter) for letter in self.password)):
            pass

        else:
            self.errors.append('Password must consists of at least one uppercase, one lowercase and one special character')        

        if duplicate_email:
            self.errors.append('Email has been registered!')