For a WSGI application, we therefore need a more complicated wrapper to be able track HTTP requests. Such a wrapper can be found in `~/exercises/hello-world-v3/metrics.py`.

```editor:open-file
file: ~/exercises/hello-world-v3/metrics.py
```

Search for the implementation of the wrapper.

```editor:execute-command
command: workbench.action.findInFiles
args:
- query: "def wsgi_application\\(.*\\):"
  filesToInclude: hello-world-v3/metrics.py
  isRegex: true
```

Click on the search result on the left side of the editor to scroll down to the appropriate line if necessary.

We still use a decorator to intercept the initial call, but we wrap up the result of the call to the original WSGI application with a transparent proxy object. This proxy object intercepts the `close()` method that WSGI servers are required to call at the completion of any HTTP request. It is in this `close()` method that we can record the metric for how long the request takes.

If interested in the details, read through the source code. Comments are included to try and explain what is occuring, and how certain error conditions are catered for.

Now open up our modified WSGI application code file.

```editor:open-file
file: ~/exercises/hello-world-v3/wsgi-1.py
```

You will see that all we have done is swap out the prior operator with the `@metrics.wsgi_application` decorator.

```editor:execute-command
command: workbench.action.findInFiles
args:
- query: "@metrics.wsgi_application"
  filesToInclude: hello-world-v3/wsgi-1.py
  isRegex: false
```

To test the decorator does what is required, start up the WSGI application:

```terminal:execute
command: mod_wsgi-express start-server hello-world-v3/wsgi-1.py --log-to-terminal --working-directory hello-world-v3
```

and send through a stream of requests.

```terminal:execute
command: bombardier -d 120s -c 1 -r 1 http://localhost:8000
session: 2
```

Jump over to the **Raw Requests** dashboard in Grafana

```dashboard:reload-dashboard
name: Grafana
url: {{ingress_protocol}}://{{session_namespace}}-grafana.{{ingress_domain}}{{ingress_port_suffix}}/d/raw-requests?orgId=1&refresh=5s
```

```terminal:interrupt-all
```

```terminal:execute
command: mod_wsgi-express start-server hello-world-v3/wsgi-2.py --log-to-terminal --working-directory hello-world-v3
```

```terminal:execute
command: siege -t 300s -c 10 http://localhost:8000
session: 2
```

```dashboard:reload-dashboard
name: Grafana
url: {{ingress_protocol}}://{{session_namespace}}-grafana.{{ingress_domain}}{ingress_port_suffix}}/d/raw-requests?orgId=1&refresh=5s
```

```terminal:interrupt-all
```
