from flask_apikit.exceptions import QueryParseError


class QueryParser:
    @classmethod
    def int(cls, data: str) -> int:
        try:
            return int(data)
        except:
            raise QueryParseError(f'value "{data}" can not parse to int')

    @classmethod
    def float(cls, data: str) -> int:
        try:
            return float(data)
        except:
            raise QueryParseError(f'value "{data}" can not parse to float')

    @classmethod
    def bool(cls, data: str) -> bool:
        # 处理query中的bool类型参数
        if (
                data.lower() == 'true' or
                data == '1'
        ):
            return True
        else:
            return False
