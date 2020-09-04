import time

import metrics

@metrics.application_time
def application(environ, start_response):
    status = '200 OK'

    response_headers = [('Content-type', 'text/plain')]]
    start_response(status, response_headers)

    yield b'Hello '

    time.sleep(0.005)

    yield b' World!'
