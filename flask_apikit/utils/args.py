def split_comma_str(value, parse_int=True):
    def to_int(v):
        try:
            v = int(v)
        except ValueError:
            pass
        finally:
            return v

    if not value:
        return None
    value_list = value.split(',')
    if parse_int:
        value_list = list(map(to_int, value_list))
    return value_list
