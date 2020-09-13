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
