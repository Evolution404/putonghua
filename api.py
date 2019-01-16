from flask import Blueprint, request

api = Blueprint('api', __name__)

@api.route('/api/loginCheck', methods=["POST"])
def loginCheck():
    name = request.json['name']
    password = request.json['password']
    if password=='22' and name == '11':
        return '{"errno":0, "msg": "ok"}'
    return '{"errno":1, "msg": "invalid username or password"}'
