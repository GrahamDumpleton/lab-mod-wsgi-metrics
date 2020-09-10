import atexit
import time
import socket
import os

import mod_wsgi

from threading import Thread
from queue import Queue

from influxdb import InfluxDBClient
from datetime import datetime

session_namespace = os.environ["SESSION_NAMESPACE"]
influxdb_hostname = f"{session_namespace}-influxdb"

client = InfluxDBClient(influxdb_hostname, 8086, 'wsgi', 'wsgi', 'wsgi')

queue = Queue()

interval = 1.0

hostname = socket.gethostname()
pid = os.getpid()

process = f"{hostname}:{pid}"

def report_metrics():
    metrics = mod_wsgi.request_metrics()

    stop_time = datetime.fromtimestamp(metrics["stop_time"]).isoformat()

    client.write_points([
        {
            "measurement": "wsgi.server",
            "time": stop_time,
            "tags": {
                "hostname": hostname,
                "process": process
            },
            "fields": {
                "request_throughput": metrics["request_throughput"],
                "capacity_utilization": metrics["capacity_utilization"],
                "server_queue_time": metrics["server_queue_time"],
                "response_time": metrics["response_time"],
                "cpu_user_time": metrics["cpu_user_time"],
                "cpu_system_time": metrics["cpu_system_time"],
                "request_threads_maximum": metrics["request_threads_maximum"],
                "request_threads_started": metrics["request_threads_started"],
                "request_threads_active": metrics["request_threads_active"]
            }
        }
    ])

def collector():
    mod_wsgi.request_metrics()
    next_time = time.time() + interval
    
    while True:
        next_time += interval
        now = time.time()

        try:
            queue.get(timeout=next_time-now)
            report_metrics()
            return

        except Exception:
            pass

        report_metrics()

thread = Thread(target=collector)
thread.start()

def shutdown_handler(name, **kwargs):
    queue.put(None)

mod_wsgi.subscribe_shutdown(shutdown_handler)

def application(environ, start_response):
    status = '200 OK'
    output = b'Hello World!'

    response_headers = [('Content-type', 'text/plain'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)

    return [output]
