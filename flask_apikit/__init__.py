from flask import _app_ctx_stack


class APIKit:
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """注册"""
        # request.args中“页数”的key，默认page
        app.config.setdefault('APIKIT_PAGINATION_PAGE_KEY', 'page')
        # request.args中“每页条目数”的key，默认limit
        app.config.setdefault('APIKIT_PAGINATION_LIMIT_KEY', 'limit')
        # 如果request.args中没有提供“每页条目数”，则默认使用的数量，默认10
        app.config.setdefault('APIKIT_PAGINATION_DEFAULT_LIMIT', 10)
        # “每页条目数”的最大值，设为0则为不限制
        app.config.setdefault('APIKIT_PAGINATION_MAX_LIMIT', 0)
        # 分页返回的响应头的key
        app.config.setdefault('APIKIT_PAGINATION_HEADER_PAGE_KEY', 'X-Pagination-Page')
        app.config.setdefault('APIKIT_PAGINATION_HEADER_LIMIT_KEY', 'X-Pagination-Limit')
        app.config.setdefault('APIKIT_PAGINATION_HEADER_COUNT_KEY', 'X-Pagination-Count')
        app.teardown_appcontext(self.teardown)

    @property
    def pagination(self):
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, 'apikit_pagination'):
                return ctx.apikit_pagination

    def teardown(self, exception):
        """暂时没有什么资源需要释放"""
        pass
