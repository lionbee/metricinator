import persist.database as db
from datetime import datetime
from metrics.creation import EnrichedMetric


def write_gauge(metric: EnrichedMetric) -> None:
    host, created = db.Host.get_or_create(name=metric["hostname"])
    dbMetric, created = db.Metric.get_or_create(name=metric["id"])

    gauge = db.Gauge.create(
        host=host,
        metric=dbMetric,
        created_date=datetime.utcfromtimestamp(metric["epoch"] / 1000),
        measure=metric["measure"],
    )
    return gauge
