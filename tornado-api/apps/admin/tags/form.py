from wtforms_tornado import Form
from wtforms import StringField
from wtforms.validators import DataRequired


class TagForm(Form):
    name = StringField("标签名称", validators=[DataRequired(message="请输入标签名称")])

