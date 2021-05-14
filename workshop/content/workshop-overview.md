This workshop explores collecting metrics from mod_wsgi and how you might use metrics as input to decisions around tuning Apache and mod_wsgi.

As a whole, the workshop is still very much a work in progress and there are many more topics which will eventually be covered. Completion of the workshop may take some time. If you have any feedback about the workshop then you can direct them to [@GrahamDumpleton](https://twitter.com/GrahamDumpleton) on Twitter or via the mod_wsgi mailing list.

For the workshop we will be using `mod_wsgi-express`, however concepts should be transferable to a manually configured Apache and mod_wsgi installation.

You must be using mod_wsgi 4.8.0 or later to be able to make use of all features demonstrated in this workshop.

For storing of metrics collected from `mod_wsgi` we will be using [InfluxDB](https://www.influxdata.com/). For charting of metrics we will be using [Grafana](https://grafana.com/).
