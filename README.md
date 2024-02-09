### Overview

#### What is this repo?

#### Architecture

#### How do I get started?

### Installation on server

#### OpenTelemetry Collector

##### Purpose

This is the collector that will gather telemetry information from the systems we want to monitor.
It will push this data to Prometheus.

##### Steps

Also, it will
1. Follow installation instructions for collector [here](https://opentelemetry.io/docs/collector/installation/\#linux).
2. Verify installation was successful with :
```
$ service otelcol status
Redirecting to /bin/systemctl status otelcol.service
? otelcol.service - OpenTelemetry Collector
     Loaded: loaded (/usr/lib/systemd/system/otelcol.service; enabled; vendor preset: disabled)
     Active: active (running) since Fri 2024-02-09 15:55:59 CST; 4min 47s ago
   Main PID: 3260254 (otelcol)
      Tasks: 22 (limit: 154460)
     Memory: 21.0M
     CGroup: /system.slice/otelcol.service
             юд3260254 /usr/bin/otelcol --config=/etc/otelcol/config.yaml

Feb 09 16:00:45 idir-server12 otelcol[3260254]: Descriptor:
Feb 09 16:00:45 idir-server12 otelcol[3260254]:      -> Name: up
Feb 09 16:00:45 idir-server12 otelcol[3260254]:      -> Description: The scraping was successful
Feb 09 16:00:45 idir-server12 otelcol[3260254]:      -> Unit:
Feb 09 16:00:45 idir-server12 otelcol[3260254]:      -> DataType: Gauge
Feb 09 16:00:45 idir-server12 otelcol[3260254]: NumberDataPoints #0
Feb 09 16:00:45 idir-server12 otelcol[3260254]: StartTimestamp: 1970-01-01 00:00:00 +0000 UTC
Feb 09 16:00:45 idir-server12 otelcol[3260254]: Timestamp: 2024-02-09 22:00:45.394 +0000 UTC
Feb 09 16:00:45 idir-server12 otelcol[3260254]: Value: 1.000000
Feb 09 16:00:45 idir-server12 otelcol[3260254]:         {"kind": "exporter", "data_type": "metrics", "name": "debug"}
$
```
3. Clone this repo onto the server.
4. Follow instructions for [Automatic service configuration](https://opentelemetry.io/docs/collector/installation/#automatic-service-configuration) and point to the `config.yaml` file in the `otel` folder of this repo.
5. Confirm the service is operating as expected with:
```
$ sudo systemctl restart otelcol
$ sudo journalctl -u otelcol
```
