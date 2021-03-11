class UserModel(object):
    #初始化用户列表
    users = {
        1:{"name":"吴花花","age":25},
        2:{"name":"搞基基","age":21},
        3:{"name":"周菲菲","age":26},
        4:{"name":"程吉吉","age":13},
    }

    #cls是当前类。类方法不要用类的实例来调用，要用当前类来调用
    @classmethod
    def get(cls,user_id):
        if user_id in cls.users:
            return cls.users[user_id]
        else:
            return None

    @classmethod
    def update(cls,user_id,age):
        cls.users[user_id]['age'] = age

    @classmethod
    def delte(cls,user_id):
        #如果存在，则删除。如果不存在。则返回none
        if user_id in cls.users:
            return cls.users.pop(user_id)
        else:
            return None

    @classmethod
    def get_all(cls):
        return cls.users

    #创建新用户
    @classmethod
    def create(cls,name,age):
        user_dict = {'name':name,'age':age}
        #获取新用户的id+1
        max_id = max(cls.users.keys()) + 1
        #添加新用户
        cls.users[max_id] = user_dict
