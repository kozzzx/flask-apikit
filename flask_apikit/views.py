from flask import request
from flask.views import MethodView
from marshmallow import Schema

from flask_apikit.decorators import api_view
from flask_apikit.exceptions import ValidateError


class ApiView(MethodView):
    decorators = (api_view,)

    def get_json(self, schema=None, *args, **kwargs):
        """
        从request获取json数据,没有则返回空字典
        可以使用一个验证器进行数据验证

        :param Schema schema: 验证器
        :param args:
        :param kwargs:
        :rtype: dict
        :return:
        """
        # 从request获取json
        json_data = request.get_json(*args, **kwargs)
        # json_data为None,转为空字典
        if json_data is None:
            json_data = {}
        # 给了验证器,则进行验证
        if isinstance(schema, Schema):
            data, errors = schema.load(json_data)
            # 有错误则抛出
            if errors:
                raise ValidateError(errors)
        # 没有验证器,直接返回
        else:
            data = json_data
        return data
