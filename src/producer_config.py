"""
Configuration for metric data production
"""

import json
import logging
import psutil
import os.path

from kafka import KafkaProducer
from kafka_wrappers import get_topic_send
from metrics.creation import create_metric_functions, get_enricher
from metrics.writer import get_writer

_module_abs_path = os.path.abspath(os.path.dirname(__file__))
_key_path = os.path.join(_module_abs_path, "../keys")

kafka_producer = KafkaProducer(
    bootstrap_servers="some server",
    security_protocol="SSL",
    ssl_check_hostname=True,
    ssl_cafile=os.path.join(_key_path, "ca.pem"),
    ssl_certfile=os.path.join(_key_path, "service.cert"),
    ssl_keyfile=os.path.join(_key_path, "service.key"),
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)


def _debug_send(*args):
    print(args)


_metrics = metric_functions = create_metric_functions(
    [
        ("cpu.percent", psutil.cpu_percent),
        ("disk.usage.percent", lambda: psutil.disk_usage("/").percent),
    ]
)
_metric_send = get_topic_send("metrics", kafka_producer.send)
_enrich = get_enricher()

log_level = logging.INFO
metric_writer = get_writer(_metrics, _metric_send, _enrich)
interval_seconds = 1
