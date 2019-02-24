import os
from flask import Blueprint, request, session, jsonify, send_from_directory
from config import ErrCode
from util import login_required
from models import db, StuInfo, Application

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/loginCheck', methods=["POST"])
def loginCheck():
    name = request.json['name']
    password = request.json['password']
    # 用户可能输入的是小写的x
    password = password.replace('x', 'X')
    # 查询到的当前姓名的记录, 可能有重名
    lists = StuInfo.query.filter_by(name=name)
    for i in lists:
        # 取到身份证号后六位为密码
        if i.idCard[-6:] == password:
            session['id'] = i.idCard
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
    idCard = session.get('id')
    isConfirm = False
    hasImg = False
    appQueryRs = Application.query.filter_by(idCard=idCard).first()
    stuQueryRs = StuInfo.query.filter_by(idCard=idCard).first()
    if appQueryRs:
        isConfirm = True
    if os.path.exists('./photo/{}.jpg'.format(idCard)):
        hasImg = True
    if stuQueryRs:
        info = {
            'name': stuQueryRs.name,
            'idCard': idCard,
            'sNumber': stuQueryRs.sNumber,
            'sex': stuQueryRs.sex,
            'profession': stuQueryRs.profession,
            'nation': stuQueryRs.nation,
            'workUnit': stuQueryRs.workUnit,
            'department': stuQueryRs.department,
            'classId': stuQueryRs.classId,
            'rank': stuQueryRs.rank,
            'hasImg': hasImg,
            'isConfirm': isConfirm,
        }
        return jsonify(errno=ErrCode.SUCCESS, msg='ok', data=info)
    return jsonify(errno=ErrCode.FORMINFO_ERR, msg='not found session id')


@api.route('/uploadImg', methods=["POST"])
@login_required
def uploadImg():
    f = request.files['file']
    basepath = os.path.dirname(__file__)  # 当前文件所在路径
    # 上传的文件名字是身份证号加'.jpg'
    # 新上传的图片使用_new标记, 当确认信息之后进行改名
    upload_path = os.path.join(basepath, 'photo', session['id']+'_new.jpg')
    f.save(upload_path)
    return jsonify(errno=ErrCode.SUCCESS, msg='ok')


@api.route('/getImg', methods=['GET'])
@login_required
def getImg():
    path = os.getcwd() + '/photo'
    idCard = session['id']
    filename = idCard+'.jpg'
    # 如果存在_new标记的图片就返回_new标记图片
    if not os.path.exists(path+'/'+filename):
        filename = idCard + '_new.jpg'
    return send_from_directory(path, filename)


@api.route('/confirm', methods=['POST'])
@login_required
def confirm():
    idCard = session['id']
    appQueryRs = Application.query.filter_by(idCard=idCard).first()
    if appQueryRs:
        return jsonify(errno=ErrCode.CONFIRM_ERR, msg='please not double check')
    newPhotoName = './photo/{}_new.jpg'.format(idCard)
    if os.path.exists(newPhotoName):
        os.rename(newPhotoName, newPhotoName.replace('_new', ''))
    db.session.add(Application(idCard=idCard))
    db.session.commit()
    return jsonify(errno=ErrCode.SUCCESS, msg='ok')
