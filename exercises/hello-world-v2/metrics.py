import socket
import os

import wrapt

from influxdb import InfluxDBClient
from datetime import datetime

session_namespace = os.environ["SESSION_NAMESPACE"]
influxdb_hostname = f"{session_namespace}-influxdb"

client = InfluxDBClient(influxdb_hostname, 8086, 'wsgi', 'wsgi', 'wsgi')

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
                "measurement": "raw-requests",
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
