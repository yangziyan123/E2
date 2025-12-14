from flask import render_template, request, redirect, url_for, flash, session
from . import admin_bp
from models import Post, db, User
from utils import admin_required

@admin_bp.route('/')
@admin_bp.route('/index')
@admin_required
def dashboard():
    stats = {
        'post_count': Post.query.count(),
        'draft_count': Post.query.filter_by(status='draft').count(),
        'user_count': User.query.count()
    }

    # 最近 5 篇文章
    recent_posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()

    return render_template(
        'admin/dashboard.html',
        stats=stats,
        recent_posts=recent_posts
    )


@admin_bp.route('/posts')
@admin_required
def admin_post_list():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('admin/post_list.html', posts=posts)

@admin_bp.route("/post/new", methods=["GET", "POST"])
@admin_required
def create_post():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        status = request.form.get("status", "published")
        author_id = session.get("user_id")

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
@admin_required
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
@admin_required
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
