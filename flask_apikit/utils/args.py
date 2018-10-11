def boolean(data):
    # 处理url中传来的bool类型参数
    if (
            data == '' or
            data.lower() == 'false' or
            data == '0' or
            data is None
    ):
        return False
    else:
        return True
