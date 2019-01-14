class APIError(Exception):
    """
    所有API抛出的错误需继承自此错误,才能被捕捉,并返回给前端
    """
    status_code = 400
    code = 1
    message = 'Undefined Error'

    def __init__(self, message=None, replace=False):
        """
        :param message: 附加message
        :param replace: 是否替换原message，为False则为'原message: 附加message'
        """
        # 如果定义了附加message，则加在原message后面
        if message:
            if replace:
                self.message = message
            else:
                self.message = f'{self.message}: {message}'


class ValidateError(APIError):
    """
    @apiDefine ValidateError
    @apiError 2 字段验证错误
    参数错误,具体错误信息将包含在message中
    @apiErrorExample {json} ValidateError示例
    {
        "error": "ValidateError",
        "code": 2,
        "message": {
            "email": [
                "此郵箱已存在,您可以直接登錄或嘗試其他郵箱"
            ],
            "name": [
                "此昵称已存在,请尝试其他昵称"
            ]
        }
    }
    """
    code = 2


class QueryParseError(APIError):
    """
    @apiDefine QueryParseError
    @apiError 3 Query解析错误
    """
    code = 3
