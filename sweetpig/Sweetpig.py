import time


def default(environ, start_response):
    print('#' * 100)
    print(environ)
    print('#' * 100)
    status = '404 Not Found'
    response_headers = [('Content-Type', 'text/html')]
    start_response(status, response_headers)
    return [('404 Not Found--->%s\n' % time.ctime()).encode('utf-8')]


class SweetPig:
    def __init__(self, import_name):
        self.import_name = import_name

        self.uri_map = {
            'default': default
        }

    def __call__(self, *args, **kwargs):
        environ, start_response = args
        url = environ['PATH_INFO']
        app = self.uri_map.get(url, self.uri_map['default'])
        return app(environ, start_response)

    def route(self, path):
        print('path', path)

        def wrapper(func):
            def _wrap(environ, start_response, *args, **kwargs):
                res = func(*args, **kwargs)
                start_response('200 OK', [('Content-Type', 'text/html')])
                return [res.encode('utf-8')]

            self.uri_map.update({
                path: _wrap,
            })
            return _wrap

        return wrapper