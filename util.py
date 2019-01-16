import functools
from flask import g, session, redirect
from config import ErrCode


def login_required(f):
    """要求用户登录的验证装饰器"""

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        idCard = session.get("id")
        if idCard is None:
            return redirect('/')
        else:
            g.user_id = idCard
            return f(*args, **kwargs)
    return wrapper
