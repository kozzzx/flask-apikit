import math
from flask import current_app, _app_ctx_stack, jsonify


class APIResponse:
    def __init__(self, data, status_code=200, headers=None):
        self.data = data
        self.status_code = status_code
        self.headers = headers

    def to_tuple(self):
        """返回make_response所用的元组，并将数据部分json化"""
        return jsonify(self.data), self.status_code, self.headers


class Pagination(APIResponse):
    def __init__(
            self,
            data: list = None,
            count: int = 0,
            limit: int = None,
            page: int = None,
            status_code: int = 200,
            headers: dict = None,
            auto_expose_headers=True
    ):
        """
        :param data: 数据
        :param count: 总条目数
        :param page: 当前页数
        :param limit: 每页条目数
        :param status_code: 状态码
        :param headers: 其他请求头
        :return:
        """
        if data is None:
            data = []
        if headers is None:
            headers = {}
        # 从app上下文获取分页数据
        ctx = _app_ctx_stack.top
        if ctx is not None and hasattr(ctx, 'apikit_pagination'):
            if page is None:
                page = ctx.apikit_pagination['page']
            if limit is None:
                limit = ctx.apikit_pagination['limit']
        # 如果page/limit仍为None则报错
        if None in (page, limit):
            raise ValueError(
                'Need use APIView.get_pagination() before Pagination() or specify parameters "page" & "limit"]'
            )
        # 拼接上分页头
        headers[current_app.config['APIKIT_PAGINATION_HEADER_PAGE_KEY']] = page
        headers[current_app.config['APIKIT_PAGINATION_HEADER_LIMIT_KEY']] = limit
        headers[current_app.config['APIKIT_PAGINATION_HEADER_COUNT_KEY']] = count
        headers[current_app.config['APIKIT_PAGINATION_HEADER_PAGE_COUNT_KEY']] = math.ceil(count / limit)
        # 加入分页所用的 Access-Control-Expose-Headers
        if auto_expose_headers:
            # 如果已有Expose-Headers，同时有值，则加一个逗号 todo: 测试如果headers提供了Access-Control-Expose-Headers，不会被覆盖
            if 'Access-Control-Expose-Headers' in headers and headers['Access-Control-Expose-Headers']:
                headers['Access-Control-Expose-Headers'] += ', '
            else:
                headers['Access-Control-Expose-Headers'] = ''
            headers['Access-Control-Expose-Headers'] += ', '.join(x.upper() for x in [
                current_app.config['APIKIT_PAGINATION_HEADER_PAGE_KEY'],
                current_app.config['APIKIT_PAGINATION_HEADER_LIMIT_KEY'],
                current_app.config['APIKIT_PAGINATION_HEADER_COUNT_KEY'],
                current_app.config['APIKIT_PAGINATION_HEADER_PAGE_COUNT_KEY']
            ])
            print(headers['Access-Control-Expose-Headers'])
        super().__init__(data, status_code, headers)
