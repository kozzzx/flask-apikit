from flask import request, current_app, _app_ctx_stack
from flask.views import MethodView
from marshmallow import Schema
from marshmallow.exceptions import ValidationError

from flask_apikit.decorators import api_cors, api_response
from flask_apikit.exceptions import ValidateError


class APIView(MethodView):
    decorators = [api_response, api_cors]
    # 关闭View中Flask对OPTIONS请求的默认处理
    # （以防add_url_rule时methods忘记加'OPTIONS'，OPTIONS请求被Flask的dispatch_request处理）
    provide_automatic_options = False

    def verify_data(self, data: dict, schema: Schema,
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
            # 合并多个验证器对于同一字段的相同错误
            for key in e.messages.keys():
                e.messages[key] = list(set(e.messages[key]))
            raise ValidateError(e.messages, replace=True)
        return data

    def get_json(self,
                 schema: Schema = None,
                 context: dict = None,
                 additional_data: dict = None,
                 *args,
                 **kwargs) -> dict:
        """
        从request获取json数据，没有则返回空字典
        可以使用一个验证器进行数据验证

        :param Schema schema: schema实例，使用marshmallow进行数据验证
        :param dict context: 传递给schema使用的额外数据，保存在schema的context属性中
        :param dict additional_data: 用于从url/args中获取的数据,将覆盖get_json获得的数据
            如果schema使用了load_from别名，请使用字段名作为key
            如：
            user_name = fields.Str(load_from='userName')
            marshmallow可以同时支持key为'user_name'或'userName'的传入数据
            但如果两者都有，此时优先级 'user_name'>'userName'，其会优先读取字典中'user_name'进行验证，而抛弃'userName'的值
            所以如果目的是覆盖request.get_json()获取的数据，为安全性，应该使用字段名作为key，而不是load_from别名
        :param args: 传给request.get_json(*args, **kwargs)
        :param kwargs: 传给request.get_json(*args, **kwargs)
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

    def get_query(self,
                  parsers: dict = None,
                  schema: Schema = None,
                  context: dict = None,
                  additional_data: dict = None) -> dict:
        """
        从request.args中获取query数据，没有则返回空字典
        默认将作为字符串返回，可以使用parsers参数定义每个键值对的解析规则
        可以使用一个验证器进行数据验证

        :param parsers: 用于定义转换数据的解析器
            {
                'names': [],  # 解析成字符串列表
                'age': QueryParser.int,  # 解析成整型
                'ages': [QueryParser.int]  # 解析成整型列表
            }
        :param Schema schema: schema实例，使用marshmallow进行数据验证
        :param dict context: 传递给schema使用的额外数据，保存在schema的context属性中
        :param dict additional_data: 用于从url/args中获取的数据,将覆盖get_json获得的数据
            如果schema使用了load_from别名，请使用字段名作为key
            如：
            user_name = fields.Str(load_from='userName')
            marshmallow可以同时支持key为'user_name'或'userName'的传入数据
            但如果两者都有，此时优先级 'user_name'>'userName'，其会优先读取字典中'user_name'进行验证，而抛弃'userName'的值
            所以如果目的是覆盖request.get_json()获取的数据，为安全性，应该使用字段名作为key，而不是load_from别名
        :rtype: dict
        :return:
        """
        # 从request获取args
        query_data = request.args.to_dict(flat=False)
        for key in query_data:
            # 如果提供了解析器，则通过其转换数据
            if parsers and key in parsers:
                parser = parsers[key]
                # 如果解析器是个列表，表示将数据当做列表处理并返回
                if isinstance(parser, list):
                    # 如果解析器是个列表，使用parser[0]进行处理
                    if len(parser) > 0:
                        query_data[key] = [
                            parser[0](data) for data in query_data[key]
                        ]
                # 直接使用parser进行处理
                else:
                    query_data[key] = parser(query_data[key][0])
            # 没有提供处理器，将值设为列表中第一个字符串
            else:
                query_data[key] = query_data[key][0]
        # 将附加的数据附加到query_data
        if additional_data:
            query_data = {**query_data, **additional_data}
        # 给了验证器,则进行验证
        if isinstance(schema, Schema):
            data = self.verify_data(query_data, schema, context)
        # 没有验证器,直接返回
        else:
            data = query_data
        return data
