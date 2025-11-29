from flask import Flask, request, session, flash, redirect, url_for, render_template
from . import auth_bp

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == 'admin' and password == '123456':
            session['user_id'] = 1      # ★ 修复点
            session['username'] = username
            flash('登录成功！', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('用户名或密码错误！', 'danger')

    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    flash('您已成功登出。', 'success')
    return redirect(url_for('auth.login'))