class ApiError(Exception):
    """
    @apiDefine ApiError
    @apiError (可能的错误) {1} ApiError 未定义的错误
    """
    code = 1
    message = 'Undefined Error'


class ValidateError(ApiError):
    """
    @apiDefine ValidateError
    @apiError (可能的错误) {2} ValidateError 
    参数错误,具体错误信息将包含在msg中
    @apiErrorExample {json} ValidateError示例
    {
        "e": 2,
        "msg": {
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

    def __init__(self, message):
        self.message = message
