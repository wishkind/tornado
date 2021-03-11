from datetime import datetime
from bcrypt import hashpw, gensalt
from peewee import *

from apps.utils.utils import get_md5
from blog.models import BaseModel


class PasswordHash(bytes):
    def check_password(self, password):
        password = password.encode('utf-8')
        return hashpw(password, self) == self


class PasswordField(BlobField):
    def __init__(self, iterations=12, *args, **kwargs):
        if None in (hashpw, gensalt):
            raise ValueError('Missing library required for PasswordField: bcrypt')
        self.bcrypt_iterations = iterations
        self.raw_password = None
        super(PasswordField, self).__init__(*args, **kwargs)

    def db_value(self, value):
        """Convert the python value for storage in the database."""
        if isinstance(value, PasswordHash):
            return bytes(value)

        if isinstance(value, str):
            value = value.encode('utf-8')
        salt = gensalt(self.bcrypt_iterations)
        return value if value is None else hashpw(value, salt)

    def python_value(self, value):
        """Convert the database value to a pythonic value."""
        if isinstance(value, str):
            value = value.encode('utf-8')

        return PasswordHash(value)


class UserModel(BaseModel):
    username = CharField(max_length=20, verbose_name='用户名')
    password = PasswordField(verbose_name="密码")
    uuid = CharField(max_length=100, default=get_md5, verbose_name='用户uuid')
    update_time = DateTimeField(default=datetime.now, verbose_name="更新时间")
