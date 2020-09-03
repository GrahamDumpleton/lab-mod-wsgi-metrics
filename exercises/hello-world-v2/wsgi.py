import mod_wsgi

from influxdb import InfluxDBClient
from datetime import datetime

client = InfluxDBClient('localhost', 8086, 'wsgi', 'wsgi', 'wsgi')

def event_handler(name, **kwargs):
    if name == 'request_finished':
        client.write_points([
            {
                "measurement": "wsgi.requests",
                "time": datetime.now().isoformat(),
                "fields": {
                    "application_time": kwargs["application_time"]
                }
            }
        ])

mod_wsgi.subscribe_events(event_handler)

def application(environ, start_response):
    status = '200 OK'
    output = b'Hello World!'

    response_headers = [('Content-type', 'text/plain'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)

    return [output]
