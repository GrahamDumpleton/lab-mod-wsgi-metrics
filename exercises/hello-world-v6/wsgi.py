import socket
import os

import mod_wsgi

from influxdb import InfluxDBClient
from datetime import datetime

client = InfluxDBClient('localhost', 8086, 'wsgi', 'wsgi', 'wsgi')

hostname = socket.gethostname()
pid = os.getpid()

process = f"{hostname}:{pid}"

def event_handler(name, **kwargs):
    if name == 'request_finished':
        client.write_points([
            {
                "measurement": "wsgi.requests",
                "time": datetime.now().isoformat(),
                "tags": {
                    "hostname": hostname,
                    "process": process
                },
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
