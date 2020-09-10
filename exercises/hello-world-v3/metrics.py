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

def report_metric(stop_time, duration):
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

class WSGIApplicationIterable(wrapt.ObjectProxy):

    def __init__(self, wrapped, start_time):
        super().__init__(wrapped)
        self._self_start_time = start_time

    def close(self):
        if hasattr(self.__wrapped__, 'close'):
            self.__wrapped__.close()

        stop_time = datetime.now()
        duration = (stop_time - self._self_start_time).total_seconds()

        report_metric(stop_time, duration)

@wrapt.decorator
def wsgi_application(wrapped, instance, args, kwargs):
    start_time = datetime.now()

    try:
        return WSGIApplicationIterable(wrapped(*args, **kwargs), start_time)

    except:
        stop_time = datetime.now()
        duration = (stop_time - start_time).total_seconds()

        report_metric(stop_time, duration)

        raise
