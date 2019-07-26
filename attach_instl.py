import subprocess

from prometheus_client import make_wsgi_app
from prometheus_client import Gauge
from wsgiref.simple_server import make_server

metrics_app = make_wsgi_app()

ATTACH_STATUS = Gauge('attach_status', 'Secure Mobile Connect Attach status')
attach_status = 0


def do_attach():
    result = subprocess.run(('sudo pon'))
    print(result)


def attach_app(environ, start_fn):
    global attach_status
    if environ['PATH_INFO'] == '/metrics':
        do_attach()
        attach_status = not attach_status
        ATTACH_STATUS.set(attach_status)
        return metrics_app(environ, start_fn)
    start_fn('200 OK', [])
    return [b'Hello Prometheus']


if __name__ == '__main__':
    httpd = make_server('', 8000, attach_app)
    httpd.serve_forever()
