from core.context import Context
from core.application import Application

from .server import ZenServer
import core.util
import multiprocessing
import webbrowser


global port


def run(env, start_response):
    print ('>>> process request')
    context = Context(env=env)
    application = Application(context)
    start_response(context.status, context.get_headers())
    return context.get_response()


def ready(server):
    global port
    url = f'http://localhost:{port}'
    webbrowser.open(url)


def launch(use_port=None):
    global port
    workers = (multiprocessing.cpu_count() * 2) + 1
    if use_port:
        port = use_port
    else:
        port = core.util.get_free_port()
    options = {
        'bind': '%s:%s' % ('127.0.0.1', port),
        'workers': workers,
        'when_ready': ready
    }
    ZenServer(run, options).run()
