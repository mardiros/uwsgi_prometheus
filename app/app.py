import os
import logging

from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
from prometheus_client import Counter, CollectorRegistry, generate_latest
from prometheus_client.multiprocess import MultiProcessCollector

log = logging.getLogger('app')

app_hello_count = Counter('app_hello_count', 'Number of hello world')


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
