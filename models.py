from config import DB_URI
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


def currentTime():
    return datetime.now().strftime('%Y-%m-%d')


class StuInfo(db.Model):
    # 定义表名
    __tablename__ = 'stu_info'
    # 定义列对象
    idCard = db.Column(db.CHAR(18), primary_key=True)
    name = db.Column(db.VARCHAR(10))
    sNumber = db.Column(db.BIGINT)
    sex = db.Column(db.CHAR(1))
    profession = db.Column(db.VARCHAR(50))
    nation = db.Column(db.VARCHAR(50))
    workUnit = db.Column(db.VARCHAR(50))
    department = db.Column(db.VARCHAR(50))
    classId = db.Column(db.VARCHAR(50))
    rank = db.Column(db.VARCHAR(50))
    applications = db.relationship('Application', backref='applications')


class Application(db.Model):
    __tablename__ = 'application'
    id = db.Column(db.INT, primary_key=True)
    idCard = db.Column(db.CHAR(18), db.ForeignKey('stu_info.idCard'))
    applyDate = db.Column(db.Date, default=datetime.now)
