# Flask-APIKit

>插件开发中，变动剧烈，请勿用于生产

使用Flask更快的构建Restful API.

## 安装

    pip install flask-apikit

## 使用

```python
from flask import Flask, Blueprint
from flask_apikit import APIKit
from flask_apikit.views import APIView
from flask_apikit.exceptions import APIError
from flask_apikit.utils.query import QueryParser

app = Flask(__name__)
apikit = APIKit(app)

# 基础使用
class BaseAPI(APIView):
    def get(self):
        return {'hello': 'apikit'}, {'X-Custom-Header': 'APIKIT'}

    def post(self):
        return [1, 2, 'go'], 201

    def put(self):
        return [1, 2, 'go'], 201, {'X-Custom-Header': 'APIKIT'}

# 注册蓝本
blueprint = Blueprint('index', __name__)
blueprint.add_url_rule('/', methods=['GET', 'OPTIONS'], view_func=BaseAPI.as_view('index'))
app.register_blueprint(blueprint)

if __name__ == '__main__':
    app.run(debug=True)
```

请求将会返回如下：

```http
>>>
GET / HTTP/1.1
<<<
HTTP/1.1 200 OK
...
Content-Type: application/json
X-Custom-Header: APIKit

{"hello": "apikit"}
```

```http
>>>
POST / HTTP/1.1
<<<
HTTP/1.1 201 Created
...
Content-Type: application/json

[1, 2, "go"]
```

```http
>>>
PUT / HTTP/1.1
<<<
HTTP/1.1 201 Created
...
Content-Type: application/json
X-Custom-Header: APIKit

[1, 2, "go"]
```

### 从请求中获取数据

```python
class GetDataAPI(APIView):
    def get(self):
        # 从请求Query String中获取数据
        data = self.get_query({
            number: QueryParser.int,
            names: [],
            numbers: [QueryParser.int]
        })
        return data

    def post(self):
        # 从请求Payload中获取json数据
        data = self.get_json()
        return data
```

请求将会返回如下：

```http
>>>
GET /?name=bill&names=bob&names=tom&number=1&numbers=10&numbers=20 HTTP/1.1
<<<
HTTP/1.1 200 OK
...
Content-Type: application/json

{
    "name": "bill",
    "names": ["bob", "tom"],
    "number": 1,
    "numbers": [10, 20]
}
```

```http
>>>
POST / HTTP/1.1

{
    "name": "bill",
    "names": ["bob", "tom"],
    "number": 1,
    "numbers": [10, 20]
}
<<<
HTTP/1.1 200 OK
...
Content-Type: application/json

{
    "name": "bill",
    "names": ["bob", "tom"],
    "number": 1,
    "numbers": [10, 20]
}
```

### 分页

```python
from flask_apikit.responses import Pagination

class PageAPI(APIView):
    def get(self):
        p = Pagination()
        # 某种查询语句
        data = query_db('XXX').skip(p.skip).limit(p.limit)
        count = query_db('XXX').count()
        # 返回数据
        return p.set_data(data, count)
```

请求将会返回如下：

```http
>>>
GET /?page=3&limit=3 HTTP/1.1
<<<
HTTP/1.1 200 OK
...
Content-Type: application/json
X-Pagination-Count: 20
X-Pagination-Limit: 3
X-Pagination-Page: 3
X-Pagination-Page-Count: 7

[1, 2, 3]
```
### 抛出错误给前端

```python
class MyError(APIError):
    status_code = 403
    code = 100  # 1-99为APIKit所用的code
    message = 'Need Login'
    headers = {'X-Custom-Header': 'APIKIT'}

class ErrorAPI(APIView):
    def get(self):
        raise MyError
```

请求将会返回如下：

```http
>>>
GET / HTTP/1.1
<<<
HTTP/1.1 403 Forbidden
...
Content-Type: application/json
X-Custom-Header: APIKit

{
    "error": "MyError",
    "code": 100,
    "message": "Need Login"
}
```
