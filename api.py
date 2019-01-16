import os
from flask import Blueprint, request, session, jsonify, send_from_directory
from config import ErrCode
from util import login_required

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/loginCheck', methods=["POST"])
def loginCheck():
    name = request.json['name']
    password = request.json['password']
    if password=='22' and name == '11':
        session['id'] = '11'
        return jsonify(errno=ErrCode.SUCCESS, msg='ok')
    return jsonify(errno=ErrCode.LOGIN_ERR, msg='invalid username or password')


@api.route('/reLogin', methods=["GET"])
@login_required
def reLogin():
    session.clear()
    return jsonify(errno=ErrCode.SUCCESS, msg='ok')


@api.route('/formInfo', methods=["GET"])
@login_required
def formInfo():
    info = {
        'name': 'zyx',
        'idCard': '11',
        'hasImg': False,
        'isConfirm': True,
    }
    return jsonify(errno=ErrCode.SUCCESS, msg='ok', data=info)


@api.route('/uploadImg', methods=["POST"])
@login_required
def uploadImg():
    f = request.files['file']
    basepath = os.path.dirname(__file__)  # 当前文件所在路径
    # 上传的文件名字是身份证号加'.jpg'
    upload_path = os.path.join(basepath, 'photo', session['id']+'.jpg')
    f.save(upload_path)
    return jsonify(errno=ErrCode.SUCCESS, msg='ok')


@api.route('/getImg', methods=['GET'])
@login_required
def getImg():
    path = os.getcwd() + '/photo'
    idCard = session['id']
    filename = idCard+'.jpg'
    return send_from_directory(path, filename)
