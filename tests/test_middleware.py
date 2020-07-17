def test_ok(fx_flask_app_with_middleware, fx_recorder):
    client = fx_flask_app_with_middleware.test_client()

    client.get('/ok')

    segment = fx_recorder.emitter.pop()
    assert not segment.in_progress

    request = segment.http['request']
    response = segment.http['response']
    annotation = segment.annotations

    assert request['method'] == 'GET'
    assert request['url'] == '//test/ok'
    assert request['client_ip'] == '127.0.0.1'
    assert response['status'] == 200
    assert response['content_length'] == 2
    assert annotation['url'] == 'http://localhost/ok'


def test_hello(fx_flask_app_with_middleware, fx_recorder):
    client = fx_flask_app_with_middleware.test_client()

    client.get('/hello/xray')

    segment = fx_recorder.emitter.pop()
    assert not segment.in_progress

    request = segment.http['request']
    response = segment.http['response']
    annotation = segment.annotations

    assert request['method'] == 'GET'
    assert request['url'] == '//test/hello/<string:name>'
    assert request['client_ip'] == '127.0.0.1'
    assert response['status'] == 200
    assert response['content_length'] == 11
    assert annotation['url'] == 'http://localhost/hello/xray'


def test_nested_ping(fx_flask_app_with_middleware, fx_recorder):
    client = fx_flask_app_with_middleware.test_client()

    client.get('/nested/ping')

    segment = fx_recorder.emitter.pop()
    assert not segment.in_progress

    request = segment.http['request']
    response = segment.http['response']
    annotation = segment.annotations

    assert request['method'] == 'GET'
    assert request['url'] == '//test/nested/ping'
    assert request['client_ip'] == '127.0.0.1'
    assert response['status'] == 200
    assert response['content_length'] == 4
    assert annotation['url'] == 'http://localhost/nested/ping'


def test_nested_bye(fx_flask_app_with_middleware, fx_recorder):
    client = fx_flask_app_with_middleware.test_client()

    client.get('/nested/bye/xray')

    segment = fx_recorder.emitter.pop()
    assert not segment.in_progress

    request = segment.http['request']
    response = segment.http['response']
    annotation = segment.annotations

    assert request['method'] == 'GET'
    assert request['url'] == '//test/nested/bye/<string:name>'
    assert request['client_ip'] == '127.0.0.1'
    assert response['status'] == 200
    assert response['content_length'] == 9
    assert annotation['url'] == 'http://localhost/nested/bye/xray'
