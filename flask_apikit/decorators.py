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
        def wrapper(*args, **kwargs):
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
        return update_wrapper(wrapper, f)

    return decorator


def _api_error_response(e):
    return jsonify({
        'error': e.__class__.__name__,
        'code': e.code,
        'message': e.message
    }), e.status_code


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
            resp = _api_error_response(e)
        # 没有错误
        else:
            # None => {'e':0}
            if resp is None:
                resp = '', 204
            # response是元组，且第一个值为字典或列表
            elif isinstance(resp, tuple) and len(resp) == 2:
                if isinstance(resp[0], (dict, list)) and isinstance(resp[1], int):
                    resp = (jsonify(resp[0]), resp[1])
            # response是字典或列表,包装成json
            elif isinstance(resp, (dict, list)):
                resp = jsonify(resp)
        return resp

    return wrapper
