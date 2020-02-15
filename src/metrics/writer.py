import logging
from typing import Callable, List
from .creation import Enricher, EnrichedMetric, MetricCreator

Writer = Callable[[EnrichedMetric], None]

logger = logging.getLogger("metric.writer")


def get_writer(
    metric_creators: List[MetricCreator], write: Writer, enrich: Enricher
) -> Callable[[], None]:
    """returns a new writer
    Create a writer that will enrich the metric before writiting

    - param: writer: function that outputs the metric
    - param: enricher: function to Enrich the metric
    """

    def enriched_write() -> None:
        for fn in metric_creators:
            try:
                metric = fn()
                enrichedMetric = enrich(metric)
                write(enrichedMetric)
            except Exception:
                logging.exception("Error capturing metric %s", fn.__name__)

    return enriched_write
