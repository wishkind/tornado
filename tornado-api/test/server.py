from peewee import *
from datetime import datetime
import tornado.web
import tornado.ioloop
import tornado.options





class BaseModel(Model):
    add_time = DateTimeField(default=datetime.now, verbose_name="添加时间", help_text='添加时间')
    update_time = DateTimeField(default=datetime.now, verbose_name='更新时间', help_text='更新时间')

    def save(self, *args, **kwargs):
        if self._get_pk_value() is None:
            self.add_time = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S")
        self.update_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S")

        return super(BaseModel, self).save(*args, **kwargs)


class CategoryHandler(tornado.web.RequestHandler):
    async def get(self, *args, **kwargs):
        

        return {}


    def post(self, *args, **kwargs):



if __name__ == '__main__':
    app = web.Application(
        urlpatterns,
        debug=True,
        **settings
    )
    app.listen(8888)
    objects = Manager(db)

    db.set_allow_sync(False)
    app.objects = objects
    ioloop.IOLoop.current().start()
