from flask import render_template
from . import blog_bp

@blog_bp.route('/')
@blog_bp.route('/index')
def index():
    posts = [
        {"id": 1, "title": "第一篇博客", "summary": "这是一段摘要……"},
        {"id": 2, "title": "第二篇博客", "summary": "这是第二篇摘要……"},
    ]
    return render_template('blog/index.html', posts=posts)

@blog_bp.route('/posts')
def posts():
    # TODO: 获取并显示博客列表
    return "前台博客列表页面"

@blog_bp.route('/post/<int:post_id>')
def post_detail(post_id):
    # TODO: 根据 post_id 获取具体的博客文章内容
    return f"博客详情页面，文章ID：{post_id}"

@blog_bp.route('/about')
def about():
    return "about 页面"