Although we have seen that the WSGI application decorator and wrapper do the job as far as timing how long it took to handle a HTTP request, and this can be made to work for any WSGI server, it turns out it is not actually required for `mod_wsgi`. This is because `mod_wsgi` implements an event callback system which can be used to track various aspects of the lifecyle of handling a request.

To use this instead, we first remove the decorator from the WSGI application entrypoint as shown in the file `~/exercises/hello-world-v6/wsgi.py`.

```editor:open-file
file: ~/exercises/hello-world-v6/wsgi.py
```

The use of a decorator is replaced by a registration of an event callback with `mod_wsgi`. This is found in `~/exercises/hello-world-v6/metrics.py`.

```editor:open-file
file: ~/exercises/hello-world-v6/metrics.py
```

The callback function in this case has been called `event_handler()`.

```editor:select-matching-text
text: "def event_handler(.*):"
file: ~/exercises/hello-world-v6/metrics.py
isRegex: true
```

and it is registered using the `mod_wsgi.subscribe_events()` function.

```editor:select-matching-text
text: "mod_wsgi.subscribe_events(event_handler)"
file: ~/exercises/hello-world-v6/metrics.py
```

As we still need to report the metrics, we still have the background task which periodically sends the accumulated metrics to InfluxDB.

To verify that this version still produces the same results, run the WSGI application. We will return to using the original default configuration.

```terminal:execute
command: mod_wsgi-express start-server hello-world-v6/wsgi.py --log-to-terminal --working-directory hello-world-v6
clear: true
```

Once more start sending the requests through to the WSGI application:

```terminal:execute
command: bombardier -d 180s -c 3 http://localhost:8000
session: 2
```

and check out the results in the **Raw Requests** dashboard of Grafana.

```dashboard:reload-dashboard
name: Grafana
url: {{ingress_protocol}}://{{session_namespace}}-grafana.{{ingress_domain}}{{ingress_port_suffix}}/d/raw-requests?orgId=1&refresh=5s
```

What you see for throughput should be more or less the same as what we got when using the WSGI application decorator.

Later on in the workshop we will delve more into what can be done with the events generated for requests and the extra information available included with them about each request. Before we get to that though, we are going to look at a completely different way of generating the request metrics from `mod_wsgi`.

Stop `bombardier` if it is still runing, as well as the WSGI application.

```terminal:interrupt-all
```
