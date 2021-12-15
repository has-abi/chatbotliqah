from enum import unique
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Conversation(db.Model):
    """
    This is a class that represents a form of a conversation in a database

    Attributes:

    id (int): the id of a conversation
    message (text): the message sended by the sender
    response (text): the response generate by the api
    created_at (datetime): the created at date time
    updated_at (datetime): the updated at date time
    
    """
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    message = db.Column(db.Text(), nullable=False)
    response = db.Column(db.Text())
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def __repr__(self) -> str:
        return 'User>>> {id = self.id}'



class Sender(db.Model):
    """
    This is a class that represents a sender in a database

    Attributes:

    id (int): the id of the sender
    nomAr (string): name of the sender
    CNIE (string): CNIE token/code
    dateExperationCNE (string): the end date of the CINE
    dateNaissance (string): date of birth
    essbAdresse (string): adress of the sender
    province: province of the sender
    commune: local of the sender
    created_at (datetime): the created at date time
    updated_at (datetime): the updated at date time
    
    """
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    nomAr = db.Column(db.String(30),nullable=False)
    CNIE = db.Column(db.String(8),nullable=False,unique=True)
    dateExperationCNE = db.Column(db.String(15),nullable=False)
    dateNaissance = db.Column(db.String(15),nullable=False)
    essbAdresse = db.Column(db.String(80))
    province = db.Column(db.String(60))
    commune = db.Column(db.String(60))
    answered = db.Column(db.Boolean)

    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def __repr__(self) -> str:
        return 'Sender>>> {CNIE = self.CNIE}'


class User(db.Model):
    """
    This is a class that represents a form of a user in a database

    Attributes:

    id (int): the id of a conversation
    username (string): username
    email (string): email
    password (text): password
    created_at (datetime): the created at date time
    updated_at (datetime): the updated at date time
    
    """
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def __repr__(self) -> str:
        return 'User>>> {self.username}'