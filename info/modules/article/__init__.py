from flask import Blueprint

article_blu = Blueprint("article", __name__)

from . import views