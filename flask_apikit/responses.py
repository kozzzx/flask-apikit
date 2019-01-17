from flask import current_app


class APIResponse:
    def __init__(self, data, status_code=200, headers=None):
        self.data = data
        self.status_code = status_code
        self.headers = headers

    def to_tuple(self):
        return self.data, self.status_code, self.headers


class Pagination(APIResponse):
    def __init__(self, data: list, count: int, page: int, limit: int, status_code: int = 200, headers: dict = None):
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
        # 拼接上分页的参数
        headers[current_app.config['APIKIT_PAGINATION_HEADER_PAGE_KEY']] = page
        headers[current_app.config['APIKIT_PAGINATION_HEADER_LIMIT_KEY']] = limit
        headers[current_app.config['APIKIT_PAGINATION_HEADER_COUNT_KEY']] = count
        super().__init__(data, status_code, headers)
