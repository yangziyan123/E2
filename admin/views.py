from flask import render_template, request, redirect, url_for, flash
from . import admin_bp
from models import Post, db
from utils import login_required

@admin_bp.route('/')
@admin_bp.route('/index')
@login_required
def dashboard():
    # TODO 统计数据展示
    stats = {
        'post_count': 150,
        'draft_count': 45,
        'user_count': 320,
    }
    return render_template('admin/dashboard.html',stats=stats)

@admin_bp.route('/posts')
@login_required
def admin_post_list():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('admin/post_list.html', posts=posts)

@admin_bp.route("/post/new", methods=["GET", "POST"])
@login_required
def create_post():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        status = request.form.get("status", "published")
        author_id = 1  # 系统只有一个管理员

        if not title or not content:
            flash("标题和内容不能为空！", "warning")
            return redirect(url_for("admin.create_post"))

        post = Post(title=title, content=content, status=status, author_id=author_id)
        db.session.add(post)
        db.session.commit()

        flash("文章创建成功！", "success")
        return redirect(url_for("admin.admin_post_list"))

    return render_template("admin/post_edit.html", mode="new")


@admin_bp.route("/post/<int:post_id>/edit", methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)

    if request.method == "POST":
        post.title = request.form.get("title")
        post.content = request.form.get("content")
        post.status = request.form.get("status")
        db.session.commit()

        flash("文章更新成功！", "success")
        return redirect(url_for("admin.admin_post_list"))

    return render_template("admin/post_edit.html", mode="edit", post=post)

@admin_bp.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    flash("文章已删除。", "info")
    return redirect(url_for("admin.admin_post_list"))

@admin_bp.route('/profile')
def profile():
    return "后台个人资料页面"

@admin_bp.route('/settings')
def settings():
    return "网站设置页面"