from flask import url_for

from flask_apikit.exceptions import ApiError
from flask_apikit.views import ApiView
from tests import AppTestCase


class BaseTestCase(AppTestCase):
    def test_return_none(self):
        """测试返回空"""

        class Ret(ApiView):
            def get(self):
                return

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(status_code, 204)
        self.assertEqual(data, '')

    def test_return_dict(self):
        """测试返回字典"""

        class Ret(ApiView):
            def get(self):
                return {'hi': 123}

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(status_code, 200)
        self.assertEqual(data['hi'], 123)

    def test_return_list(self):
        """测试返回列表"""

        class Ret(ApiView):
            def get(self):
                return [1, 2]

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(status_code, 200)
        self.assertEqual(data[0], 1)
        self.assertEqual(data[1], 2)

    def test_return_dict_with_status(self):
        """测试返回列表+状态码"""

        class Ret(ApiView):
            def get(self):
                return [1, 2], 511

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(status_code, 511)
        self.assertEqual(data[0], 1)
        self.assertEqual(data[1], 2)

    def test_return_str(self):
        """测试返回字符串"""

        class Ret(ApiView):
            def get(self):
                return 'hi'

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(data, 'hi')

    def test_return_dict_with_status(self):
        """测试返回字典+状态码"""

        class Ret(ApiView):
            def get(self):
                return {'hi': 123}, 511

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(status_code, 511)
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
        self.assertEqual(status_code, 400)
        self.assertEqual(data['code'], 1)
        self.assertEqual(data['message'], ApiError.message)

    def test_return_error(self):
        """测试返回错误"""

        class Err(ApiError):
            code = 1000
            message = 'hi'

        class Ret(ApiView):
            def get(self):
                raise Err

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(status_code, 400)
        self.assertEqual(data['code'], Err.code)
        self.assertEqual(data['message'], Err.message)

    def test_return_error_with_status(self):
        """测试返回错误+状态码"""

        class Err(ApiError):
            status_code = 511
            code = 1000
            message = 'hi'

        class Ret(ApiView):
            def get(self):
                raise Err

        self.app.add_url_rule('/', methods=['GET'], view_func=Ret.as_view('ret'))
        data, headers, status_code = self.get(url_for('ret'))
        self.assertEqual(status_code, Err.status_code)
        self.assertEqual(data['code'], Err.code)
        self.assertEqual(data['message'], Err.message)
