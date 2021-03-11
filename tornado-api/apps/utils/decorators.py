
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
import functools
import jwt

from apps.models.user_models import UserModel


def authenticated_async(method):
    @functools.wraps(method)
    async def wrapper(self, *args, **kwargs):
        re_data = {}
        token = self.request.headers.get("token", None)
        if token and token != 'undefined':
            try:
                send_data = jwt.decode(
                    token,
                    self.settings["secret_key"],
                    leeway=self.settings["jwt_expire"],
                    options={"verify_exp": True}
                )
                user_id = send_data["id"]
                try:
                    user = await self.application.objects.get(UserModel, id=int(user_id))
                    self._current_user = user
                    await method(self, *args, **kwargs)
                except UserModel.DoesNotExist as e:
                    self.set_status(401)
                    re_data['code'] = 0
                    re_data['message'] = '登录失败！'
                    self.finish(re_data)
            except jwt.ExpiredSignatureError as e:
                self.set_status(401)
                re_data['code'] = 0
                re_data['message'] = '认证失败！'
                self.finish(re_data)
        else:
            self.set_status(401)
            re_data['code'] = 0
            re_data['message'] = '请登录！'
            self.finish(re_data)

    return wrapper
