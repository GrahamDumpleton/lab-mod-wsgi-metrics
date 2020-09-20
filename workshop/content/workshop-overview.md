This workshop explores generating metrics from mod_wsgi and how you might use metrics to tune Apache and mod_wsgi.

As a whole, the workshop is still very much a work in progress and there are many more topics which will eventually be covered. Completion of the workshop may take some time. If you have any feedback about the workshop then you can direct them to @GrahamDumpleton on Twitter.

For the workshop we will be using `mod_wsgi-express`, however concepts should be transferable to a manually configured Apache and mod_wsgi installation.

The workshop currently uses a development version of `mod_wsgi` as some tweaks were made to `mod_wsgi` in the process of developing this workshop. The updates will be released in an official version of `mod_wsgi` at a future date. If you want to experiment with some parts of what is described, for now, you will need to use the same development version of `mod_wsgi`.

For storing of metrics collected from `mod_wsgi` we will be using [InfluxDB](https://www.influxdata.com/). For charting of metrics we will be using [Grafana](https://grafana.com/).
