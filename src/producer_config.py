"""
Configuration for metric data production
"""

import json
import logging
import psutil
from kafka import KafkaProducer
from kafka_config import server_config
from kafka_utils.send import get_topic_send
from metrics.creation import create_metric_functions, get_enricher
from metrics.writer import get_writer


_kafka_producer = KafkaProducer(
    **server_config, value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)


def _debug_send(*args):
    print(args)


_metrics = metric_functions = create_metric_functions(
    [
        ("cpu.percent", psutil.cpu_percent),
        ("disk.usage.percent", lambda: psutil.disk_usage("/").percent),
    ]
)
_metric_send = get_topic_send("metrics", _kafka_producer.send)
_enrich = get_enricher()

log_level = logging.INFO


def shutdown():
    _kafka_producer.close(timeout=10)


metric_writer = get_writer(_metrics, _metric_send, _enrich)
interval_seconds = 1
