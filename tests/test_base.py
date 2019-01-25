from flask import url_for

from flask_apikit.exceptions import APIError
from flask_apikit.responses import Pagination, APIResponse
from flask_apikit.views import APIView
from tests import AppTestCase


class BaseTestCase(AppTestCase):
    def test_return_none(self):
        """测试返回空"""

        class Ret(APIView):
            def get(self):
                return

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(status_code, 204)
        self.assertEqual(data, '')

    def test_return_str(self):
        """测试返回字符串"""

        class Ret(APIView):
            def get(self):
                return 'hi'

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(data, 'hi')

    def test_return_str_with_status(self):
        """测试返回字符串+状态码"""

        class Ret(APIView):
            def get(self):
                return 'hi', 511

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(status_code, 511)
        self.assertEqual(data, 'hi')

    def test_return_str_with_headers(self):
        """测试返回字符串+响应头"""

        class Ret(APIView):
            def get(self):
                return 'hi', {'XXX': 'x'}

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(status_code, 200)
        self.assertEqual(data, 'hi')
        self.assertEqual(headers.get('XXX'), 'x')
        # 不会覆盖掉api_cors处理的头
        self.assertEqual(
            headers.get('Access-Control-Expose-Headers'),
            'X-PAGINATION-PAGE, X-PAGINATION-LIMIT, X-PAGINATION-COUNT, X-PAGINATION-PAGE-COUNT'
        )

    def test_return_str_with_headers2(self):
        """测试返回字符串+响应头（另一种响应头形式）"""

        class Ret(APIView):
            def get(self):
                return 'hi', [('XXX', 'x')]

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(status_code, 200)
        self.assertEqual(data, 'hi')
        self.assertEqual(headers.get('XXX'), 'x')
        # 不会覆盖掉api_cors处理的头
        self.assertEqual(
            headers.get('Access-Control-Expose-Headers'),
            'X-PAGINATION-PAGE, X-PAGINATION-LIMIT, X-PAGINATION-COUNT, X-PAGINATION-PAGE-COUNT'
        )

    def test_return_str_with_status_and_headers(self):
        """测试返回字符串+状态码+响应头"""

        class Ret(APIView):
            def get(self):
                return 'hi', 511, {'XXX': 'x'}

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(status_code, 511)
        self.assertEqual(data, 'hi')
        self.assertEqual(headers.get('XXX'), 'x')
        # 不会覆盖掉api_cors处理的头
        self.assertEqual(
            headers.get('Access-Control-Expose-Headers'),
            'X-PAGINATION-PAGE, X-PAGINATION-LIMIT, X-PAGINATION-COUNT, X-PAGINATION-PAGE-COUNT'
        )

    def test_return_str_with_status_and_headers2(self):
        """测试返回字符串+状态码+响应头（另一种响应头形式）"""

        class Ret(APIView):
            def get(self):
                return 'hi', 511, [('XXX', 'x')]

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(status_code, 511)
        self.assertEqual(data, 'hi')
        self.assertEqual(headers.get('XXX'), 'x')
        # 不会覆盖掉api_cors处理的头
        self.assertEqual(
            headers.get('Access-Control-Expose-Headers'),
            'X-PAGINATION-PAGE, X-PAGINATION-LIMIT, X-PAGINATION-COUNT, X-PAGINATION-PAGE-COUNT'
        )

    def test_return_list(self):
        """测试返回列表"""

        class Ret(APIView):
            def get(self):
                return [1, 2]

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(status_code, 200)
        self.assertEqual(data[0], 1)
        self.assertEqual(data[1], 2)

    def test_return_list_with_status(self):
        """测试返回列表+状态码"""

        class Ret(APIView):
            def get(self):
                return [1, 2], 511

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(status_code, 511)
        self.assertEqual(data[0], 1)
        self.assertEqual(data[1], 2)

    def test_return_list_with_headers(self):
        """测试返回列表+响应头"""

        class Ret(APIView):
            def get(self):
                return [1, 2], {'XXX': 'x'}

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(status_code, 200)
        self.assertEqual(headers.get('XXX'), 'x')
        # 不会覆盖掉api_cors处理的头
        self.assertEqual(
            headers.get('Access-Control-Expose-Headers'),
            'X-PAGINATION-PAGE, X-PAGINATION-LIMIT, X-PAGINATION-COUNT, X-PAGINATION-PAGE-COUNT'
        )
        self.assertEqual(data[0], 1)
        self.assertEqual(data[1], 2)

    def test_return_list_with_headers2(self):
        """测试返回列表+响应头（另一种响应头形式）"""

        class Ret(APIView):
            def get(self):
                return [1, 2], [('XXX', 'x')]

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(status_code, 200)
        self.assertEqual(headers.get('XXX'), 'x')
        # 不会覆盖掉api_cors处理的头
        self.assertEqual(
            headers.get('Access-Control-Expose-Headers'),
            'X-PAGINATION-PAGE, X-PAGINATION-LIMIT, X-PAGINATION-COUNT, X-PAGINATION-PAGE-COUNT'
        )
        self.assertEqual(data[0], 1)
        self.assertEqual(data[1], 2)

    def test_return_list_with_status_and_headers(self):
        """测试返回列表+状态码+响应头"""

        class Ret(APIView):
            def get(self):
                return [1, 2], 511, {'XXX': 'x'}

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(status_code, 511)
        self.assertEqual(headers.get('XXX'), 'x')
        # 不会覆盖掉api_cors处理的头
        self.assertEqual(
            headers.get('Access-Control-Expose-Headers'),
            'X-PAGINATION-PAGE, X-PAGINATION-LIMIT, X-PAGINATION-COUNT, X-PAGINATION-PAGE-COUNT'
        )
        self.assertEqual(data[0], 1)
        self.assertEqual(data[1], 2)

    def test_return_list_with_status_and_headers2(self):
        """测试返回列表+状态码+响应头（另一种响应头形式）"""

        class Ret(APIView):
            def get(self):
                return [1, 2], 511, [('XXX', 'x')]

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(status_code, 511)
        self.assertEqual(headers.get('XXX'), 'x')
        # 不会覆盖掉api_cors处理的头
        self.assertEqual(
            headers.get('Access-Control-Expose-Headers'),
            'X-PAGINATION-PAGE, X-PAGINATION-LIMIT, X-PAGINATION-COUNT, X-PAGINATION-PAGE-COUNT'
        )
        self.assertEqual(data[0], 1)
        self.assertEqual(data[1], 2)

    def test_return_dict(self):
        """测试返回字典"""

        class Ret(APIView):
            def get(self):
                return {'hi': 123}

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(status_code, 200)
        self.assertEqual(data['hi'], 123)

    def test_return_dict_with_status(self):
        """测试返回字典+状态码"""

        class Ret(APIView):
            def get(self):
                return {'hi': 123}, 511

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(status_code, 511)
        self.assertEqual(data['hi'], 123)

    def test_return_dict_with_headers(self):
        """测试返回字典+响应头"""

        class Ret(APIView):
            def get(self):
                return {'hi': 123}, {'XXX': 'x'}

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(status_code, 200)
        self.assertEqual(headers.get('XXX'), 'x')
        # 不会覆盖掉api_cors处理的头
        self.assertEqual(
            headers.get('Access-Control-Expose-Headers'),
            'X-PAGINATION-PAGE, X-PAGINATION-LIMIT, X-PAGINATION-COUNT, X-PAGINATION-PAGE-COUNT'
        )
        self.assertEqual(data['hi'], 123)

    def test_return_dict_with_headers2(self):
        """测试返回字典+响应头（另一种响应头形式）"""

        class Ret(APIView):
            def get(self):
                return {'hi': 123}, [('XXX', 'x')]

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(status_code, 200)
        self.assertEqual(headers.get('XXX'), 'x')
        # 不会覆盖掉api_cors处理的头
        self.assertEqual(
            headers.get('Access-Control-Expose-Headers'),
            'X-PAGINATION-PAGE, X-PAGINATION-LIMIT, X-PAGINATION-COUNT, X-PAGINATION-PAGE-COUNT'
        )
        self.assertEqual(data['hi'], 123)

    def test_return_dict_with_status_and_headers(self):
        """测试返回字典+状态码+响应头"""

        class Ret(APIView):
            def get(self):
                return {'hi': 123}, 511, {'XXX': 'x'}

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(status_code, 511)
        self.assertEqual(headers.get('XXX'), 'x')
        # 不会覆盖掉api_cors处理的头
        self.assertEqual(
            headers.get('Access-Control-Expose-Headers'),
            'X-PAGINATION-PAGE, X-PAGINATION-LIMIT, X-PAGINATION-COUNT, X-PAGINATION-PAGE-COUNT'
        )
        self.assertEqual(data['hi'], 123)

    def test_return_dict_with_status_and_headers2(self):
        """测试返回字典+状态码+响应头（另一种响应头形式）"""

        class Ret(APIView):
            def get(self):
                return {'hi': 123}, 511, [('XXX', 'x')]

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(status_code, 511)
        self.assertEqual(headers.get('XXX'), 'x')
        # 不会覆盖掉api_cors处理的头
        self.assertEqual(
            headers.get('Access-Control-Expose-Headers'),
            'X-PAGINATION-PAGE, X-PAGINATION-LIMIT, X-PAGINATION-COUNT, X-PAGINATION-PAGE-COUNT'
        )
        self.assertEqual(data['hi'], 123)

    def test_return_base_error(self):
        """测试返回基本错误"""

        class Ret(APIView):
            def get(self):
                raise APIError

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(status_code, 400)
        self.assertEqual(data['code'], 1)
        self.assertEqual(data['message'], APIError.message)

    def test_return_error(self):
        """测试返回错误"""

        class Err(APIError):
            code = 1000
            message = 'hi'

        class Ret(APIView):
            def get(self):
                raise Err

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(status_code, 400)
        self.assertEqual(data['code'], Err.code)
        self.assertEqual(data['message'], Err.message)

    def test_return_error_with_status(self):
        """测试返回错误+状态码"""

        class Err(APIError):
            status_code = 511
            code = 1000
            message = 'hi'

        class Ret(APIView):
            def get(self):
                raise Err

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(status_code, Err.status_code)
        self.assertEqual(data['code'], Err.code)
        self.assertEqual(data['message'], Err.message)

    def test_return_error_with_headers(self):
        """测试返回错误+响应头"""

        class Err(APIError):
            code = 1000
            message = 'hi'
            headers = {'XXX': 'x'}

        class Ret(APIView):
            def get(self):
                raise Err

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(status_code, 400)
        self.assertEqual(data['code'], Err.code)
        self.assertEqual(data['message'], Err.message)
        self.assertEqual(headers.get('XXX'), 'x')
        # 不会覆盖掉api_cors处理的头
        self.assertEqual(
            headers.get('Access-Control-Expose-Headers'),
            'X-PAGINATION-PAGE, X-PAGINATION-LIMIT, X-PAGINATION-COUNT, X-PAGINATION-PAGE-COUNT'
        )

    def test_return_error_with_headers2(self):
        """测试返回错误+响应头（另一种响应头形式）"""

        class Err(APIError):
            code = 1000
            message = 'hi'
            headers = [('XXX', 'x')]

        class Ret(APIView):
            def get(self):
                raise Err

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(status_code, 400)
        self.assertEqual(data['code'], Err.code)
        self.assertEqual(data['message'], Err.message)
        self.assertEqual(headers.get('XXX'), 'x')
        # 不会覆盖掉api_cors处理的头
        self.assertEqual(
            headers.get('Access-Control-Expose-Headers'),
            'X-PAGINATION-PAGE, X-PAGINATION-LIMIT, X-PAGINATION-COUNT, X-PAGINATION-PAGE-COUNT'
        )

    def test_return_error_with_status_and_headers(self):
        """测试返回错误+状态码+响应头"""

        class Err(APIError):
            status_code = 511
            code = 1000
            message = 'hi'
            headers = {'XXX': 'x'}

        class Ret(APIView):
            def get(self):
                raise Err

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(status_code, 511)
        self.assertEqual(data['code'], Err.code)
        self.assertEqual(data['message'], Err.message)
        self.assertEqual(headers.get('XXX'), 'x')
        # 不会覆盖掉api_cors处理的头
        self.assertEqual(
            headers.get('Access-Control-Expose-Headers'),
            'X-PAGINATION-PAGE, X-PAGINATION-LIMIT, X-PAGINATION-COUNT, X-PAGINATION-PAGE-COUNT'
        )

    def test_return_api_response(self):
        """测试返回APIResponse"""

        res = APIResponse(data={'hi': 123})

        class Ret(APIView):
            def get(self):
                return res

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(status_code, 200)
        self.assertEqual(data, {'hi': 123})

    def test_return_api_response_with_status(self):
        """测试返回APIResponse+状态码"""

        res = APIResponse(data={'hi': 123}, status_code=511)

        class Ret(APIView):
            def get(self):
                return res

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(status_code, 511)
        self.assertEqual(data, {'hi': 123})

    def test_return_api_response_with_headers(self):
        """测试返回APIResponse+响应头"""

        res = APIResponse(data={'hi': 123}, headers={'XXX': 'x'})

        class Ret(APIView):
            def get(self):
                return res

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(status_code, 200)
        self.assertEqual(data, {'hi': 123})
        self.assertEqual(headers.get('XXX'), 'x')
        # 不会覆盖掉api_cors处理的头
        self.assertEqual(
            headers.get('Access-Control-Expose-Headers'),
            'X-PAGINATION-PAGE, X-PAGINATION-LIMIT, X-PAGINATION-COUNT, X-PAGINATION-PAGE-COUNT'
        )

    def test_return_api_response_with_headers2(self):
        """测试返回APIResponse+响应头（另一种响应头形式）"""

        res = APIResponse(data={'hi': 123}, headers=[('XXX', 'x')])

        class Ret(APIView):
            def get(self):
                return res

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(status_code, 200)
        self.assertEqual(data, {'hi': 123})
        self.assertEqual(headers.get('XXX'), 'x')
        # 不会覆盖掉api_cors处理的头
        self.assertEqual(
            headers.get('Access-Control-Expose-Headers'),
            'X-PAGINATION-PAGE, X-PAGINATION-LIMIT, X-PAGINATION-COUNT, X-PAGINATION-PAGE-COUNT'
        )

    def test_return_api_response_with_status_and_headers(self):
        """测试返回APIResponse+状态码+响应头"""

        res = APIResponse(data={'hi': 123}, status_code=511, headers={'XXX': 'x'})

        class Ret(APIView):
            def get(self):
                return res

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(status_code, 511)
        self.assertEqual(data, {'hi': 123})
        self.assertEqual(headers.get('XXX'), 'x')
        # 不会覆盖掉api_cors处理的头
        self.assertEqual(
            headers.get('Access-Control-Expose-Headers'),
            'X-PAGINATION-PAGE, X-PAGINATION-LIMIT, X-PAGINATION-COUNT, X-PAGINATION-PAGE-COUNT'
        )

    def test_return_api_response_with_status_and_headers2(self):
        """测试返回APIResponse+状态码+响应头（另一种响应头形式）"""

        res = APIResponse(data={'hi': 123}, status_code=511, headers=[('XXX', 'x')])

        class Ret(APIView):
            def get(self):
                return res

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(status_code, 511)
        self.assertEqual(data, {'hi': 123})
        self.assertEqual(headers.get('XXX'), 'x')
        # 不会覆盖掉api_cors处理的头
        self.assertEqual(
            headers.get('Access-Control-Expose-Headers'),
            'X-PAGINATION-PAGE, X-PAGINATION-LIMIT, X-PAGINATION-COUNT, X-PAGINATION-PAGE-COUNT'
        )
