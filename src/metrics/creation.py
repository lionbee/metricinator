import platform
import time
from typing import Any, Callable, List, Tuple
from typing_extensions import TypedDict

EnrichedMetric = TypedDict(
    "EnrichedMetric",
    {"hostname": str, "epoch": int, "id": str, "measure": float},
)
Metric = Tuple[str, float]
Enricher = Callable[[Metric], EnrichedMetric]
MetricCreator = Callable[[], Metric]
MetricSupplier = Callable[[], Any]


def create_metric_function(id: str, fn: MetricSupplier) -> MetricCreator:
    def metric_function():
        return id, fn()

    metric_function.__name__ = id
    return metric_function


def create_metric_functions(
    metrics: List[Tuple[str, MetricSupplier]]
) -> List[MetricCreator]:
    return [create_metric_function(id, fn) for id, fn in metrics]


def get_enricher(
    hostname: str = platform.node(),
    epoch: Callable[[], int] = lambda: int(time.time() * 1000),
) -> Enricher:
    def enrich(metric: Metric) -> EnrichedMetric:
        return {
            "hostname": hostname,
            "epoch": epoch(),
            "id": metric[0],
            "measure": metric[1],
        }

    return enrich
