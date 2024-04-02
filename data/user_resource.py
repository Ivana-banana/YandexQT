from flask_restful import reqparse, abort, Api, Resource
from flask import jsonify
from werkzeug.security import generate_password_hash

from . import db_session
from .users import User
from .user_parser import parser


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    news = session.query(User).get(user_id)
    if not news:
        abort(404, message=f"User {user_id} not found")


def set_password(password):
    return generate_password_hash(password)


class UserResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        sess = db_session.create_session()
        user = sess.query(User).get(user_id)
        return jsonify({
                'user': user.to_dict(only=("name", "surname", "age"))
            })

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        sess = db_session.create_session()
        user = sess.query(User).get(user_id)
        sess.delete(user)
        sess.commit()
        sess.close()
        return jsonify({
            'delete success': f"user_id {user_id}"})


class UserResourceList(Resource):
    def get(self):
        sess = db_session.create_session()
        user = sess.query(User).all()
        return jsonify({
            'users': [item.to_dict(only=("name", "surname", "position")) for item in user]})

    def post(self):
        args = parser.parse_args()
        sess = db_session.create_session()
        user = User(
            name=args["name"],
            surname=args["surname"],
            age=args["age"],
            position=args["position"],
            speciality=args["speciality"],
            address=args["address"],
            email=args["email"],
            hashed_password=set_password(args["hashed_password"])
        )
        sess.add(user)
        sess.commit()
        sess.close()
        return jsonify({'success': 'OK'})
