from tornado import ioloop
import os
import sys

from tornado import web
from peewee_async import Manager
from blog.urls import urlpatterns
from blog.settings import settings, db


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
abs_path = os.path.dirname(os.path.abspath("__file__"))

sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))


if __name__ == '__main__':
    import wtforms_json
    wtforms_json.init()
    print("wtform")
    app = web.Application(
        urlpatterns,
        static_path=os.path.join(abs_path, 'static'),
        debug=True,
        **settings
    )
    app.listen(8888)

    objects = Manager(db)

    db.set_allow_sync(False)
    app.objects = objects
    ioloop.IOLoop.current().start()
