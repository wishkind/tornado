from urllib import parse


def format_str_params(params):
    if isinstance(params, bytes):
        params = params.decode('utf-8')

    elif not isinstance(params, str):
        raise TypeError('参数类型错误 需要字符串')

    re_data = {}
    new_params = params.split('&')
    for new_param in new_params:
        data = new_param.split('=')
        re_data[data[0]] = parse.unquote(data[1])
    return re_data


def format_list_params(params):
    re_data = {}
    if isinstance(params, dict):
        for key, value in params.items():
            locals()[f'{key}'] = []
            if len(value) > 1:
                for item in value:
                    eval('{}'.format(key)).append(str(item, encoding='utf-8'))
                re_data['{}'.format(key)] = eval('{}'.format(key))
            else:
                re_data['{}'.format(key)] = str(value[0], encoding='utf-8')
    else:
        return False
    return re_data
