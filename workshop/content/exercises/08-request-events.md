```editor:open-file
file: ~/exercises/hello-world-v6/wsgi.py
```

```editor:open-file
file: ~/exercises/hello-world-v6/metrics.py
```

```editor:execute-command
command: workbench.action.findInFiles
args:
- query: "def event_handler(.*):"
  filesToInclude: hello-world-v6/metrics.py
  isRegex: true
```

```editor:execute-command
command: workbench.action.findInFiles
args:
- query: "mod_wsgi.subscribe_events(event_handler)"
  filesToInclude: hello-world-v6/metrics.py
  isRegex: false
```

```terminal:execute
command: mod_wsgi-express start-server hello-world-v6/wsgi.py --log-to-terminal --working-directory hello-world-v6
```

```terminal:execute
command: siege -t 300s -c 10 http://localhost:8000
session: 2
```

```dashboard:reload-dashboard
name: Grafana
url: {{ingress_protocol}}://{{session_namespace}}-grafana.{{ingress_domain}}{{ingress_port_suffix}}/d/raw-requests?orgId=1&refresh=5s
```

```terminal:interrupt-all
```
