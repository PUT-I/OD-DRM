import json
from typing import List

from flask import Flask, request, Response
from sqlalchemy import create_engine
# noinspection PyProtectedMember
from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

import orm_objects as orm
from Log import Log

# noinspection PyTypeChecker
engine: Engine = create_engine("sqlite:///database.sqlite")
Session = sessionmaker()
Session.configure(bind=engine)

app = Flask("PokeVisorAuthorization")


@app.route('/')
@app.route('/test')
def test():
    Log.i("Received test request")
    return "ok"


@app.route('/user/<user_id>/authorized', methods=["POST"])
def authorize(user_id: int):
    session = Session()
    user: orm.User = session.query(orm.User) \
        .filter(orm.User.id_user == user_id) \
        .first()

    if user is None:
        return "", 401

    session.close()

    return '{"authorized": "true"}', 200


@app.route('/user', methods=["GET"])
def get_all_users():
    session = Session()
    try:
        users: List[orm.User] = session.query(orm.User).all()

        response: list = []
        for user in users:
            response.append({
                "userId": user.id_user,
                "username": user.username,
                "password": user.password,
                "authorized": user.authorized
            })
    except:
        session.close()
        return "", 500
    session.close()

    return Response(response=json.dumps(response, default=lambda x: x.__dict__),
                    status=200,
                    mimetype="application/json")


@app.route('/user/<user_id>', methods=["GET"])
def get_user(user_id: int):
    session = Session()
    user: orm.User = session.query(orm.User) \
        .filter(orm.User.id_user == user_id) \
        .first()

    if user is None:
        return "", 404

    response = {
        "userId": user.id_user,
        "username": user.username,
        "password": user.password,
        "authorized": user.authorized
    }
    session.close()

    return Response(json.dumps(response),
                    status=200,
                    mimetype="application/json")


@app.route('/user', methods=["POST"])
def add_user():
    session = Session()
    try:
        request_json = request.json
        user = orm.User(username=request_json["username"],
                        password=request_json["password"],
                        authorized=request_json["authorized"])
        session.add(user)
        session.commit()

        response = {
            "userId": user.id_user,
            "username": user.username,
            "password": user.password,
            "authorized": user.authorized
        }

    except IntegrityError:
        session.close()
        return "", 409
    session.close()

    return Response(json.dumps(response),
                    status=200,
                    mimetype="application/json")


@app.route('/user/<user_id>', methods=["PUT"])
def update_user(user_id: int):
    session = Session()
    user: orm.User = session.query(orm.User) \
        .filter(orm.User.id_user == user_id) \
        .first()

    if user is None:
        return "", 404

    request_json = request.json
    user.password = request_json["password"]
    user.authorized = request_json["authorized"]
    session.commit()

    response = {
        "userId": user.id_user,
        "username": user.username,
        "password": user.password,
        "authorized": user.authorized
    }
    session.close()

    return Response(response,
                    status=200,
                    mimetype="application/json")


@app.route('/user/<user_id>', methods=["DELETE"])
def delete_user(user_id: int):
    session = Session()
    user: orm.User = session.query(orm.User) \
        .filter(orm.User.id_user == user_id) \
        .first()

    if user is None:
        return "", 404

    response = {"userId": user.id_user, "username": user.username, "password": user.password}
    session.delete(user)
    session.commit()
    session.close()

    return response, 200


def _main():
    app.run("0.0.0.0", 5000)


if __name__ == '__main__':
    _main()
