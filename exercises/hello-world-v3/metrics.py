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
    """Writes a single data point to InfluxDB.

    """

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

class WSGIApplicationIterable(wrapt.ObjectProxy):

    """A wrapper object for the result returned by the WSGI application when
    called. It uses a transparent object proxy to wrap the original response
    such that any operations are passed through to the original. The only
    exception is that the call to the close() method of any iterable by the
    WSGI server is intercepted and used to close out timing for the request
    and report a metric to InfluxDB.

    """

    def __init__(self, wrapped, start_time):
        super().__init__(wrapped)

        # Save away the time the wrapped function was called.

        self._self_start_time = start_time

    def close(self):
        # A close() method on an iterable returned from a WSGI application
        # is required to be called by the WSGI server at the end of a request,
        # whether the request was successful, or an exception was raised.
        # If the original wrapped object returned by the WSGI application
        # provided a close() method we need to ensure it is in turn called.

        try:
            if hasattr(self.__wrapped__, 'close'):
                self.__wrapped__.close()

        finally:
            # Remember the time the close() function was called.

            stop_time = datetime.now()

            # Calculate how long the function took to run.

            duration = (stop_time - self._self_start_time).total_seconds()

            # Write the metrics to InfluxDB for the function call.

            report_metric(stop_time, duration)

@wrapt.decorator
def wsgi_application(wrapped, instance, args, kwargs):
    """Reports a metric to InfluxDB for each HTTP request handled
    by the wrapped WSGI application.

    """

    # Remember time the wrapped function was called.

    start_time = datetime.now()

    try:
        # Call the wrapped function. The result can be any iterable, but may
        # specifically be a generator. In any case, the WSGI server would
        # iterate over the result and consume the yielded response. Any code
        # implementing the WSGI application may not be executed until the WSGI
        # server starts to consume the response. This is the case for a
        # generator, but could also be the case for custom iterable responses.
        # It is only for the simple case of the iterable being a list of
        # strings where no further code execution to generate the content will
        # occur after this point.

        result = wrapped(*args, **kwargs)

        # Rather than return the result, we wrap the result in a transparent
        # object proxy and return that instead. Because a transparent object
        # proxy is used, any actions to consume the iterable get transferred
        # through to the result object wrapped by the proxy. As such the
        # wrapper object doesn't need to implement methods for an iterable and
        # make the calls to the wrapped object itself. The wrapper object only
        # provides and intercepts a call to the close() method of any
        # iterable.

        return WSGIApplicationIterable(result, start_time)

    except:
        # This case handles where the calling of the wrapped function resulted
        # in an exception. This could occur where the wrapped function is not
        # a generator. We need to record a metric still even when it fails. So
        # remember the time the wrapped function returned.

        stop_time = datetime.now()

        # Calculate how long the function took to run.

        duration = (stop_time - start_time).total_seconds()

        # Write the metrics to InfluxDB for the function call.

        report_metric(stop_time, duration)

        # Raise the original exception so that the WSGI server still sees
        # it and logs the details.

        raise
