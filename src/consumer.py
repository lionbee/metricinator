#!/usr/bin/env python

import consumer_config
import json
import logging
from persist.database import set_database
from persist.metrics import write_gauge

logging.basicConfig(level=consumer_config.log_level)
logger = logging.getLogger("producer")


def consume_metrics(
    consumer=consumer_config.kafka_consumer, db=consumer_config.db
):
    try:
        set_database(db)
        for message in consumer:
            logger.info(message.value)
            metric = json.loads(message.value)
            write_gauge(metric)
    except (KeyboardInterrupt, SystemExit):
        logging.info("shutting down")
        db.close()


if __name__ == "__main__":
    consume_metrics()
