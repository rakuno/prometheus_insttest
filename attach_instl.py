from prometheus_client import make_wsgi_app
from wsgiref.simple_server import make_server

metrics_app = make_wsgi_app()


def attach_app(environ, start_fn):
    if environ['PATH_INFO'] == '/metrics':
        return metrics_app(environ, start_fn)
    start_fn('200 OK', [])
    return [b'Hello Prometheus']


if __name__ == '__main__':
    httpd = make_server('', 8000, attach_app)
    httpd.serve_forever()
