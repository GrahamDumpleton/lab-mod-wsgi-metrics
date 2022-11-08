#!/bin/bash

INFLUXDB_HOST=influxdb-workshop
export INFLUXDB_HOST

envsubst < $HOME/exercises/grafana/datasource.json.in > $HOME/exercises/grafana/datasource.json
