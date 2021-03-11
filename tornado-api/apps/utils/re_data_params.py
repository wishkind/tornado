def resSuccess(msg, error=None):
    params = {}
    if msg == '失败':
        params['code'] = 0
        params['message'] = error or msg
    elif msg == '成功':
        params['code'] = 1
        params['message'] = error or msg
    return params
