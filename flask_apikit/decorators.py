from datetime import timedelta
from functools import update_wrapper
from functools import wraps

from flask import jsonify, make_response, request, current_app

from flask_apikit.exceptions import ApiError


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    """
    See: http://flask.pocoo.org/snippets/56/
    """
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, str):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, str):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)

    return decorator


def _api_response(resp=None, code=0, message=None):
    """
    将resp转换成json,没有resp则生成空字典

    :param resp:
    :param code:
    :param message:
    :return:
    """
    # 没有resp,生产空字典
    if resp is None:
        resp = {}
    # 加上错误码
    resp['e'] = code
    # 加上信息
    if message:
        resp['msg'] = message
    return jsonify(resp)


def api_view(func):
    """
    api 视图装饰器
    将ApiError,None,str,dict转换成_api_response

    :param func:
    :return:
    """

    @crossdomain(origin='*', headers=['Authorization', 'Content-Type'])
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 尝试获取response
        try:
            resp = func(*args, **kwargs)
        # 捕获到ApiError
        except ApiError as e:
            resp = (_api_response(code=e.code, message=e.message), e.status_code)
        # 没有错误
        else:
            # None => {'e':0}
            if resp is None:
                resp = _api_response()
            # response是元组，且第一个值为字典
            elif isinstance(resp, tuple):
                if len(resp) == 2 and isinstance(resp[0], dict) and isinstance(resp[1], int):
                    resp = (_api_response(resp=resp[0]), resp[1])
            # response是字典,包装成json
            elif isinstance(resp, dict):
                resp = _api_response(resp=resp)
        return resp

    return wrapper
