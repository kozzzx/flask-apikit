class APIResponse:
    def __init__(self, data, status_code=200, headers=None):
        self.data = data
        self.status_code = status_code
        self.headers = headers

    def to_tuple(self):
        return self.data, self.status_code, self.headers


class Pagination(APIResponse):

    def __init__(self, data: list, count: int, page: int, limit: int, status_code: int=200, headers: dict=None):
        """
        :param data: 数据，需要是个列表
        :param count: 数据总数
        :param page: 当前页数
        :param limit: 数据单页个数
        :param status_code: 状态码
        :param other_headers: 其他请求头
        :return:
        """
        if headers is None:
            headers = {}
        # 拼接上分页的参数
        headers = {
            'X-Pagination-Count': count,
            'X-Pagination-Page': page,
            'X-Pagination-Limit': limit,
            **headers
        }
        super().__init__(data, status_code, headers)
