```editor:open-file
file: ~/exercises/hello-world-v2/wsgi-1.py
```

```editor:execute-command
command: workbench.action.findInFiles
args:
- query: "@metrics.function_call"
  filesToInclude: hello-world-v2/wsgi-1.py
  isRegex: false
```

```editor:open-file
file: ~/exercises/hello-world-v2/metrics.py
```

```editor:execute-command
command: workbench.action.findInFiles
args:
- query: "def function_call(.*):"
  filesToInclude: hello-world-v2/metrics.py
  isRegex: true
```

```terminal:execute
command: |
    curl -H "Content-Type: application/json" --user admin:admin --data @grafana/raw-requests.json http://{{session_namespace}}-grafana:3000/api/dashboards/db
```

```terminal:execute
command: mod_wsgi-express start-server hello-world-v2/wsgi-1.py --log-to-terminal --working-directory hello-world-v2
```

```terminal:execute
command: siege -t 300s -c 10 http://localhost:8000
session: 2
```

```dashboard:reload-dashboard
name: Grafana
url: {{ingress_protocol}}://{{session_namespace}}-grafana.{{ingress_domain}}/d/raw-requests?orgId=1&refresh=5s
```

```terminal:interrupt-all
```

```terminal:execute
command: mod_wsgi-express start-server hello-world-v2/wsgi-2.py --log-to-terminal --working-directory hello-world-v2
```

```terminal:execute
command: siege -t 300s -c 10 http://localhost:8000
session: 2
```

```dashboard:reload-dashboard
name: Grafana
url: {{ingress_protocol}}://{{session_namespace}}-grafana.{{ingress_domain}}/d/raw-requests?orgId=1&refresh=5s
```

```terminal:interrupt-all
```
