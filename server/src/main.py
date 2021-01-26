import json
from typing import List

from flask import Flask, request, Response
from flask_cors import cross_origin
from sqlalchemy import create_engine
# noinspection PyProtectedMember
from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.orm import sessionmaker

import orm_objects as orm
from Log import Log

# noinspection PyTypeChecker
engine: Engine = None
Session = sessionmaker()

app = Flask("PokeVisorAuthorization")


@app.route('/')
@app.route('/test')
@cross_origin()
def test():
    Log.i("Received test request")
    return "ok"


@app.route('/user/authorize', methods=["POST"])
@cross_origin()
def authorize():
    request_json = request.json
    username = request_json["username"]
    password = request_json["password"]

    session = Session()
    user: orm.User = session.query(orm.User) \
        .filter(orm.User.username == username and orm.User.password == password) \
        .first()

    if user is None:
        return "", 401

    session.close()

    return json.dumps({"authorized": user.authorized}), 200


@app.route('/user', methods=["GET"])
@cross_origin()
def get_all_users():
    session = Session()
    try:
        users: List[orm.User] = session.query(orm.User).all()

        response: list = []
        for user in users:
            response.append({
                "userId": user.id_user,
                "username": user.username,
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
@cross_origin()
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
        "authorized": user.authorized
    }
    session.close()

    return Response(json.dumps(response),
                    status=200,
                    mimetype="application/json")


@app.route('/user', methods=["POST"])
@cross_origin()
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
@cross_origin()
def update_user(user_id: int):
    session = Session()
    user: orm.User = session.query(orm.User) \
        .filter(orm.User.id_user == user_id) \
        .first()

    if user is None:
        return "", 404

    request_json = request.json
    if "password" in request_json and request_json["password"]:
        user.password = request_json["password"]
    if "authorized" in request_json:
        user.authorized = request_json["authorized"]
    session.commit()

    response = {
        "userId": user.id_user,
        "username": user.username,
        "authorized": user.authorized
    }
    session.close()

    return Response(response,
                    status=200,
                    mimetype="application/json")


@app.route('/user/<user_id>', methods=["DELETE"])
@cross_origin()
def delete_user(user_id: int):
    session = Session()
    user: orm.User = session.query(orm.User) \
        .filter(orm.User.id_user == user_id) \
        .first()

    if user is None:
        return "", 404

    response = {
        "userId": user.id_user,
        "username": user.username,
        "authorized": user.authorized
    }
    session.delete(user)
    session.commit()
    session.close()

    return response, 200


def _main():
    import argparse
    import time
    global engine

    parser = argparse.ArgumentParser()

    # Required argument
    parser.add_argument("-a", "--host", type=str, default="localhost", required=False, help="Database host")
    parser.add_argument("-p", "--port", type=int, default=3306, required=False, help="Database port")
    args = parser.parse_args()

    time_start = time.time()
    stop = False
    while not stop:
        try:
            orm.init_db(args.host, args.port)
            stop = True
        except OperationalError as error:
            if time.time() - time_start >= 10.0:
                raise error
    engine = create_engine(f"mysql://root:admin@{args.host}:{args.port}/pokevisor")
    Session.configure(bind=engine)
    app.run("0.0.0.0", 5000)


if __name__ == '__main__':
    _main()
