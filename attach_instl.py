import subprocess

from prometheus_client import make_wsgi_app
from prometheus_client import Gauge
from wsgiref.simple_server import make_server

metrics_app = make_wsgi_app()

ATTACH_STATUS = Gauge('attach_status', 'Secure Mobile Connect Attach status')
attach_status = 0


def do_detach():
    result = subprocess.run(['poff'])
    print(result)


def do_attach():
    result = subprocess.run(['pon'])
    print(result)
    return result.returncode


def attach_app(environ, start_fn):
    global attach_status
    if environ['PATH_INFO'] == '/metrics':
        do_detach()
        result = do_attach()
        if result == 0:
            attach_status = 1
        else:
            attach_status = 0
        ATTACH_STATUS.set(attach_status)
        return metrics_app(environ, start_fn)
    start_fn('200 OK', [])
    return [b'Hello Prometheus']


if __name__ == '__main__':
    httpd = make_server('', 8000, attach_app)
    httpd.serve_forever()
