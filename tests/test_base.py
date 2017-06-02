from flask import url_for

from flask_apikit.exceptions import ApiError
from flask_apikit.views import ApiView
from tests import AppTestCase


class BaseTestCase(AppTestCase):
    def test_return_dict(self):
        """测试返回字典"""

        class Ret(ApiView):
            def get(self):
                return {'hi': 123}

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(status_code, 200)
        self.assertEqual(data['e'], 0)
        self.assertEqual(data['hi'], 123)

    def test_return_str(self):
        """测试返回字符串"""

        class Ret(ApiView):
            def get(self):
                return 'hi'

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(status_code, 200)
        self.assertEqual(data, 'hi')

    def test_return_dict_with_status(self):
        """测试返回字典+状态码"""

        class Ret(ApiView):
            def get(self):
                return {'hi': 123}, 511

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(status_code, 511)
        self.assertEqual(data['e'], 0)
        self.assertEqual(data['hi'], 123)

    def test_return_str_with_status(self):
        """测试返回字符串+状态码"""

        class Ret(ApiView):
            def get(self):
                return 'hi', 511

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(status_code, 511)
        self.assertEqual(data, 'hi')

    def test_return_base_error(self):
        """测试返回基本错误"""

        class Ret(ApiView):
            def get(self):
                raise ApiError

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(status_code, 200)
        self.assertEqual(data['e'], 1)
        self.assertEqual(data['msg'], ApiError.message)

    def test_return_error(self):
        """测试返回错误"""

        class Err(ApiError):
            error_code = 1000
            message = 'hi'

        class Ret(ApiView):
            def get(self):
                raise Err

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(status_code, 200)
        self.assertEqual(data['e'], Err.error_code)
        self.assertEqual(data['msg'], Err.message)

    def test_return_error_with_status(self):
        """测试返回错误+状态码"""

        class Err(ApiError):
            status_code = 511
            error_code = 1000
            message = 'hi'

        class Ret(ApiView):
            def get(self):
                raise Err

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(status_code, Err.status_code)
        self.assertEqual(data['e'], Err.error_code)
        self.assertEqual(data['msg'], Err.message)
