from flask import url_for

from flask_apikit.exceptions import APIError
from flask_apikit.responses import Pagination
from flask_apikit.views import APIView
from tests import AppTestCase


class CORSTestCase(AppTestCase):
    def test_default_configs(self):
        """测试没有配置时默认设置"""

        class Ret(APIView):
            def get(self):
                return {}

        self.app.add_url_rule('/', methods=['OPTIONS', 'PATCH', 'GET'], view_func=Ret.as_view('ret'))
        # options
        data, headers, status_code = self.options(url_for('ret'), headers={
            'Origin': 'https://example.com'
        })
        self.assertEqual(200, status_code)
        self.assertEqual('600', headers.get('Access-Control-Max-Age'))
        self.assertEqual('*', headers.get('Access-Control-Allow-Origin'))
        self.assertCountEqual(['PATCH', 'OPTIONS', 'GET', 'HEAD'],
                              headers.get('Access-Control-Allow-Methods').split(', ')),
        self.assertEqual('AUTHORIZATION, CONTENT-TYPE', headers.get('Access-Control-Allow-Headers'))
        self.assertEqual('X-PAGINATION-PAGE, X-PAGINATION-LIMIT, X-PAGINATION-COUNT',
                         headers.get('Access-Control-Expose-Headers'))
        self.assertNotIn('Access-Control-Allow-Credentials', headers)
        # get
        data, headers, status_code = self.get(url_for('ret'), headers={
            'Origin': 'https://example.com'
        })
        self.assertEqual(200, status_code)
        self.assertNotIn('Access-Control-Max-Age', headers)
        self.assertEqual('*', headers.get('Access-Control-Allow-Origin'))
        self.assertNotIn('Access-Control-Allow-Methods', headers)
        self.assertNotIn('Access-Control-Allow-Headers', headers)
        self.assertEqual('X-PAGINATION-PAGE, X-PAGINATION-LIMIT, X-PAGINATION-COUNT',
                         headers.get('Access-Control-Expose-Headers'))
        self.assertNotIn('Access-Control-Allow-Credentials', headers)

        # 当request没有提供Origin时
        # options
        data, headers, status_code = self.options(url_for('ret'))
        self.assertEqual(200, status_code)
        self.assertEqual('600', headers.get('Access-Control-Max-Age'))
        self.assertNotIn('Access-Control-Allow-Origin', headers)
        self.assertCountEqual(['PATCH', 'OPTIONS', 'GET', 'HEAD'],
                              headers.get('Access-Control-Allow-Methods').split(', ')),
        self.assertEqual('AUTHORIZATION, CONTENT-TYPE', headers.get('Access-Control-Allow-Headers'))
        self.assertEqual('X-PAGINATION-PAGE, X-PAGINATION-LIMIT, X-PAGINATION-COUNT',
                         headers.get('Access-Control-Expose-Headers'))
        self.assertNotIn('Access-Control-Allow-Credentials', headers)
        # get
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(200, status_code)
        self.assertNotIn('Access-Control-Max-Age', headers)
        self.assertNotIn('Access-Control-Allow-Origin', headers)
        self.assertNotIn('Access-Control-Allow-Methods', headers)
        self.assertNotIn('Access-Control-Allow-Headers', headers)
        self.assertEqual('X-PAGINATION-PAGE, X-PAGINATION-LIMIT, X-PAGINATION-COUNT',
                         headers.get('Access-Control-Expose-Headers'))
        self.assertNotIn('Access-Control-Allow-Credentials', headers)

    def test_disable_flask_automatic_options(self):
        """测试View不会走Flask的自动OPTIONS处理"""

        class Ret(APIView):
            def get(self):
                return {}

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        # 不允许options
        data, headers, status_code = self.options(url_for('ret'))
        self.assertEqual(405, status_code)
        # 允许get
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(200, status_code)

    def test_other_methods(self):
        """测试ALLOW_METHODS自动返回add_url_rule时methods"""

        class Ret(APIView):
            def get(self):
                return {}

        self.app.add_url_rule('/', methods=['OPTIONS', 'A', 'B', 'GET'], view_func=Ret.as_view('ret'))
        # options
        data, headers, status_code = self.options(url_for('ret'))
        self.assertEqual(200, status_code)
        self.assertCountEqual(['OPTIONS', 'HEAD', 'A', 'B', 'GET'],
                              headers.get('Access-Control-Allow-Methods').split(', ')),
        # 不会出现在get
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(200, status_code)
        self.assertNotIn('Access-Control-Allow-Methods', headers)

    def test_max_age_none(self):
        """测试不设置MAX_AGE"""
        self.app.config['APIKIT_ACCESS_CONTROL_MAX_AGE'] = None

        class Ret(APIView):
            def get(self):
                return {}

        self.app.add_url_rule('/', methods=['OPTIONS', 'PATCH', 'GET'], view_func=Ret.as_view('ret'))
        # options
        data, headers, status_code = self.options(url_for('ret'))
        self.assertEqual(200, status_code)
        self.assertNotIn('Access-Control-Max-Age', headers)
        # get
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(200, status_code)
        self.assertNotIn('Access-Control-Max-Age', headers)

    def test_max_age(self):
        """测试MAX_AGE设置"""
        self.app.config['APIKIT_ACCESS_CONTROL_MAX_AGE'] = 1

        class Ret(APIView):
            def get(self):
                return {}

        self.app.add_url_rule('/', methods=['OPTIONS', 'PATCH', 'GET'], view_func=Ret.as_view('ret'))
        # options
        data, headers, status_code = self.options(url_for('ret'))
        self.assertEqual(200, status_code)
        self.assertEqual('1', headers.get('Access-Control-Max-Age'))
        # get
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(200, status_code)
        self.assertNotIn('Access-Control-Max-Age', headers)

    def test_allow_origin_wildcard(self):
        """测试ALLOW_ORIGIN设置为通配符（同时测试了ALLOW_CREDENTIALS的状况）"""
        self.app.config['APIKIT_ACCESS_CONTROL_ALLOW_ORIGIN'] = '*'

        class Ret(APIView):
            def get(self):
                return {}

        self.app.add_url_rule('/', methods=['OPTIONS', 'PATCH', 'GET'], view_func=Ret.as_view('ret'))

        # request不携带Origin，不返回Allow-Origin
        # options
        data, headers, status_code = self.options(url_for('ret'))
        self.assertEqual(200, status_code)
        self.assertNotIn('Access-Control-Allow-Origin', headers)
        self.assertNotIn('Access-Control-Allow-Credentials', headers)
        # get
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(200, status_code)
        self.assertNotIn('Access-Control-Allow-Origin', headers)
        self.assertNotIn('Access-Control-Allow-Credentials', headers)

        # 携带Origin，返回'*'
        # options
        data, headers, status_code = self.options(url_for('ret'), headers={
            'Origin': 'https://example.com'
        })
        self.assertEqual(200, status_code)
        self.assertEqual('*', headers.get('Access-Control-Allow-Origin'))
        self.assertNotIn('Access-Control-Allow-Credentials', headers)
        # get
        data, headers, status_code = self.get(url_for('ret'), headers={
            'Origin': 'https://example.com'
        })
        self.assertEqual(200, status_code)
        self.assertEqual('*', headers.get('Access-Control-Allow-Origin'))
        self.assertNotIn('Access-Control-Allow-Credentials', headers)

    def test_allow_origin_wildcard_with_credentials(self):
        """测试ALLOW_ORIGIN设置为通配符，同时允许携带证书"""
        self.app.config['APIKIT_ACCESS_CONTROL_ALLOW_ORIGIN'] = '*'
        self.app.config['APIKIT_ACCESS_CONTROL_ALLOW_CREDENTIALS'] = True

        class Ret(APIView):
            def get(self):
                return {}

        self.app.add_url_rule('/', methods=['OPTIONS', 'PATCH', 'GET'], view_func=Ret.as_view('ret'))

        # request不携带Origin，不返回Allow-Origin
        # options
        data, headers, status_code = self.options(url_for('ret'))
        self.assertEqual(200, status_code)
        self.assertNotIn('Access-Control-Allow-Origin', headers)
        self.assertEqual('true', headers.get('Access-Control-Allow-Credentials'))
        # get
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(200, status_code)
        self.assertNotIn('Access-Control-Allow-Origin', headers)
        self.assertEqual('true', headers.get('Access-Control-Allow-Credentials'))

        # 携带Origin，因为携带了证书，返回'https://example.com'
        # options
        data, headers, status_code = self.options(url_for('ret'), headers={
            'Origin': 'https://example.com'
        })
        self.assertEqual(200, status_code)
        self.assertEqual('https://example.com', headers.get('Access-Control-Allow-Origin'))
        self.assertEqual('true', headers.get('Access-Control-Allow-Credentials'))
        # get
        data, headers, status_code = self.get(url_for('ret'), headers={
            'Origin': 'https://example.com'
        })
        self.assertEqual(200, status_code)
        self.assertEqual('https://example.com', headers.get('Access-Control-Allow-Origin'))
        self.assertEqual('true', headers.get('Access-Control-Allow-Credentials'))

    def test_allow_origin_none(self):
        """测试不设置ALLOW_ORIGIN"""
        self.app.config['APIKIT_ACCESS_CONTROL_ALLOW_ORIGIN'] = None

        class Ret(APIView):
            def get(self):
                return {}

        self.app.add_url_rule('/', methods=['OPTIONS', 'PATCH', 'GET'], view_func=Ret.as_view('ret'))
        # options
        data, headers, status_code = self.options(url_for('ret'))
        self.assertEqual(200, status_code)
        self.assertNotIn('Access-Control-Allow-Origin', headers)
        # get
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(200, status_code)
        self.assertNotIn('Access-Control-Allow-Origin', headers)

    def test_allow_origin_str(self):
        """测试ALLOW_ORIGIN设置为字符串，直接返回"""
        self.app.config['APIKIT_ACCESS_CONTROL_ALLOW_ORIGIN'] = 'https://example.com'

        class Ret(APIView):
            def get(self):
                return {}

        # request不携带Origin，不返回Allow-Origin
        self.app.add_url_rule('/', methods=['OPTIONS', 'PATCH', 'GET'], view_func=Ret.as_view('ret'))
        # options
        data, headers, status_code = self.options(url_for('ret'))
        self.assertEqual(200, status_code)
        self.assertNotIn('Access-Control-Allow-Origin', headers)
        # get
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(200, status_code)
        self.assertNotIn('Access-Control-Allow-Origin', headers)

        # 携带一致的Origin，返回
        # options
        data, headers, status_code = self.options(url_for('ret'), headers={
            'Origin': 'https://example.com'
        })
        self.assertEqual(200, status_code)
        self.assertEqual('https://example.com', headers.get('Access-Control-Allow-Origin'))
        # get
        data, headers, status_code = self.get(url_for('ret'), headers={
            'Origin': 'https://example.com'
        })
        self.assertEqual(200, status_code)
        self.assertEqual('https://example.com', headers.get('Access-Control-Allow-Origin'))

        # 携带不一致的Origin，不返回
        # options
        data, headers, status_code = self.options(url_for('ret'), headers={
            'Origin': 'https://1.example.com'
        })
        self.assertEqual(200, status_code)
        self.assertNotIn('Access-Control-Allow-Origin', headers)
        # get
        data, headers, status_code = self.get(url_for('ret'), headers={
            'Origin': 'https://1.example.com'
        })
        self.assertEqual(200, status_code)
        self.assertNotIn('Access-Control-Allow-Origin', headers)

    def test_allow_origin_list(self):
        """测试ALLOW_ORIGIN设置为字符串，直接返回"""
        self.app.config['APIKIT_ACCESS_CONTROL_ALLOW_ORIGIN'] = [
            'https://1.example.com',
            'http://1.example.com',
            'https://2.example.com'
        ]

        class Ret(APIView):
            def get(self):
                return {}

        self.app.add_url_rule('/', methods=['OPTIONS', 'PATCH', 'GET'], view_func=Ret.as_view('ret'))

        # 请求没有Origin时，不返回Allow-Origin
        # options
        data, headers, status_code = self.options(url_for('ret'))
        self.assertEqual(200, status_code)
        self.assertNotIn('Access-Control-Allow-Origin', headers)
        # get
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(200, status_code)
        self.assertNotIn('Access-Control-Allow-Origin', headers)

        # Origin存在于列表中时，Allow-Origin返回相应域名
        # options
        data, headers, status_code = self.options(url_for('ret'), headers={
            'Origin': 'https://1.example.com'
        })
        self.assertEqual(200, status_code)
        self.assertEqual('https://1.example.com', headers.get('Access-Control-Allow-Origin'))
        # get
        data, headers, status_code = self.get(url_for('ret'), headers={
            'Origin': 'https://1.example.com'
        })
        self.assertEqual(200, status_code)
        self.assertEqual('https://1.example.com', headers.get('Access-Control-Allow-Origin'))

        # http Origin存在于列表中时，Allow-Origin返回相应域名
        # options
        data, headers, status_code = self.options(url_for('ret'), headers={
            'Origin': 'http://1.example.com'
        })
        self.assertEqual(200, status_code)
        self.assertEqual('http://1.example.com', headers.get('Access-Control-Allow-Origin'))
        # get
        data, headers, status_code = self.get(url_for('ret'), headers={
            'Origin': 'http://1.example.com'
        })
        self.assertEqual(200, status_code)
        self.assertEqual('http://1.example.com', headers.get('Access-Control-Allow-Origin'))

        # Origin不存在于列表中时，不返回Allow-Origin
        # options
        data, headers, status_code = self.options(url_for('ret'), headers={
            'Origin': 'https://3.example.com'
        })
        self.assertEqual(200, status_code)
        self.assertNotIn('Access-Control-Allow-Origin', headers)
        # get
        data, headers, status_code = self.get(url_for('ret'), headers={
            'Origin': 'https://3.example.com'
        })
        self.assertEqual(200, status_code)
        self.assertNotIn('Access-Control-Allow-Origin', headers)

    def test_allow_headers_none(self):
        """测试不设置ALLOW_HEADERS"""
        self.app.config['APIKIT_ACCESS_CONTROL_ALLOW_HEADERS'] = None

        class Ret(APIView):
            def get(self):
                return {}

        self.app.add_url_rule('/', methods=['OPTIONS', 'PATCH', 'GET'], view_func=Ret.as_view('ret'))
        # options
        data, headers, status_code = self.options(url_for('ret'))
        self.assertEqual(200, status_code)
        self.assertNotIn('Access-Control-Allow-Headers', headers)
        # get
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(200, status_code)
        self.assertNotIn('Access-Control-Allow-Headers', headers)

    def test_allow_headers(self):
        """测试ALLOW_HEADERS设置"""
        self.app.config['APIKIT_ACCESS_CONTROL_ALLOW_HEADERS'] = ['h1', 'h2']

        class Ret(APIView):
            def get(self):
                return {}

        self.app.add_url_rule('/', methods=['OPTIONS', 'PATCH', 'GET'], view_func=Ret.as_view('ret'))
        # options
        data, headers, status_code = self.options(url_for('ret'))
        self.assertEqual(200, status_code)
        self.assertEqual('H1, H2', headers.get('Access-Control-Allow-Headers'))
        # 不会出现在get
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(200, status_code)
        self.assertNotIn('Access-Control-Allow-Headers', headers)

    def test_expose_headers(self):
        # todo: 测试EXPOSE_HEADERS设置
        pass
