from prometheus_client import make_wsgi_app
from prometheus_client import Gauge
from wsgiref.simple_server import make_server

metrics_app = make_wsgi_app()

ATTACH_STATUS = Gauge('attach_status', 'Secure Mobile Connect Attach status')
attach_status = 0


class AttachMonitor:
    def __init__(self):
        self.attach_status = 0

    def attach_app(self, environ, start_fn):
        if environ['PATH_INFO'] == '/metrics':
            self.attach_status = not self.attach_status
            ATTACH_STATUS.set(self.attach_status)
            return metrics_app(environ, start_fn)
        start_fn('200 OK', [])
        return [b'Hello Prometheus']


if __name__ == '__main__':
    httpd = make_server('', 8000, AttachMonitor.attach_app)
    httpd.serve_forever()
