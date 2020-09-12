import socket
import traceback
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
    """Records a metric to InfluxDB for each call of the function.

    """

    # Remember time the wrapped function was called.

    start_time = datetime.now()

    try:
        # Call the wrapped function.

        return wrapped(*args, **kwargs)
    finally:
        # Remember time the wrapped function returned.

        stop_time = datetime.now()

        # Calculate how long the function took to run.

        duration = (stop_time - start_time).total_seconds()

        # Write the metrics to InfluxDB for the function call.

        try:
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

        except Exception:
            traceback.print_exc()
