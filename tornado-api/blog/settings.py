import os

import peewee_async

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

settings = {
    "secret_key": "ZGGA#Mp4yL4w5CDu",
    "jwt_expire": (7 * 86400000),
    "MEDIA_ROOT": os.path.join(BASE_DIR, "media"),
    "SITE_URL": "http://api.blog.qinjiahu.cn",
    "BASE_ADMIN_URL": "/api/v1",
    "BASE_WEB_URL": "/api/v2",
    "IMAGE_URL": 'http://api.blog.qinjiahu.cn/api/v1/media/images/',
    "page_size": '10',
    "db": {
        "host": "127.0.0.1",
        "user": "root",
        "password": "dragon",
        "name": "blog",
        "port": 3306
    },
   "db1": {
        "host": "127.0.0.1",
        "user": "postgres",
        "password": "dragon",
        "name": "social_communication_database",
        "port": 5432
    },
    "redis": {
        "host": "127.0.0.1"
    }
}

database = peewee_async.MySQLDatabase(
    database='blog',
    
    host="127.0.0.1",
    port=3306,
    user="root",
    password="dragon",
    database="blog"
)


database1 = peewee_async.PostgresqlDatabase(
    database='social_communication_database',
    host="127.0.0.1",
    
    port=5432,
    user="postgres",
    password="dragon"
)
