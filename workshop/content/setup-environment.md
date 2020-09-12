Before we start we need to configure Grafana to use InfluxDB as a data source. To do this run the following command by clicking on the action block below.

```terminal:execute
command: |
    curl -H "Content-Type: application/json" --user admin:admin --data @grafana/datasource.json http://{{session_namespace}}-grafana:3000/api/datasources
```

The workshop uses these action blocks for various purposes. Anytime you see such a block with an icon on the right hand side, you can click on it and it will perform the listed action for you, you do not need to enter in these commands yourself.

As well as set up the datasource for InfluxDB in Grafana, we will also pre-load some Grafana dashboards that we will be using as we go along. Execute:

```terminal:execute
command: |
    curl -H "Content-Type: application/json" --user admin:admin --data @grafana/raw-requests.json http://{{session_namespace}}-grafana:3000/api/dashboards/db
```

and:

```terminal:execute
command: |
    curl -H "Content-Type: application/json" --user admin:admin --data @grafana/request-metrics.json http://{{session_namespace}}-grafana:3000/api/dashboards/db
```

To verify that Grafana is running okay, open the **Grafana** dashboard tab.

```dashboard:open-dashboard
name: Grafana
```

There is no need to login to Grafana as anonymous access is enabled for view Grafana dashboards.

We will also be using the embedded VS Code editor later on as well, open the **Editor** dashboard tab to start it up.

```dashboard:open-dashboard
name: Editor
```

Dismiss any popups that VS Code displays.

Finally, return back to the **Terminal** dashboard tab:

```dashboard:open-dashboard
name: Terminal
```

Clear the terminals so we are ready to go.

```terminal:clear-all
```
