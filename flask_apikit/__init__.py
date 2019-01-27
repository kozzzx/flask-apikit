class APIKit:
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """注册"""
        # === 分页设置 ===
        # 分页数量设置
        app.config.setdefault('APIKIT_PAGINATION_DEFAULT_LIMIT', 10)  # 如果没有提供“每页条目数”，则默认使用的数量，默认10
        app.config.setdefault('APIKIT_PAGINATION_MAX_LIMIT', 100)  # “每页条目数”的最大值，设为0则为不限制
        # 分页请求参数名
        app.config.setdefault('APIKIT_PAGINATION_PAGE_KEY', 'page')  # request.args中“页数”的key，默认page
        app.config.setdefault('APIKIT_PAGINATION_LIMIT_KEY', 'limit')  # request.args中“每页条目数”的key，默认limit
        # 分页返回头参数名
        app.config.setdefault('APIKIT_PAGINATION_HEADER_PAGE_KEY', 'X-Pagination-Page')  # 当前页码
        app.config.setdefault('APIKIT_PAGINATION_HEADER_LIMIT_KEY', 'X-Pagination-Limit')  # 每页个数
        app.config.setdefault('APIKIT_PAGINATION_HEADER_COUNT_KEY', 'X-Pagination-Count')  # 元素总个数
        app.config.setdefault('APIKIT_PAGINATION_HEADER_PAGE_COUNT_KEY', 'X-Pagination-Page-Count')  # 总页数
        # === CORS配置 ===
        app.config.setdefault('APIKIT_ACCESS_CONTROL_MAX_AGE', 600)
        app.config.setdefault('APIKIT_ACCESS_CONTROL_ALLOW_ORIGIN', '*')
        app.config.setdefault('APIKIT_ACCESS_CONTROL_ALLOW_HEADERS', ['Authorization', 'Content-Type'])
        app.config.setdefault('APIKIT_ACCESS_CONTROL_ALLOW_CREDENTIALS', False)
        app.config.setdefault('APIKIT_ACCESS_CONTROL_EXPOSE_HEADERS', [])
        app.teardown_appcontext(self.teardown)

    def teardown(self, exception):
        """暂时没有什么资源需要释放"""
        pass
