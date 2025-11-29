from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:  # 没登录
            flash("请先登录！", "warning")
            return redirect(url_for("auth.login"))
        return func(*args, **kwargs)  # 已登录，放行
    return wrapper