#!/usr/bin/env python

import psutil
import signal
import sys
import time

import metrics


def shutdown(sig, frame):
    print("Shutting down")
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGQUIT, shutdown)
    enrich = metrics.get_enricher()
    metric_functions = metrics.create_metric_functions(
        [("cpu.percent", psutil.cpu_percent)]
    )

    while True:
        for f in metric_functions:
            print(enrich(f()))
        time.sleep(1)
