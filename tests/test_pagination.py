from flask import url_for

from flask_apikit.exceptions import APIError
from flask_apikit.responses import Pagination
from flask_apikit.views import APIView
from tests import AppTestCase


class PaginationTestCase(AppTestCase):
    def test_pagination(self):
        """测试返回分页"""

        class Ret(APIView):
            def get(self):
                return Pagination([1, 2], count=100, page=2, limit=10)

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(status_code, 200)
        self.assertEqual(headers.get('X-Pagination-Count'), '100')
        self.assertEqual(headers.get('X-Pagination-Limit'), '10')
        self.assertEqual(headers.get('X-Pagination-Page'), '2')
        self.assertEqual(data[0], 1)
        self.assertEqual(data[1], 2)

    def test_pagination_with_status(self):
        """测试返回分页+状态码"""

        class Ret(APIView):
            def get(self):
                return Pagination([1, 2], count=100, page=2, limit=10, status_code=511)

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(status_code, 511)
        self.assertEqual(headers.get('X-Pagination-Count'), '100')
        self.assertEqual(headers.get('X-Pagination-Limit'), '10')
        self.assertEqual(headers.get('X-Pagination-Page'), '2')
        self.assertEqual(data[0], 1)
        self.assertEqual(data[1], 2)

    def test_pagination_other_headers(self):
        """测试返回分页包含其他headers"""

        class Ret(APIView):
            def get(self):
                return Pagination([1, 2], count=100, page=2, limit=10, headers={'AAA': 'a', 'bbb': 'B'})

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(status_code, 200)
        self.assertEqual(headers.get('X-Pagination-Count'), '100')
        self.assertEqual(headers.get('X-Pagination-Limit'), '10')
        self.assertEqual(headers.get('X-Pagination-Page'), '2')
        self.assertEqual(headers.get('AAA'), 'a')
        self.assertEqual(headers.get('bbb'), 'B')
        self.assertEqual(data[0], 1)
        self.assertEqual(data[1], 2)
