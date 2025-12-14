from flask import render_template
from . import blog_bp
from models import Post


@blog_bp.route("/")
@blog_bp.route("/index")
def index():
    # 预取最新文章供模板使用（当前模板主要靠 JS 调 API）
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template("blog/index.html", posts=posts)


@blog_bp.route("/posts")
def posts():
    return render_template("blog/posts.html")


@blog_bp.route("/post/<int:post_id>")
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("blog/post_detail.html", post=post)


@blog_bp.route("/about")
def about():
    return "about 页面"
