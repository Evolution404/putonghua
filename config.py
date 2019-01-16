import os
from datetime import timedelta

# 设置为24位的字符,每次运行服务器都是不同的，所以服务器启动一次上次的session就清除。
# SECRET_KEY = os.urandom(24)
SECRET_KEY = 'putonghua'
# 设置session的保存时间。
PERMANENT_SESSION_LIFETIME = timedelta(days=7)

DB_HOST = '115.159.209.36'
DB_USER = 'root'
DB_PASS = '615598813'


class ErrCode:
    SUCCESS = 0
    SESSION_ERR = 1
    LOGIN_ERR = 2
