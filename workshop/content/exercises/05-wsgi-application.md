```editor:open-file
file: ~/exercises/hello-world-v3/metrics.py
```

Search for the implementation of the decorator. 

```editor:execute-command
command: workbench.action.findInFiles
args:
- query: "def wsgi_application\\(.*\\):"
  filesToInclude: hello-world-v3/metrics.py
  isRegex: true
```

Click on the search result on the left side of the editor to scroll down to the appropriate line if necessary.

```editor:open-file
file: ~/exercises/hello-world-v3/wsgi-1.py
```

```editor:execute-command
command: workbench.action.findInFiles
args:
- query: "@wsgi_application"
  filesToInclude: hello-world-v3/wsgi-1.py
  isRegex: false
```

```terminal:execute
command: mod_wsgi-express start-server hello-world-v3/wsgi-1.py --log-to-terminal --working-directory hello-world-v3
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
