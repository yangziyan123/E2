from flask import Flask, request, session, flash, redirect, url_for, render_template
from . import auth_bp
from models import User


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session["user_id"] = user.id
            session["username"] = user.username
            session["is_admin"] = bool(user.is_admin)
            flash("登录成功！", "success")
            return redirect(url_for("admin.dashboard"))

        flash("用户名或密码错误！", "danger")

    return render_template("auth/login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()  # 清除会话
    session.pop("_flashes", None)  # 清空所有闪的 flash 消息
    flash("您已成功退出。")
    return redirect(url_for("auth.login"))
