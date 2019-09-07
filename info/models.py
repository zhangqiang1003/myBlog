

# module
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from info import db


# 基础表
class BaseModel(object):
    """模型基类，为每个模型补充创建时间与更新时间"""
    create_time = db.Column(db.DateTime, default=datetime.now)  # 记录的创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 记录的更新时间


# 用户表
class User(BaseModel, db.Model):
    __tablename__ = "info_user"

    id = db.Column(db.Integer, primary_key=True)  # 用户编号
    nick_name = db.Column(db.String(32), unique=True, nullable=False)  # 用户昵称
    password_hash = db.Column(db.String(128), nullable=False)  # 加密的密码
    last_login = db.Column(db.DateTime, default=datetime.now)  # 最后一次登录时间
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        raise AttributeError("当前属性不可读")

    @password.setter
    def password(self, value):
        self.password_hash = generate_password_hash(value)

    def check_passowrd(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        resp_dict = {
            "id": self.id,
            "nick_name": self.nick_name,
        }
        return resp_dict

    def to_admin_dict(self):
        resp_dict = {
            "id": self.id,
            "nick_name": self.nick_name,
            "register": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "last_login": self.last_login.strftime("%Y-%m-%d %H:%M:%S"),
        }
        return resp_dict


# 文章表
class Article(BaseModel, db.Model):
    __tablename__ = "info_article"

    id = db.Column(db.Integer, primary_key=True)  # 文章编号
    title = db.Column(db.String(256), nullable=False)  # 文章标题
    source_id = db.Column(db.Integer, db.ForeignKey('info_article_source.id'))  # 文章来源
    digest = db.Column(db.String(512), nullable=False)  # 文章摘要
    content = db.Column(db.Text, nullable=False)  # 文章内容
    clicks = db.Column(db.Integer, default=0)  # 浏览量
    index_image_url = db.Column(db.String(256))  # 文章列表图片路径
    category_id = db.Column(db.Integer, db.ForeignKey("info_category.id"))  # 文章分类
    user_name = db.Column(db.String(25), default='张小强')
    status = db.Column(db.Integer, default=1)  # 当前文章状态 如果为0代表审核通过，1代表审核中，-1代表审核不通过
    reason = db.Column(db.String(256))  # 未通过原因，status = -1 的时候使用
    # # 当前文章的所有评论
    # comments = db.relationship("Comment", lazy="dynamic")

    def to_review_dict(self):  # 发布状态查看
        resp_dict = {
            "id": self.id,
            "title": self.title,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "status": self.status,
            "reason": self.reason if self.reason else ""
        }
        return resp_dict

    def to_basic_dict(self):  # 首页文章列表
        resp_dict = {
            "id": self.id,
            "title": self.title,
            "source": self.source,
            "digest": self.digest,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "index_image_url": self.index_image_url,
            "clicks": self.clicks,
        }
        return resp_dict

    def to_dict(self):  #
        resp_dict = {
            "id": self.id,
            "title": self.title,
            "source": self.source,
            "digest": self.digest,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "content": self.content,
            "clicks": self.clicks,
            "category": self.category.to_dict(),
            "index_image_url": self.index_image_url,
            "author": self.user_name,
        }
        return resp_dict


# 分类表
class Category(BaseModel, db.Model):
    __tablename__ = "info_category"

    id = db.Column(db.Integer, primary_key=True)  # 分类编号
    name = db.Column(db.String(64), nullable=False)  # 分类名
    parent_id = db.Column(db.Integer, db.ForeignKey("info_category.id"))  # 父分类id
    parent = db.relationship("Category", remote_side=[id])  # 自关联
    article_list = db.relationship('Article', backref='category', lazy='dynamic')

    def to_dict(self):
        resp_dict = {
            "id": self.id,
            "name": self.name,
            "parent_id": self.parent_id
        }
        return resp_dict


# 文章来源表
class ArticleSource(BaseModel, db.Model):
    __tablename__ = "info_article_source"

    id = db.Column(db.Integer, primary_key=True)  # 文章来源编号
    source = db.Column(db.String(12), default='个人原创')
