from functools import wraps

from flask import jsonify, make_response, request, current_app, Request

from flask_apikit.exceptions import APIError
from flask_apikit.responses import APIResponse


def cross_domain(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        def get_allow_methods():
            """直接使用add_url_rule时定义的methods"""
            options_resp = current_app.make_default_options_response()
            return options_resp.headers['allow']

        # 自动处理OPTIONS的响应
        if request.method == 'OPTIONS':
            resp = current_app.make_default_options_response()
            h = resp.headers
            # PreFlight Request所使用的响应头
            # Max-Age
            if current_app.config['APIKIT_ACCESS_CONTROL_MAX_AGE']:
                h['Access-Control-Max-Age'] = current_app.config['APIKIT_ACCESS_CONTROL_MAX_AGE']
            # Allow-Methods
            h['Access-Control-Allow-Methods'] = get_allow_methods()
            # Allow-Headers
            if current_app.config['APIKIT_ACCESS_CONTROL_ALLOW_HEADERS']:
                h['Access-Control-Allow-Headers'] = ', '.join(
                    x.upper() for x in current_app.config['APIKIT_ACCESS_CONTROL_ALLOW_HEADERS']
                )
        else:
            resp = make_response(func(*args, **kwargs))
            h = resp.headers
        # 其他公用的响应头
        # Allow-Origin
        # 如果是字符串则直接返回
        if isinstance(current_app.config['APIKIT_ACCESS_CONTROL_ALLOW_ORIGIN'], str):
            h['Access-Control-Allow-Origin'] = current_app.config['APIKIT_ACCESS_CONTROL_ALLOW_ORIGIN']
        # 如果时列表，根据请求中的Origin动态设置Allow-Origin
        elif isinstance(current_app.config['APIKIT_ACCESS_CONTROL_ALLOW_ORIGIN'], list):
            origin = request.headers.get('Origin')
            # 如果有ORIGIN并且存在于配置白名单中则加上
            if origin and origin.lower() in [
                o.lower() for o in current_app.config['APIKIT_ACCESS_CONTROL_ALLOW_ORIGIN']
            ]:
                h['Access-Control-Allow-Origin'] = origin.lower()
        # Expose-Headers
        if current_app.config['APIKIT_ACCESS_CONTROL_EXPOSE_HEADERS']:
            h['Access-Control-Expose-Headers'] = ', '.join(
                x.upper() for x in current_app.config['APIKIT_ACCESS_CONTROL_EXPOSE_HEADERS']
            )
        # 分页的Expose-Headers
        if current_app.config['APIKIT_PAGINATION_AUTO_EXPOSE_HEADERS']:
            if 'Access-Control-Expose-Headers' not in h:
                h['Access-Control-Expose-Headers'] = ''
            else:
                h['Access-Control-Expose-Headers'] += ', '
            # 接上分页参数响应头
            h['Access-Control-Expose-Headers'] += ', '.join(x.upper() for x in [
                current_app.config['APIKIT_PAGINATION_HEADER_PAGE_KEY'],
                current_app.config['APIKIT_PAGINATION_HEADER_LIMIT_KEY'],
                current_app.config['APIKIT_PAGINATION_HEADER_COUNT_KEY']
            ])
        return resp

    return wrapper


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

    @cross_domain
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
