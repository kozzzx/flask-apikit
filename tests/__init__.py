import json
from unittest import TestCase

from flask import Flask
from flask_apikit import APIKit


class AppTestCase(TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['SERVER_NAME'] = 'test'
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client(use_cookies=True)
        # 初始化Flask-APIKit插件
        self.apikit = APIKit()
        self.apikit.init_app(self.app)

    def open(self, *args, **kwargs):
        # 查看是否指定client
        client = kwargs.pop('client', None)
        if client is None:
            client = self.client
        # 增加headers
        if kwargs.get('headers') is None:
            kwargs['headers'] = {
                # 默认增加跨域参数
                'Origin': 'https://example.com'
            }
        # 如果给予data参数,则转换为json
        data = kwargs.pop('json', None)
        if data:
            kwargs['data'] = json.dumps(data)
            kwargs['headers']['Content-Type'] = 'application/json'
        resp = client.open(*args, **kwargs)
        headers = resp.headers
        status_code = resp._status_code
        result = resp.get_data(as_text=True)
        try:
            data = json.loads(result)
        except json.JSONDecodeError:
            data = result
        return data, headers, status_code

    def get(self, *args, **kw):
        kw['method'] = 'GET'
        return self.open(*args, **kw)

    def patch(self, *args, **kw):
        kw['method'] = 'PATCH'
        return self.open(*args, **kw)

    def post(self, *args, **kw):
        kw['method'] = 'POST'
        return self.open(*args, **kw)

    def head(self, *args, **kw):
        kw['method'] = 'HEAD'
        return self.open(*args, **kw)

    def put(self, *args, **kw):
        kw['method'] = 'PUT'
        return self.open(*args, **kw)

    def delete(self, *args, **kw):
        kw['method'] = 'DELETE'
        return self.open(*args, **kw)

    def options(self, *args, **kw):
        kw['method'] = 'OPTIONS'
        return self.open(*args, **kw)

    def trace(self, *args, **kw):
        kw['method'] = 'TRACE'
        return self.open(*args, **kw)
