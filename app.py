from flask import Flask
from blog import blog_bp
from auth import auth_bp
from admin import admin_bp
from models import db, User

def create_app():
    app = Flask(__name__)

    app.secret_key = "yzy123"

    # 配置 SQLite
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///myblog.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # 注册蓝图
    app.register_blueprint(blog_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth') 
    app.register_blueprint(admin_bp, url_prefix='/admin')

        # 创建数据库 & 超级用户
    with app.app_context():
        db.create_all()

        # 如果数据库里没有用户，则创建一个超级用户
        if User.query.count() == 0:
            admin = User(username="admin")
            admin.set_password("123456")  # ← 你可以改成自己的密码
            db.session.add(admin)
            db.session.commit()
            print("超级用户 admin 已创建，密码：123456")

    return app

if __name__ == '__main__':
    app = create_app()

    # 第一次运行自动创建数据库
    with app.app_context():
        db.create_all()

    app.run(debug=True)