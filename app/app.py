import os
import sys
import logging
import atexit

from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
from prometheus_client import Counter, Gauge, CollectorRegistry, generate_latest
from prometheus_client.multiprocess import MultiProcessCollector, mark_process_dead

__VERSION__ = '1.0'
version_info = {
    'version': __VERSION__,
    'python_version': '{0}.{1}.{2}'.format(
        sys.version_info.major,
        sys.version_info.minor,
        sys.version_info.micro)
}


log = logging.getLogger('app')

app_hello_count = Counter('app_hello_count', 'Number of hello world')
app_info = Gauge(
    'app_info',
    'Application Information',
    labelnames=version_info.keys(),
    multiprocess_mode='livesum'
    )
app_info.labels(**version_info).set(1)


@atexit.register
def mark_dead():
    log.info('Child process is dead')
    mark_process_dead(os.getpid())


@view_config(route_name='hello')
def hello_world(request):
    log.info('Serving hello world')
    app_hello_count.inc()
    return Response('Hello World!')


@view_config(route_name='metrics')
def metrics(request):
    log.info('Serving metrics')
    registry = CollectorRegistry()
    MultiProcessCollector(registry)
    data = generate_latest(registry)
    return Response(data, content_type='text/plain')


with Configurator() as config:
    logging.basicConfig(level=logging.DEBUG)
    log.info('Starting')
    config.scan('.')
    config.add_route('hello', '/')
    config.add_route('metrics', '/metrics')

    application = config.make_wsgi_app()
    log.info('Application built')


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', 6543, application)
    server.serve_forever()
