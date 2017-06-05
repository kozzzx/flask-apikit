from flask import request
from flask.views import MethodView
from marshmallow import Schema

from flask_apikit.decorators import api_view
from flask_apikit.exceptions import ValidateError


class ApiView(MethodView):
    decorators = (api_view,)

    def verify_data(self, data, schema, context=None):
        """
        使用schema实例验证数据，有错误时抛出ValidateError

        :param dict data: 需要验证的数据
        :param Schema schema: schema实例
        :param dict context: 传递给schema使用的额外数据，保存在schema的context属性中
        :return:
        """
        # 传递给schema使用的额外数据
        if context:
            schema.context = context
        data, errors = schema.load(data)
        # 有错误则抛出
        if errors:
            raise ValidateError(errors)
        return data

    def get_json(self, schema=None, context=None, *args, **kwargs):
        """
        从request获取json数据,没有则返回空字典
        可以使用一个验证器进行数据验证

        :param Schema schema: schema实例
        :param dict context: 传递给schema使用的额外数据，保存在schema的context属性中
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
            data = self.verify_data(json_data, schema, context)
        # 没有验证器,直接返回
        else:
            data = json_data
        return data
