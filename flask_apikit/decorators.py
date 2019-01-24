from functools import wraps

from flask import jsonify, make_response, request, current_app, Request

from flask_apikit.exceptions import APIError
from flask_apikit.responses import APIResponse


def cross_domain(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        def get_allow_methods():
            """返回add_url_rule时定义的methods"""
            options_resp = current_app.make_default_options_response()
            return options_resp.headers['allow']

        # 生成Response
        if request.method == 'OPTIONS':
            resp = current_app.make_default_options_response()
        else:
            resp = make_response(func(*args, **kwargs))
        # 为Response添加响应头
        h = resp.headers
        # === PreFlight专用的响应头 ===
        if request.method == 'OPTIONS':
            # ==> Access-Control-Max-Age
            if current_app.config['APIKIT_ACCESS_CONTROL_MAX_AGE']:
                h['Access-Control-Max-Age'] = current_app.config['APIKIT_ACCESS_CONTROL_MAX_AGE']
            # ==> Access-Control-Allow-Methods
            h['Access-Control-Allow-Methods'] = get_allow_methods()
            # ==> Access-Control-Allow-Headers
            if current_app.config['APIKIT_ACCESS_CONTROL_ALLOW_HEADERS']:
                h['Access-Control-Allow-Headers'] = ', '.join(
                    x.upper() for x in current_app.config['APIKIT_ACCESS_CONTROL_ALLOW_HEADERS']
                )
        # === 其他公用的响应头 ===
        # ==> Access-Control-Allow-Credentials
        if current_app.config['APIKIT_ACCESS_CONTROL_ALLOW_CREDENTIALS'] is True:
            h['Access-Control-Allow-Credentials'] = 'true'
        # ==> Access-Control-Allow-Origin
        origin = request.headers.get('Origin')  # 请求头的Origin
        if origin:
            # 将Origin处理为小写
            origin = origin.lower()
            # 是"*"通配符，允许所有Origin访问
            if current_app.config['APIKIT_ACCESS_CONTROL_ALLOW_ORIGIN'] == '*':
                # 如果允许携带证书则必须返回与Origin相同的值
                # See also：https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#Requests_with_credentials
                if current_app.config['APIKIT_ACCESS_CONTROL_ALLOW_CREDENTIALS'] is True:
                    h['Access-Control-Allow-Origin'] = origin
                # 其他情况直接返回"*"通配符
                else:
                    h['Access-Control-Allow-Origin'] = '*'
            # 指定了其他参数
            else:
                # ALLOW_ORIGIN是字符串，且与请求头的Origin一致
                if isinstance(current_app.config['APIKIT_ACCESS_CONTROL_ALLOW_ORIGIN'], str):
                    if origin == current_app.config['APIKIT_ACCESS_CONTROL_ALLOW_ORIGIN'].lower():
                        h['Access-Control-Allow-Origin'] = origin
                # ALLOW_ORIGIN是列表，且包含请求头的Origin
                elif isinstance(current_app.config['APIKIT_ACCESS_CONTROL_ALLOW_ORIGIN'], list):
                    if origin in [
                        o.lower() for o in current_app.config['APIKIT_ACCESS_CONTROL_ALLOW_ORIGIN']
                    ]:
                        h['Access-Control-Allow-Origin'] = origin
        # ==> Access-Control-Expose-Headers
        if current_app.config['APIKIT_ACCESS_CONTROL_EXPOSE_HEADERS']:
            h['Access-Control-Expose-Headers'] = ', '.join(
                x.upper() for x in current_app.config['APIKIT_ACCESS_CONTROL_EXPOSE_HEADERS']
            )
        # ==> 自动加入分页所用的 Access-Control-Expose-Headers
        if current_app.config['APIKIT_PAGINATION_AUTO_EXPOSE_HEADERS']:
            if 'Access-Control-Expose-Headers' not in h:
                h['Access-Control-Expose-Headers'] = ''
            else:
                h['Access-Control-Expose-Headers'] += ', '
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
