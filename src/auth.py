from flask import Blueprint, json, request, jsonify
from flask_jwt_extended.utils import get_jwt_identity
from http_constants.status import HttpStatus
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required

from src.database import User
from src.database import db
import validators
from flasgger import swag_from

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth.route("/register",methods=["POST"])
@swag_from('./docs/auth/register.yaml')
def register():
    username = request.json["username"]
    email = request.json["email"]
    password = request.json["password"]

    if len(username) < 3:
        return jsonify({'error': "username is too short"}), HttpStatus.BAD_REQUEST

    if not username.isalnum() or " " in username:
        return jsonify({'error': "username should be alphanumeric also no spaces"}), HttpStatus.BAD_REQUEST

    if len(password) < 6:
        return jsonify({'error': "password is too short"}), HttpStatus.BAD_REQUEST

    if not validators.email(email):
        return jsonify({'error': "email is not valid"}), HttpStatus.BAD_REQUEST

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({'error': "email already exists!"}), HttpStatus.CONFLICT

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({'error': "username already exists!"}), HttpStatus.CONFLICT

    hashed_pwd = generate_password_hash(password)
    user = User(username=username, email=email, password=hashed_pwd)
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': "user created!",
        'user': {
            'username': username,
            'email': email
        }
    }), HttpStatus.CREATED


@auth.route("/login",methods=["POST"])
@swag_from('./docs/auth/login.yaml')
def login():
    email = request.json.get("email", "")
    password = request.json.get("password", "")

    user = User.query.filter_by(email=email).first()
    if user:
        is_pass_correct = check_password_hash(user.password, password)
        if is_pass_correct:
            access = create_access_token(identity=user.id)
            refresh = create_refresh_token(identity=user.id)
            return jsonify({
                'user': {
                    'access': access,
                    'refresh': refresh,
                    'username': user.username,
                    'email': user.email
                }
            }), HttpStatus.OK
        else:
            return jsonify({'error': "Incorrect email or password!"}), HttpStatus.UNAUTHORIZED
    else:
        return jsonify({'error': "Incorrect email or password!"}), HttpStatus.UNAUTHORIZED


@auth.route("/refresh/token",methods=["POST"])
@jwt_required(refresh=True)
def refresh_user_tokens():
    identity = get_jwt_identity()
    access = create_access_token(identity=identity)
    return jsonify({
        "access": access
    }), HttpStatus.OK
