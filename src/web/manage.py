# -*- coding: utf-8 -*-

import os

from apps import create_app

from flask_script import Manager, Shell
from tornado.httpserver import HTTPServer
from tornado.wsgi import WSGIContainer
from tornado.ioloop import IOLoop


def development_server():
    app = create_app(os.getenv('FLASK_CONFIG') or 'default')

    def make_shell_context():
        return dict(app=app)
    manager = Manager(app)
    manager.add_command('shell', Shell(make_context=make_shell_context))
    manager.run()


def product_server():
    app = create_app('production')
    server = HTTPServer(WSGIContainer(app))
    server.listen(80)
    IOLoop.current().start()


if __name__ == '__main__':

    development_server()

    # product_server()
