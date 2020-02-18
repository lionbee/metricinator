#!/usr/bin/env python

import logging
import producer_config
import time

if producer_config.log_level:
    logging.basicConfig(level=producer_config.log_level)
logger = logging.getLogger("producer")


def produce_metrics(
    metric_writer=producer_config.metric_writer,
    interval_seconds=producer_config.interval_seconds,
    shutdown=producer_config.shutdown,
):
    """
    Produce metrics on a configurable interval
    """
    try:
        while True:
            logger.info("Capturing metrics")
            metric_writer()
            logger.info("Going to sleep for %s", interval_seconds)
            time.sleep(interval_seconds)
    except (KeyboardInterrupt, SystemExit):
        logging.info("shutting down")
    finally:
        shutdown()


if __name__ == "__main__":
    produce_metrics()
