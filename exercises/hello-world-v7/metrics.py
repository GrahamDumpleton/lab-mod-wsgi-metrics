import atexit
import time
import socket
import traceback
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
    """Report aggregated metrics to InfluxDB.

    """

    # Grab the set of metrics for the current reporting period.

    metrics = mod_wsgi.request_metrics()

    stop_time = datetime.fromtimestamp(metrics["stop_time"]).isoformat()

    data_points = []

    # Create a record for InfluxDB of the primary metrics.

    measurement = {
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
            "memory_max_rss": metrics["memory_max_rss"],
            "memory_rss": metrics["memory_rss"],
            "request_threads_maximum": metrics["request_threads_maximum"],
            "request_threads_started": metrics["request_threads_started"],
            "request_threads_active": metrics["request_threads_active"]
        }
    }

    if metrics["queue_time"] is not None:
        measurement["fields"]["queue_time"] = metrics["queue_time"]

    if metrics["daemon_time"] is not None:
        measurement["fields"]["daemon_time"] = metrics["daemon_time"]

    data_points.append(measurement)

    # Now record special bucketed metrics corresponding to the spread
    # of response times. The first bucket is for 0 to 0.005 seconds.
    # The next will be 0.005 to 0.010. For each subsequent bucket, the
    # end of the time bucket is doubled, except for the last bucket,
    # which is opened ended and covers up to infinity. There should be
    # a total of 16 buckets.

    server_time_buckets = metrics["server_time_buckets"]
    queue_time_buckets = metrics["queue_time_buckets"]
    daemon_time_buckets = metrics["daemon_time_buckets"]
    application_time_buckets = metrics["application_time_buckets"]

    def add_bucket_1(threshold, server_count, queue_count, daemon_count, application_count):
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
                    "queue_time_bucket": queue_count,
                    "daemon_time_bucket": daemon_count,
                    "application_time_bucket": application_count
                }
            }
        )

    threshold = 0.0

    for i in range(len(server_time_buckets)-1):
        add_bucket_1(threshold, server_time_buckets[i], queue_time_buckets[i], daemon_time_buckets[i], application_time_buckets[i])
        threshold = (threshold * 2) or 0.005

    add_bucket_1(float("inf"), server_time_buckets[-1], queue_time_buckets[-1], daemon_time_buckets[-1], application_time_buckets[-1])

    request_threads_buckets = metrics["request_threads_buckets"]

    def add_bucket_2(thread_id, request_count):
        data_points.append(
            {
                "measurement": "request-metrics",
                "time": stop_time,
                "tags": {
                    "hostname": hostname,
                    "process": process,
                    "thread_id": thread_id,
                },
                "fields": {
                    "request_threads_bucket": request_count
                }
            }
        )

    for i, value in enumerate(sorted(request_threads_buckets, reverse=True)):
        add_bucket_2(i+1, value)

    # Write the metrics to InfluxDB.

    try:
        client.write_points(data_points)

    except Exception:
        traceback.print_exc()

def collector():
    # Activate aggregated metrics and set baseline for initial period.
    # Since this is the first time it is being called we ignore result.

    mod_wsgi.request_metrics()

    next_time = time.time() + interval
    
    while True:
        next_time += interval
        now = time.time()

        try:
            # Waiting for next schedule time to report metrics.

            queue.get(timeout=max(0, next_time-now))

            # If we get to here it means the process is being shutdown
            # so we report any metrics that haven't been sent.

            report_metrics()

            return

        except Exception:
            # Timeout occurred on waiting on queue, which means the next
            # reporting time has arrived.

            pass

        # Report the current batch of metrics.

        report_metrics()

queue = Queue()
thread = Thread(target=collector)

def shutdown_handler(name, **kwargs):
    queue.put(None)

def enable_reporting():
    """Subscribe to shutdown of the application so we can report the last
    batch of metrics and notify the collector thread to shutdown.

    """

    mod_wsgi.subscribe_shutdown(shutdown_handler)

    # Start collector thread for periodically reporting accumlated metrics.

    thread.start()
