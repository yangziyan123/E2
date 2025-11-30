# api/views.py
from flask import request, jsonify, session
from . import api_bp
from models import db, Post, User
from utils import login_required

# -------------------
# 登录 API
# -------------------
@api_bp.route("/login", methods=["POST"])
def api_login():
    data = request.json

    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        # 使用 session 保存登录状态
        session["user_id"] = user.id
        return jsonify({"message": "login success"}), 200

    return jsonify({"message": "invalid credentials"}), 401


@api_bp.route("/logout", methods=["POST"])
def api_logout():
    session.clear()
    return jsonify({"message": "logout success"}), 200


# -------------------
# 文章资源 RESTful
# -------------------
@api_bp.route("/posts", methods=["GET"])
def list_posts():
    posts = Post.query.all()
    return jsonify([
        {
            "id": p.id,
            "title": p.title,
            "status": p.status,
            "content": p.content[:30] if p.content else ""
        }
        for p in posts
    ])


@api_bp.route("/posts", methods=["POST"])
@login_required
def create_post():
    data = request.json
    post = Post(
        title=data.get("title"),
        content=data.get("content"),
        status=data.get("status", "published"),
        author_id=session["user_id"]   # 登录后才有 user_id
    )
    db.session.add(post)
    db.session.commit()
    return jsonify({"message": "created", "id": post.id}), 201

@api_bp.route("/posts/<int:post_id>", methods=["GET"])
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify({
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "status": post.status
    })

@api_bp.route("/posts/<int:post_id>", methods=["PUT"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    data = request.json

    post.title = data.get("title", post.title)
    post.content = data.get("content", post.content)
    post.status = data.get("status", post.status)
    db.session.commit()

    return jsonify({"message": "updated"}), 200

@api_bp.route("/posts/<int:post_id>", methods=["DELETE"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": "deleted"}), 200