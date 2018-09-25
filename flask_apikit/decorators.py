from datetime import timedelta
from functools import update_wrapper
from functools import wraps

from flask import jsonify, make_response, request, current_app

from flask_apikit.exceptions import APIError
from flask_apikit.responses import APIResponse


def crossdomain(origin=None, methods=None, headers=None, expose_headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    """
    See: http://flask.pocoo.org/snippets/56/
    """
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, str):
        headers = ', '.join(x.upper() for x in headers)
    if expose_headers is not None and not isinstance(expose_headers, str):
        expose_headers = ', '.join(x.upper() for x in expose_headers)
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
            if expose_headers is not None:
                h['Access-Control-Expose-Headers'] = expose_headers
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
    将APIError,None,str,dict转换成_api_response

    :param func:
    :return:
    """

    @crossdomain(origin='*', headers=['Authorization', 'Content-Type'],
                 expose_headers=['X-Pagination-Count', 'X-Pagination-Page', 'X-Pagination-Limit'])
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 尝试获取response
        try:
            resp = func(*args, **kwargs)
        # 捕获到APIError
        except APIError as e:
            return _api_error_response(e)
        # 没有错误
        else:
            # 将APIResponse转化成元组，以供下面处理
            if isinstance(resp, APIResponse):
                resp = resp.to_tuple()
            # 如果发现返回数据为None，则返回204
            if resp is None:
                resp = '', 204
            # 如果字典或列表，jsonify后返回
            elif isinstance(resp, (dict, list)):
                resp = jsonify(resp)
            # 如果是元组，则只jsonify第一个值（P.S. 后两个是状态码，HTTP头）
            elif isinstance(resp, tuple):
                if isinstance(resp[0], (dict, list)):
                    resp = (jsonify(resp[0]), *resp[1:])
            return resp

    return wrapper
