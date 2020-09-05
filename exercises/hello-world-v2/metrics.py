import socket
import os

import wrapt

from influxdb import InfluxDBClient
from datetime import datetime

client = InfluxDBClient('localhost', 8086, 'wsgi', 'wsgi', 'wsgi')

hostname = socket.gethostname()
pid = os.getpid()

process = f"{hostname}:{pid}"

@wrapt.decorator
def function_call(wrapped, instance, args, kwargs):
    start_time = datetime.now()

    try:
        return wrapped(*args, **kwargs)
    finally:
        stop_time = datetime.now()
        duration = (stop_time - start_time).total_seconds()

        client.write_points([
            {
                "measurement": "wsgi.requests",
                "time": stop_time.isoformat(),
                "tags": {
                    "hostname": hostname,
                    "process": process
                },
                "fields": {
                    "application_time": duration
                }
            }
        ])
