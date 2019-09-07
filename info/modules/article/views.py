from flask import render_template

from . import article_blu


@article_blu.route('/article')
def index():
    return render_template('article/article.html')
