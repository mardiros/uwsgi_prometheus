import os
import logging

from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config

log = logging.getLogger('app')


@view_config(route_name='hello')
def hello_world(request):
    log.info('Serving hello world')
    return Response('Hello World!')


with Configurator() as config:
    logging.basicConfig(level=logging.DEBUG)
    log.info('Starting')
    config.scan('.')
    config.add_route('hello', '/')

    application = config.make_wsgi_app()
    log.info('Application built')


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', 6543, application)
    server.serve_forever()
