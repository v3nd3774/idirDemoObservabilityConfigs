### Overview

#### What is this repo?

#### Architecture

#### How do I get started?

### Installation on server

#### Prometheus

##### Purpose

This is the time series database that will store telemetry data for the systems we want to monitor.
Additionally, it can generate alerts based on customized queries for this data.
These alerts will be sent to ZenDuty through an integration to generate an SMS alert as needed.

##### Steps

1. Download prometheus install file from pre-compiled binaries with (may need to update version strings):
```
$ wget https://github.com/prometheus/prometheus/releases/download/v2.49.1/prometheus-2.49.1.linux-amd64.tar.gz
$ mkdir prometheus
$ tar -C prometheus -xvzf prometheus-2.49.1.linux-amd64.tar.gz
```
2. Move the prometheus installation to the desired location with:

```
$mv prometheus/prometheus-2.49.1 <desired location here>
```
3. Create a `prometheus` linux user and group on the system to run the prometheus instance.

4. Create the folder for prometheus to store data with:
```
$sudo mkdir /var/lib/prometheus/data
$sudo chown -R prometheus:prometheus /var/lib/prometheus
```
5. Copy the template for the prometheus service from this repo to `/etc/systemd/system/prometheus.service` with:
```
# From this repo for pwd:
$sudo cp prometheus/prometheus.service.template /etc/systemd/system/prometheus.service
```
6. Fill in the required data in the service file template with `sudo vim /etc/systemd/system/prometheus.service`

7. Copy the template file to the appropriate location with `$cp <path to repo>/prometheus/prometheus.{yml.template, yml}`

8. Fill in the required data in the configuration template with `vim <path to repo>/prometheus/prometheus.yml`

9. Reload the daemon that manages services with: `$ sudo systemctl daemon-reload`

10. Make SELinux changes to filetype of binary so `systemd` can execute it with: `$chcon -t bin_t <path to prometheus install>/prometheus`

11. Start the prometheus service with: `$ sudo systemctl start prometheus`

12. Confirm the prometheus service is working with: `$ sudo systemctl status prometheus`

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
#### Resources

- [Install the Collector](https://opentelemetry.io/docs/collector/installation/)
- [A practical guide to data collection with OpenTelemetry and Prometheus](https://grafana.com/blog/2023/07/20/a-practical-guide-to-data-collection-with-opentelem-and-prometheus/)
- [How to Run Prometheus server as a Service?](https://www.devopsschool.com/blog/how-to-run-prometheus-server-as-a-service/)
- [Python app instrumentation](https://opentelemetry.io/docs/languages/python/getting-started/)
