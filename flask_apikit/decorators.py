from functools import wraps

from flask import jsonify, make_response, request, current_app, Response

from flask_apikit.exceptions import APIError
from flask_apikit.responses import APIResponse


def api_cors(func):
    """
    处理Response的CORS响应头， 返回一个Response对象

    See also：[MDN CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)
    See also：[CORS Server Flowchart](https://www.html5rocks.com/static/images/cors_server_flowchart.png)
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 请求不含有Origin，则直接返回，不进行CORS处理
        origin = request.headers.get('Origin')
        if not origin:
            return make_response(func(*args, **kwargs))

        # === Preflight Request ===
        if request.method == 'OPTIONS':
            # 生成Flask默认的Options Response
            resp = current_app.make_default_options_response()
            h = resp.headers
            # ==> Access-Control-Allow-Methods
            h['Access-Control-Allow-Methods'] = resp.headers.get('allow')  # add_url_rule中定义的methods，会自动加上HEAD方法
            # ==> Access-Control-Allow-Headers
            if current_app.config['APIKIT_ACCESS_CONTROL_ALLOW_HEADERS']:
                h['Access-Control-Allow-Headers'] = ', '.join(
                    x.upper() for x in
                    current_app.config['APIKIT_ACCESS_CONTROL_ALLOW_HEADERS'])
            # ==> Access-Control-Max-Age
            if current_app.config['APIKIT_ACCESS_CONTROL_MAX_AGE']:
                h['Access-Control-Max-Age'] = current_app.config[
                    'APIKIT_ACCESS_CONTROL_MAX_AGE']
        # === Actual Request ===
        else:
            resp = make_response(func(*args, **kwargs))
            h = resp.headers
            # ==> Access-Control-Expose-Headers
            if current_app.config['APIKIT_ACCESS_CONTROL_EXPOSE_HEADERS']:
                # 如果已有Expose-Headers，同时有值，则加一个逗号
                if 'Access-Control-Expose-Headers' in h and h[
                        'Access-Control-Expose-Headers']:
                    h['Access-Control-Expose-Headers'] += ', '
                else:
                    h['Access-Control-Expose-Headers'] = ''
                h['Access-Control-Expose-Headers'] += ', '.join(
                    x.upper() for x in
                    current_app.config['APIKIT_ACCESS_CONTROL_EXPOSE_HEADERS'])
        # === 其他公用的响应头 ===
        # ==> Access-Control-Allow-Credentials
        if current_app.config[
                'APIKIT_ACCESS_CONTROL_ALLOW_CREDENTIALS'] is True:
            h['Access-Control-Allow-Credentials'] = 'true'
        # ==> Access-Control-Allow-Origin
        # 设置为"*"，表示允许所有Origin访问
        if current_app.config['APIKIT_ACCESS_CONTROL_ALLOW_ORIGIN'] == '*':
            # 如果允许请求附带身份凭证则必须返回与Origin相同的值
            # See also：[MDN CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS#Requests_with_credentials)
            if current_app.config[
                    'APIKIT_ACCESS_CONTROL_ALLOW_CREDENTIALS'] is True:
                h['Access-Control-Allow-Origin'] = origin
            # 其他情况直接返回"*"通配符
            else:
                h['Access-Control-Allow-Origin'] = '*'
        # 设置了其他参数
        else:
            # 设置为字符串，表示允许一个域名，与请求头的Origin一致则返回
            if isinstance(
                    current_app.config['APIKIT_ACCESS_CONTROL_ALLOW_ORIGIN'],
                    str):
                if origin.lower() == current_app.config[
                        'APIKIT_ACCESS_CONTROL_ALLOW_ORIGIN'].lower():
                    h['Access-Control-Allow-Origin'] = origin
            # 设置为列表，表示允许多个域名，包含请求头的Origin则返回
            elif isinstance(
                    current_app.config['APIKIT_ACCESS_CONTROL_ALLOW_ORIGIN'],
                    list):
                if origin.lower() in [
                        o.lower() for o in current_app.
                        config['APIKIT_ACCESS_CONTROL_ALLOW_ORIGIN']
                ]:
                    h['Access-Control-Allow-Origin'] = origin
        return resp

    return wrapper


def api_response(func):
    """
    将视图返回的值处理为flask.app.make_response所用的元组（参数rv），并将数据部分json化

    :param func:
    :return:
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 尝试获取response
        try:
            resp = func(*args, **kwargs)
        # 捕获到APIError
        except APIError as e:
            return e.to_tuple()
        # 没有错误
        else:
            # 如果发现返回数据为None，则返回204
            if resp is None:
                resp = '', 204
            # 如果是字典或列表，转换为json后返回
            elif isinstance(resp, (dict, list)):
                resp = jsonify(resp)
            # 如果是有两个元素以上的元组，且第一个值为字典或列表，则将第一个值转换为json（P.S. 后两个是状态码，HTTP头）
            elif isinstance(resp, tuple) and len(resp) > 1 and isinstance(
                    resp[0], (dict, list)):
                resp = (jsonify(resp[0]), *resp[1:])
            # APIResponse直接返回
            elif isinstance(resp, APIResponse):
                resp = resp.to_tuple()
            return resp

    return wrapper
