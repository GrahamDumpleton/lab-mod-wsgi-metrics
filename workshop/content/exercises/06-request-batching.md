```terminal:execute
command: mod_wsgi-express start-server hello-world-v4/wsgi.py --log-to-terminal --working-directory hello-world-v4
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
command: mod_wsgi-express start-server hello-world-v5/wsgi.py --log-to-terminal --working-directory hello-world-v5
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