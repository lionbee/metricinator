import logging
from kafka import KafkaConsumer
from kafka_config import server_config
from peewee import PostgresqlDatabase

log_level = logging.INFO

kafka_consumer = KafkaConsumer(
    "metrics", **server_config, group_id="metric.consumer"
)

db = PostgresqlDatabase(
    "metricinator",
    user="metricinator",
    password="rorys2ehw2mt9zti",
    host="pg-aiven-test-abadhideout-6761.aivencloud.com",
    port=26150,
)
