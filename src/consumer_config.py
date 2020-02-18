import logging
from kafka import KafkaConsumer
from kafka_config import server_config
from peewee import PostgresqlDatabase

log_level = logging.INFO

kafka_consumer = KafkaConsumer(
    "metrics", **server_config, group_id="metric.consumer"
)

db = PostgresqlDatabase(
    "name", user="username", password="password", host="host", port=26150,
)
