import socket
import threading
import os

import wrapt

import mod_wsgi

from influxdb import InfluxDBClient
from datetime import datetime

client = InfluxDBClient('localhost', 8086, 'wsgi', 'wsgi', 'wsgi')

hostname = socket.gethostname()
pid = os.getpid()

process = f"{hostname}:{pid}"

lock = threading.Lock()
data_points = []

@wrapt.synchronized(lock)
def record_metric(stop_time, duration):
    global data_points

    data_points.append(
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
    )

def report_metrics():
    global data_points

    with wrapt.synchronized(lock):
        pending_data_points = data_points
        data_points = []

    if data_points:
        client.write_points(data_points)

def shutdown_handler(name, **kwargs):
    report_metrics()

mod_wsgi.subscribe_shutdown(shutdown_handler)

class WSGIApplicationIterable(wrapt.ObjectProxy):

    def __init__(self, wrapped, start_time):
        super().__init__(wrapped)
        self._self_start_time = start_time

    def close(self):
        if hasattr(self.__wrapped__, 'close'):
            self.__wrapped__.close()

        stop_time = datetime.now()
        duration = (stop_time - self._self_start_time).total_seconds()

        record_metric(stop_time, duration)

@wrapt.decorator
def wsgi_application(wrapped, instance, args, kwargs):
    start_time = datetime.now()

    try:
        return WSGIApplicationIterable(wrapped(*args, **kwargs), start_time)

    except:
        stop_time = datetime.now()
        duration = (stop_time - start_time).total_seconds()

        record_metric(stop_time, duration)

        raise
