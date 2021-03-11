import json
import requests
import logging 
from python.akskapp.scripts.api.baseHandler import RclassAuthSdk(object)
#登录

def loginToAuthcenter(self, username, password):

    resp=None

    headers= {"Content-Type": "application/json"}

    data= {"username": username,"password": password}
    try:

        resp= requests.post("http://localhost:8888/login", 
                              data=json.dumps(data), 
                              headers=headers)
        print(json.loads(resp.content))
    exceptException as e:

    logging.error(e)
    return resp

def logout(self):
    pass

host = options.conf.authcenter

#是否已经登录

def isLogin(self, sessionid, verification):

    headers= {"session_id": sessionid, "verification": verification}

    resp= requests.post("http://localhost:8888/islogin", cookies=headers)

    content= json.loads(str(resp.content, encoding="utf-8"))
    if resp.status_code == 200 and content is not None and content !={}:
        print(content)

        return True, content
    print(resp.content)

    return False, resp.content
def needPermission(permissionstr):
    pass
def decorator(func):
    pass
def hasPermission(self,*args, **kw):

    sessionid= self.get_cookie("session_id")

    verification= self.get_cookie("verification")#print(sessionid)

    print(verification)

    islogin, content = AuthSdk().isLogin(sessionid, verification)

    permissionList=[]
    if islogin:

        permissionList= content["permissions"]
    else:

        self.set_status(401)

        self.write(R().errorCodeMsg(401, "认证不通过，请确认是否登录"))
    return

    print('%s %s %s():' % (self, permissionstr, func.__name__))

    if permissionstr not inpermissionList:

        self.set_status(403)

        self.write(R().errorCodeMsg(403, "没有访问权限"))
        return

    else:
        return func(self, *args, **kw)
return hasPermissionreturndecorator
if __name__ == '__main__':

    asdk=AuthSdk()

    boolres, content= asdk.isLogin('NzViYWU2M2JmNDRiOGQ5ZTMwZWFmN2Q2ZDRiYzI3NzRjNWIzYzE0ZWE5MjM1NDQwMzI2ODBkNTI4Mjg4Nzk5Yg==|1555926739|6a69c6cbf0384f6c26d42384ca046b5c9495a201','NjQxNDY4Yzk0MGYzYjUxOTJiNmFiODMzMjZiMjZjZDQ1Yzk4OGUxMzg3OGU0Y2RkNTJkMDBlYWQwYTFjMWEzMg==|1555926739|f4ed1b4254bbe38dd604e7199c11a532b8240228')#print(boolres)

    asdk.loginToAuthcenter("admin", "123456")
