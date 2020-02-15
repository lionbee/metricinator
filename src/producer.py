#!/usr/bin/env python

import logging
import producer_config
import signal
import sys
import time

logging.basicConfig(level=producer_config.log_level)
logger = logging.getLogger("producer")


def shutdown(sig, frame):
    logger.info("Flushing kafka")
    producer_config.kafka_producer.flush()
    logger.info("Shutting down")
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGQUIT, shutdown)

    while True:
        logger.info("Captureing metric")
        producer_config.metric_writer()
        logger.info("Going to sleep for %s", producer_config.interval_seconds)
        time.sleep(producer_config.interval_seconds)
