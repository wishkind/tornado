import sys
sys.path.append("..")
import tornado.web
from models.user import UserModel
from tornado.escape import json_encode

class AllUsersHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.get_default_headers()
    
    def get_default_headers(self):
        print("set default header")
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')  
    
    def get(self):
        print("get")
        result = UserModel.get_all()
        if result:
            self.write(result)
        else:
            resp = {'status': False, 'msg': '没有用户'}
            self.write(json_encode(resp))

    def post(self):
        name = self.get_argument('name')
        age = self.get_argument('age')
        UserModel.create(name, age)

        resp = {'status': True, 'msg': '成功'}
        self.write(json_encode(resp))

class UserHandler(tornado.web.RequestHandler):
    def get(self, user_id):
        result = UserModel.get(int(user_id))
        if result:
            self.write(result)
        else:
            resp = {'status': False, 'msg': '查询用户不存在'}
            self.write(json_encode(resp))

    def put(self, user_id):
        age = self.get_argument('age')
        UserModel.update(int(user_id), int(age))
        resp = {'status': True, 'msg': 'update sucess'}
        self.write(json_encode(resp))

    def delete(self, user_id):
        result = UserModel.delete(int(user_id))
        if result:
            resp = {'status': True, 'msg': result}
            self.write(json_encode(resp))
        else:
            resp = {'status': False, 'msg': '你删除的用户不存在'}
            self.write(json_encode(resp))
