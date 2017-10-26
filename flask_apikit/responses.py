def pagination(data, status_code=200, other_headers=None, **kwargs):
    header_prefix = 'X-Pagination-'
    headers = {'{}{}'.format(header_prefix, k.capitalize()): v for k, v in kwargs.items()}
    if other_headers:
        for k, v in other_headers.items():
            headers[k] = v
    return data, status_code, headers


# class APIResponse:
#     header_prefix = ''
#
#     def __init__(self, data, status_code=200, other_headers=None, **kwargs):
#         self.data = data
#         self.status_code = status_code
#         self.headers = {'{}{}'.format(self.header_prefix, k.capitalize()): v for k, v in kwargs.items()}
#         if other_headers:
#             for k, v in other_headers.items():
#                 self.headers[k] = v
#
#     def dump(self):
#         return self.data, self.status_code, self.headers
#
#
# class Pagination(APIResponse):
#     header_prefix = 'X-Pagination-'
