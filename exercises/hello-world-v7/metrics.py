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

    data_points = []

    data_points.append(
        {
            "measurement": "request-metrics",
            "time": stop_time,
            "tags": {
                "hostname": hostname,
                "process": process
            },
            "fields": {
                "request_throughput": metrics["request_throughput"],
                "capacity_utilization": metrics["capacity_utilization"],
                "server_time": metrics["server_time"],
                "application_time": metrics["application_time"],
                "cpu_user_time": metrics["cpu_user_time"],
                "cpu_system_time": metrics["cpu_system_time"],
                "request_threads_maximum": metrics["request_threads_maximum"],
                "request_threads_started": metrics["request_threads_started"],
                "request_threads_active": metrics["request_threads_active"]
            }
        }
    )

    server_time_buckets = metrics["server_time_buckets"]
    application_time_buckets = metrics["application_time_buckets"]

    def add_bucket(threshold, server_count, application_count):
        data_points.append(
            {
                "measurement": "request-metrics",
                "time": stop_time,
                "tags": {
                    "hostname": hostname,
                    "process": process,
                    "time_bucket": threshold,
                },
                "fields": {
                    "server_time_bucket": server_count,
                    "application_time_bucket": application_count
                }
            }
        )

    threshold = 0.0

    for i in range(15):
        add_bucket(threshold, server_time_buckets[i], application_time_buckets[i])
        threshold = (threshold * 2) or 0.005

    add_bucket(float("inf"), server_time_buckets[-1], server_time_buckets[-1])

    client.write_points(data_points)

def shutdown_handler(name, **kwargs):
    queue.put(None)

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

queue = Queue()
thread = Thread(target=collector)

def enable_reporting():
    mod_wsgi.subscribe_shutdown(shutdown_handler)
    thread.start()
