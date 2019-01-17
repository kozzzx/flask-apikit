from flask import current_app, _app_ctx_stack


class APIResponse:
    def __init__(self, data, status_code=200, headers=None):
        self.data = data
        self.status_code = status_code
        self.headers = headers

    def to_tuple(self):
        return self.data, self.status_code, self.headers


class Pagination(APIResponse):
    def __init__(self, data: list, count: int, page: int = None, limit: int = None, status_code: int = 200,
                 headers: dict = None):
        """
        :param data: 数据
        :param count: 总条目数
        :param page: 当前页数
        :param limit: 每页条目数
        :param status_code: 状态码
        :param headers: 其他请求头
        :return:
        """
        if headers is None:
            headers = {}
        # 从app上下文获取分页数据
        ctx = _app_ctx_stack.top
        if ctx is not None and hasattr(ctx, 'apikit_pagination'):
            if page is None:
                page = ctx.apikit_pagination['page']
            if limit is None:
                limit = ctx.apikit_pagination['limit']
        # 如果page/limit仍未None则报错
        if None in (page, limit):
            raise RuntimeError(
                'Need use APIView.get_pagination() before Pagination() or specify parameters "page" & "limit"]'
            )
        # 拼接上分页的参数
        headers[current_app.config['APIKIT_PAGINATION_HEADER_PAGE_KEY']] = page
        headers[current_app.config['APIKIT_PAGINATION_HEADER_LIMIT_KEY']] = limit
        headers[current_app.config['APIKIT_PAGINATION_HEADER_COUNT_KEY']] = count
        super().__init__(data, status_code, headers)
