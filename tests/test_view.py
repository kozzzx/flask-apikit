from flask import url_for
from flask_apikit.utils.query import QueryParser
from flask_apikit.views import APIView
from tests import AppTestCase


class QueryTestCase(AppTestCase):
    def test_get_json(self):
        """测试get_json"""

        class Ret(APIView):
            """原样返回get_json数据"""

            def post(self):
                return self.get_json()

        self.app.add_url_rule('/', methods=['POST'], view_func=Ret.as_view('ret'))

        # 不提交数据
        data, headers, status_code = self.post(
            url_for('ret')
        )
        self.assertEqual(status_code, 200)
        self.assertEqual(data, {})

        # 提交空数据
        data, headers, status_code = self.post(
            url_for('ret'),
            json={}
        )
        self.assertEqual(status_code, 200)
        self.assertEqual(data, {})

        # 提交各种数据
        request_data = {
            'ne_int': -1,
            'zero': 0,
            'int': 1,
            'float': 1.1,
            'str': '1',
            'true': True,
            'false': False,
            'int_list': [1, 2],
            'str_list': ['1', '2'],
            'float_list': [1.1, 2.2],
            'bool_list': [True, False],
            'list_in_list': [[1, 2], ['1', '2']],
            'dict': {
                'list': [1, '2'], 'dict': {'1': 1},
                'true': True, 'false': False,
                'int': 1, 'float': 1.1
            }
        }
        data, headers, status_code = self.post(
            url_for('ret'),
            json=request_data
        )
        self.assertEqual(status_code, 200)
        self.assertEqual(data, request_data)

    def test_get_query(self):
        """测试get_query"""

        class Ret(APIView):
            """原样返回get_json数据"""

            def get(self):
                return self.get_query({
                    'ne_int': QueryParser.int,
                    'zero': QueryParser.int,
                    'int': QueryParser.int,
                    'float': QueryParser.float,
                    'true': QueryParser.bool,
                    'false': QueryParser.bool,
                    'int_list': [QueryParser.int],
                    'str_list': [],
                    'float_list': [QueryParser.float],
                    'bool_list': [QueryParser.bool]
                })

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))

        # 不提交数据，返回空数组
        data, headers, status_code = self.get(
            url_for('ret')
        )
        self.assertEqual(status_code, 200)
        self.assertEqual(data, {})

        # 提交空数据，返回空数组
        data, headers, status_code = self.get(
            url_for('ret'),
            query_string={}
        )
        self.assertEqual(status_code, 200)
        self.assertEqual(data, {})

        # 提交没有解析器的各种数据，返回字符串，列表返回第一个元素的字符串
        request_data = {
            'ne_int_no_parse': -1,
            'zero_no_parse': 0,
            'int_no_parse': 1,
            'float_no_parse': 1.1,
            'str_no_parse': '1',
            'true_no_parse': True,
            'false_no_parse': False,
            'int_list_no_parse': [1, 2],
            'str_list_no_parse': ['1', '2'],
            'float_list_no_parse': [1.1, 2.2],
            'bool_list_no_parse': [True, False]
        }
        data, headers, status_code = self.get(
            url_for('ret'),
            query_string=request_data
        )
        self.assertEqual(status_code, 200)
        self.assertEqual(data, {
            'ne_int_no_parse': '-1',
            'zero_no_parse': '0',
            'int_no_parse': '1',
            'float_no_parse': '1.1',
            'str_no_parse': '1',
            'true_no_parse': 'True',
            'false_no_parse': 'False',
            'int_list_no_parse': '1',
            'str_list_no_parse': '1',
            'float_list_no_parse': '1.1',
            'bool_list_no_parse': 'True'
        })

        # 提交有解析器的各种数据，原样返回
        request_data = {
            'ne_int': -1,
            'zero': 0,
            'int': 1,
            'float': 1.1,
            'str': '1',
            'true': True,
            'false': False,
            'int_list': [1, 2],
            'str_list': ['1', '2'],
            'float_list': [1.1, 2.2],
            'bool_list': [True, False]
        }
        data, headers, status_code = self.get(
            url_for('ret'),
            query_string=request_data
        )
        self.assertEqual(status_code, 200)
        self.assertEqual(data, request_data)

        # 向列表提交字符串
        data, headers, status_code = self.get(
            url_for('ret'),
            query_string={
                'int_list': '1'
            }
        )
        self.assertEqual(status_code, 200)
        self.assertEqual(data, {
            'int_list': [1]
        })

        # 测试列表的顺序
        request_data = {
            'int_list': [1, 2],
            'str_list': ['1', '2'],
            'float_list': [1.1, 2.2],
            'bool_list': [True, False]
        }
        data, headers, status_code = self.get(
            url_for('ret'),
            query_string=request_data
        )
        self.assertEqual(status_code, 200)
        self.assertEqual(data, request_data)
        # 倒序也没问题
        request_data = {
            'int_list': [2, 1],
            'str_list': ['2', '1'],
            'float_list': [2.2, 1.2],
            'bool_list': [False, True]
        }
        data, headers, status_code = self.get(
            url_for('ret'),
            query_string=request_data
        )
        self.assertEqual(status_code, 200)
        self.assertEqual(data, request_data)

        # 提交错误的数据
        request_data = {
            'int': 'abc'
        }
        data, headers, status_code = self.get(
            url_for('ret'),
            query_string=request_data
        )
        self.assertEqual(status_code, 400)
        self.assertEqual(data['code'], 3)

        # 提交错误的数据
        request_data = {
            'float': 'abc'
        }
        data, headers, status_code = self.get(
            url_for('ret'),
            query_string=request_data
        )
        self.assertEqual(status_code, 400)
        self.assertEqual(data['code'], 3)

        # 除了True/true/1，布尔值都是False
        data, headers, status_code = self.get(
            url_for('ret'),
            query_string={
                'true': 'True'
            }
        )
        self.assertEqual(status_code, 200)
        self.assertEqual(data, {'true': True})

        data, headers, status_code = self.get(
            url_for('ret'),
            query_string={
                'true': 'true'
            }
        )
        self.assertEqual(status_code, 200)
        self.assertEqual(data, {'true': True})

        data, headers, status_code = self.get(
            url_for('ret'),
            query_string={
                'true': '1'
            }
        )
        self.assertEqual(status_code, 200)
        self.assertEqual(data, {'true': True})

        data, headers, status_code = self.get(
            url_for('ret'),
            query_string={
                'true': 1
            }
        )
        self.assertEqual(status_code, 200)
        self.assertEqual(data, {'true': True})

        data, headers, status_code = self.get(
            url_for('ret'),
            query_string={
                'true': 0
            }
        )
        self.assertEqual(status_code, 200)
        self.assertEqual(data, {'true': False})

        data, headers, status_code = self.get(
            url_for('ret'),
            query_string={
                'true': '0'
            }
        )
        self.assertEqual(status_code, 200)
        self.assertEqual(data, {'true': False})

        data, headers, status_code = self.get(
            url_for('ret'),
            query_string={
                'true': -1
            }
        )
        self.assertEqual(status_code, 200)
        self.assertEqual(data, {'true': False})

        data, headers, status_code = self.get(
            url_for('ret'),
            query_string={
                'true': 'abc'
            }
        )
        self.assertEqual(status_code, 200)
        self.assertEqual(data, {'true': False})

        data, headers, status_code = self.get(
            url_for('ret'),
            query_string={
                'true': ['123']
            }
        )
        self.assertEqual(status_code, 200)
        self.assertEqual(data, {'true': False})
