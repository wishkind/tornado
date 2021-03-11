import json
from datetime import datetime
import time
import jwt
from playhouse.shortcuts import model_to_dict

from apps.utils.decorators import authenticated_async
from apps.utils.utils import json_serial
from blog.handler import RedisHandler
from blog.settings import settings
from apps.models.user_models import UserModel
from apps.utils.utils import url_encode


class LoginHandle(RedisHandler):
    # @authenticated_async
    async def post(self, *args, **kwargs):
        """登陆"""
        re_data = {}

        param = json.loads(self.request.body.decode('utf-8'))
        username = param['username']
        password = param['password']

        try:
            user = await self.application.objects.get(UserModel, username=username)
            if not user.password.check_password(password):
                self.set_status(400)
                re_data['code'] = 0
                re_data['message'] = '用户名或密码错误'

            else:
                payload = {
                    "id": user.id,
                    "username": user.username,
                    "exp": datetime.utcnow()
                }

                token = jwt.encode(payload, self.settings["secret_key"], algorithm='HS256')

                re_data['code'] = 1
                # re_data["id"] = url_encode(str(user.username))
                re_data["token"] = token.decode("utf8")
                re_data["lifeTime"] = str(int(time.time() * 1000) + int(settings['jwt_expire']))
                re_data['message'] = '登录成功'

        except UserModel.DoesNotExist as e:
            self.set_status(400)
            re_data['code'] = 0
            re_data['message'] = '用户不存在'

        self.finish(re_data)


class UserHandler(RedisHandler):
    @authenticated_async
    async def put(self, *args, **kwargs):
        """添加用户"""
        re_data = {}
        params = json.loads(self.request.body.decode('utf-8'))

        try:
            await self.application.objects.get(UserModel, username=params['username'])
            self.set_status(400)
            re_data['code'] = 0
            re_data['message'] = '用户已存在'
        except UserModel.DoesNotExist as e:
            await self.application.objects.create(UserModel, username=params['username'], password=params['password'])
            re_data['code'] = 1
            re_data['message'] = '添加成功'

        self.finish(re_data)

    @authenticated_async
    async def post(self, *args, **kwargs):
        """修改用户"""
        re_data = {}
        params = json.loads(self.request.body.decode('utf-8'))

        try:
            user = await self.application.objects.get(UserModel, uuid=params['uuid'])
            user.username = params['username']
            await self.application.objects.update(user)
            re_data['code'] = 1
            re_data['message'] = '修改成功'
        except UserModel.DoesNotExist as e:
            self.set_status(400)
            re_data['code'] = 0
            re_data['message'] = '修改失败'

        self.finish(re_data)

    @authenticated_async
    async def get(self, *args, **kwargs):
        """获取用户列表"""
        re_data = {}
        try:
            re_list = []
            user_list = await self.application.objects.execute(UserModel.select())
            for user in user_list:
                user_dict = model_to_dict(user)
                re_list.append(user_dict)
            re_data['code'] = 1
            re_data['message'] = '查询成功'
            re_data['result'] = {
                'list': re_list
            }

        except UserModel.DoesNotExist as e:
            self.set_status(400)
            re_data['code'] = 0
            re_data['message'] = '内部查询出错'

        self.finish(json.dumps(re_data, default=json_serial))

    @authenticated_async
    async def delete(self, *args, **kwargs):
        """删除用户"""
        re_data = {}
        param = self.request.arguments
        try:
            await self.application.objects.execute(UserModel.delete().where(
                UserModel.username==param['username'][0].decode('utf-8'),
                UserModel.uuid==param['uuid'][0].decode('utf-8'))
            )
            re_data['code'] = 1
            re_data['message'] = '删除成功'

        except UserModel.DoesNotExist as e:
            self.set_status(400)
            re_data['code'] = 0
            re_data['message'] = '删除失败'

        self.finish(re_data)
