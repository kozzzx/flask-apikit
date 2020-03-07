import math
from flask import current_app, jsonify, request


class APIResponse:
    """基础的API响应"""
    def __init__(self, data, status_code=200, headers=None):
        self.data = data
        self.status_code = status_code
        self.headers = headers

    def to_tuple(self):
        """返回make_response所用的元组，并将数据部分json化"""
        return jsonify(self.data), self.status_code, self.headers


class Pagination(APIResponse):
    """分页的API响应"""
    def __init__(self,
                 default_limit: int = None,
                 max_limit: int = None,
                 page_key: str = None,
                 limit_key: str = None,
                 status_code: int = 200,
                 headers: dict = None,
                 auto_expose_headers=True):
        """
        :param default_limit: 请求中没有“每页条目数”参数时，则使用此值（为None则使用插件配置的值）
        :param max_limit: “每页最大条目数”，为0则不限制（为None则使用插件配置的值）
        :param page_key: “页数”的key（为None则使用插件配置的值）
        :param limit_key: “每页条目数”的key（为None则使用插件配置的值）
        :param status_code: 状态码
        :param headers: 其他请求头
        :param auto_expose_headers: 自动加入分页的Access-Control-Expose-Headers
        :return:
        """
        # 默认值
        self.count = 0
        # 从query中获取分页参数
        self._parse_query(default_limit=default_limit,
                          max_limit=max_limit,
                          page_key=page_key,
                          limit_key=limit_key)
        # 自动加入分页所用的 Access-Control-Expose-Headers
        if headers is None:
            headers = {}
        if auto_expose_headers:
            # 如果已有Expose-Headers，同时有值，则将其全部大小并加一个逗号
            if 'Access-Control-Expose-Headers' in headers and headers[
                    'Access-Control-Expose-Headers']:
                headers['Access-Control-Expose-Headers'] += ', '
            else:
                headers['Access-Control-Expose-Headers'] = ''
            headers['Access-Control-Expose-Headers'] += ', '.join(x.upper(
            ) for x in [
                current_app.config['APIKIT_PAGINATION_HEADER_PAGE_KEY'],
                current_app.config['APIKIT_PAGINATION_HEADER_LIMIT_KEY'],
                current_app.config['APIKIT_PAGINATION_HEADER_COUNT_KEY'],
                current_app.config['APIKIT_PAGINATION_HEADER_PAGE_COUNT_KEY']
            ])
        super().__init__([], status_code, headers)

    def set_data(self, data, count):
        self.data = data
        self.count = count
        self._set_pagination_headers()
        return self

    def _parse_query(self,
                     default_limit: int = None,
                     max_limit: int = None,
                     page_key: str = None,
                     limit_key: str = None):
        """
        从request.args中获取分页数据，并返回(skip, limit, page)

        :param default_limit: 请求中没有“每页条目数”参数时，则使用此值（为None则使用插件配置的值）
        :param max_limit: “每页最大条目数”，为0则不限制（为None则使用插件配置的值）
        :param page_key: “页数”的key（为None则使用插件配置的值）
        :param limit_key: “每页条目数”的key（为None则使用插件配置的值）
        :return:
        """
        # 获取配置
        if default_limit is None:
            default_limit = current_app.config[
                'APIKIT_PAGINATION_DEFAULT_LIMIT']
        if max_limit is None:
            max_limit = current_app.config['APIKIT_PAGINATION_MAX_LIMIT']
        if page_key is None:
            page_key = current_app.config['APIKIT_PAGINATION_PAGE_KEY']
        if limit_key is None:
            limit_key = current_app.config['APIKIT_PAGINATION_LIMIT_KEY']
        # 获取页数，默认1
        page = request.args.get(page_key, 1, int)
        if page < 1:
            page = 1
        # 限制数量，默认default_limit
        limit = request.args.get(limit_key, default_limit, int)
        if limit < 1:
            limit = default_limit
        if max_limit and limit > max_limit:  # 限制最大数量
            limit = max_limit
        self.page = page
        self.limit = limit
        self.skip = (page - 1) * limit  # 计算出要跳过的数量

    def _set_pagination_headers(self):
        """设置分页头"""
        self.headers[current_app.
                     config['APIKIT_PAGINATION_HEADER_PAGE_KEY']] = self.page
        self.headers[current_app.
                     config['APIKIT_PAGINATION_HEADER_LIMIT_KEY']] = self.limit
        self.headers[current_app.
                     config['APIKIT_PAGINATION_HEADER_COUNT_KEY']] = self.count
        self.headers[current_app.config[
            'APIKIT_PAGINATION_HEADER_PAGE_COUNT_KEY']] = math.ceil(
                self.count / self.limit)
