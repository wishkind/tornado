from wtforms_tornado import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired


class ArticleForm(Form):
    title = StringField("文章标题", validators={DataRequired(message="请输入文章标题")})
    content = TextAreaField("文章内容", validators={DataRequired(message="请输入文章内容")})
    keyword = StringField("关键词", validators={DataRequired(message="请输入关键词")})
