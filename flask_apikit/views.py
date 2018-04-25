from flask import request
from flask.views import MethodView
from marshmallow import Schema
from marshmallow.exceptions import ValidationError

from flask_apikit.decorators import api_view
from flask_apikit.exceptions import ValidateError


class APIView(MethodView):
    decorators = (api_view,)

    def verify_data(self,
                    data: dict,
                    schema: Schema,
                    context: dict = None) -> dict:
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
        try:
            data = schema.load(data)
        except ValidationError as e:
            raise ValidateError(e.messages)
        return data

    def get_json(self,
                 schema: Schema = None,
                 context: dict = None,
                 additional_data: dict = None,
                 *args, **kwargs) -> dict:
        """
        从request获取json数据,没有则返回空字典
        可以使用一个验证器进行数据验证

        :param Schema schema: schema实例
        :param dict context: 传递给schema使用的额外数据，保存在schema的context属性中
        :param dict additional_data: 用于从url/args中获取的数据,将覆盖get_json获得的数据
        如果schema使用load_from,会优先使用字段名读取
        user_name = fields.Str(load_from='userName')
        优先级 'user_name'>'userName',也就是说如果get_json中使用的是'user_name',additional_data中是'userName',additional_data的数据将不生效
        为安全性,如果要覆盖传入的数据(以此来同时验证additional_data传入的数据),请勿使用load_from中的名字,直接使用字段名即可
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
        # 将附加的数据附加到json_data
        if additional_data:
            json_data = {**json_data, **additional_data}
        # 给了验证器,则进行验证
        if isinstance(schema, Schema):
            data = self.verify_data(json_data, schema, context)
        # 没有验证器,直接返回
        else:
            data = json_data
        return data
