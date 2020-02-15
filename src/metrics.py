import platform
import time

from typing import Any, Callable, List, Tuple
from typing_extensions import TypedDict

Metric = Tuple[str, Any]
EnrichedMetric = TypedDict(
    "Metric", {"hostname": str, "epoch": int, "id": str, "measure": Any}
)
MetricSupplierFn = Callable[[], Any]
MetricFn = Callable[[], Metric]


def create_metric_function(id: str, fn: MetricSupplierFn) -> MetricFn:
    def metric_function():
        return id, fn()

    return metric_function


def create_metric_functions(
    metrics: List[Tuple[str, MetricSupplierFn]]
) -> List[MetricFn]:
    return [create_metric_function(id, fn) for id, fn in metrics]


def get_enricher(
    hostname: str = platform.node(),
    epoch: Callable[[], int] = lambda: int(time.time() * 1000),
) -> Callable[[Metric], EnrichedMetric]:
    def enrich(metric: Metric) -> EnrichedMetric:
        return {
            "hostname": hostname,
            "epoch": epoch(),
            "id": metric[0],
            "measure": metric[1],
        }

    return enrich
