import unittest
import metrics.writer as writer
from unittest.mock import MagicMock

_test_metric = ("test.metric", "test.value")


def _metric():
    return _test_metric


_metric_list = [_metric]


def raise_(msg: str) -> None:
    raise Exception(msg)


class TestMWriterFunctions(unittest.TestCase):
    def test_writer_is_callable(self):
        write = writer.get_writer(_metric_list, MagicMock(), MagicMock())
        self.assertTrue(callable(write))

    def test_writer_use_supplied_write(self):
        my_writer = MagicMock()

        write = writer.get_writer(_metric_list, my_writer, MagicMock())
        write()

        my_writer.assert_called_once()

    def test_writer_use_supplied_enricher(self):
        my_enrich = MagicMock()

        write = writer.get_writer(_metric_list, MagicMock(), my_enrich)
        write()

        my_enrich.assert_called_once_with(_test_metric)

    def test_write_enriched_value(self):
        my_write = MagicMock()
        my_enrich = MagicMock()
        my_enrich.return_value = "test"

        write = writer.get_writer(_metric_list, my_write, my_enrich)
        write()

        my_write.assert_called_once_with("test")

    def test_mutiple_metrics(self):
        my_writer = MagicMock()
        my_enricher = MagicMock()

        write = writer.get_writer([_metric, _metric], my_writer, my_enricher)
        write()

        self.assertEqual(2, my_enricher.call_count)
        self.assertEqual(2, my_writer.call_count)

    def test_broken_metrics(self):
        my_writer = MagicMock()
        my_enricher = MagicMock()

        write = writer.get_writer(
            [lambda: raise_("dead"), _metric], my_writer, my_enricher
        )
        write()

        my_writer.assert_called_once()
        my_enricher.assert_called_once()
