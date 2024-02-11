"""
Browses to frontend and waits for bipartite graph visualization to load.
"""
from time import sleep, time
from typing import List, Union

from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics.export import (
    PeriodicExportingMetricReader,
    ConsoleMetricExporter
)

from selenium import webdriver
from selenium.webdriver import ChromeOptions, Remote
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


# Setup OTEL Collector Connection
# Also setup metric info
OTLP_ENDPOINT: str = "http://localhost:4318"
OTLP_V: str = "v1"
resource: Resource = Resource(attributes={
    SERVICE_NAME: "bipartiteGraphUiSeleniumSvgTest"
})
metric_readers: List[PeriodicExportingMetricReader] = [
    PeriodicExportingMetricReader(ConsoleMetricExporter()),
    PeriodicExportingMetricReader(OTLPMetricExporter(endpoint=f"{OTLP_ENDPOINT}/{OTLP_V}/metrics"))
]
provider = MeterProvider(resource=resource, metric_readers=metric_readers)
metrics.set_meter_provider(provider)
meter = metrics.get_meter("bipartiteGraphUiSeleniumSvgTest")
duration_metric = meter.create_counter(
    "bipartiteGraphUiSeleniumSvgTestDuration",
    unit="S"
)

# Setup connection to selenium server
options: ChromeOptions = webdriver.ChromeOptions()
driver: Remote = webdriver.Remote(
    command_executor="http://localhost:4444",
    options=options
)

# run test
# Test will browse to the bipartite graph web app
# It will time how long until the graph is rendered.
# It will timeout after 150s.
# At the end of the test metrics will be pushed to Otel collector
start_time: float = time()
driver.get("https://idir.uta.edu/bipartiteGraphUi/")
driver.implicitly_wait(1)
RETRIES: int = 15
SLEEP_TIME: int = 10
bipartite_graph_svg: "WebElement | None" = None
while RETRIES >= 0:
    try:
        bipartite_graph_svg = driver.find_element(
            by=By.CSS_SELECTOR,
            value="container > svg"
        )
    except NoSuchElementException:
        pass
    if bipartite_graph_svg and bipartite_graph_svg.is_displayed():
        break
    RETRIES = RETRIES - 1
    sleep(SLEEP_TIME)
end_time: float = time()
duration_S: float = end_time - start_time
duration_metric.add(
    duration_S,
    {
        "test": "svgLoadTimeTest"
    }
)
for metric_reader in metric_readers:
    metric_reader.force_flush()
driver.quit()
