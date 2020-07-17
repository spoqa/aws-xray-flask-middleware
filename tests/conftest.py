from __future__ import absolute_import

from aws_xray_sdk import global_sdk_config
from aws_xray_sdk.core.context import Context
from flask import Flask
from pytest import fixture, yield_fixture
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from spoqa_aws_xray_flask_middleware import XRayMiddleware
from tests.util import get_new_stubbed_recorder


@yield_fixture
def fx_recorder():
    recorder = get_new_stubbed_recorder()
    recorder.configure(service='test', sampling=False, context=Context())
    recorder.clear_trace_entities()
    yield recorder
    recorder.clear_trace_entities()
    global_sdk_config.set_sdk_enabled(True)


@fixture
def fx_second_flask_app():
    app = Flask(__name__)

    @app.route('/ping')
    def ping():
        return 'pong'

    @app.route('/bye/<string:name>')
    def bye(name):
        return 'Bye, {}'.format(name)
    app.config['TESTING'] = True

    return app


@fixture
def fx_flask_app(fx_second_flask_app):
    app = Flask(__name__)

    @app.route('/ok')
    def ok():
        return 'ok'

    @app.route('/hello/<string:name>')
    def hello(name):
        return 'Hello, {}'.format(name)

    app.wsgi_app = DispatcherMiddleware(
        app.wsgi_app,
        {'/nested': fx_second_flask_app},
    )
    app.config['TESTING'] = True

    return app


@fixture
def fx_flask_app_with_middleware(
    fx_recorder,
    fx_flask_app,
    fx_second_flask_app,
):
    XRayMiddleware(fx_flask_app, fx_recorder)
    XRayMiddleware(fx_second_flask_app, fx_recorder)
    return fx_flask_app
