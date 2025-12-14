from functools import wraps
from flask import session, redirect, url_for, flash, jsonify


def login_required(func):
    """网页端保护：未登录时跳到登录页并提示。"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("请先登录！", "warning")
            return redirect(url_for("auth.login"))
        return func(*args, **kwargs)
    return wrapper


def admin_required(func):
    """后台保护：需要管理员角色。"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("请先登录！", "warning")
            return redirect(url_for("auth.login"))
        if not session.get("is_admin"):
            flash("无权限访问后台。", "danger")
            return redirect(url_for("blog.index"))
        return func(*args, **kwargs)
    return wrapper


def api_login_required(func):
    """API 保护：未登录返回 401 JSON，而不是重定向到登录页。"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"message": "login required"}), 401
        return func(*args, **kwargs)
    return wrapper
