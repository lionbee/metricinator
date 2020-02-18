import sys
import unittest
from unittest.mock import patch, MagicMock


sys.modules["producer_config"] = MagicMock(log_level=100)
from producer import produce_metrics  # noqa E402


def get_mock_sleep(iter=1, throws=KeyboardInterrupt):
    count = iter

    def sleep(*args):
        nonlocal count
        count -= 1
        if count == 0:
            raise throws()
        return None

    return sleep


class TestMWriteFunctions(unittest.TestCase):
    @patch("time.sleep", side_effect=[KeyboardInterrupt()])
    def test_loop_exits(self, mock_sleep):
        mock_metric_writer = MagicMock()
        mock_shutdown = MagicMock()
        produce_metrics(
            metric_writer=mock_metric_writer,
            interval_seconds=1,
            shutdown=mock_shutdown,
        )
        mock_metric_writer.assert_called_once()
        mock_shutdown.assert_called_once()

    @patch("time.sleep", side_effect=[None, None, KeyboardInterrupt()])
    def test_loop_multiple(self, mock_sleep):
        mock_metric_writer = MagicMock()
        mock_shutdown = MagicMock()
        produce_metrics(
            metric_writer=mock_metric_writer,
            interval_seconds=1,
            shutdown=mock_shutdown,
        )
        self.assertEqual(3, mock_metric_writer.call_count)
        mock_shutdown.assert_called_once()

    @patch("time.sleep", side_effect=[KeyboardInterrupt()])
    def test_sleep_interval(self, mock_sleep):
        produce_metrics(interval_seconds=123)
        mock_sleep.assert_called_once_with(123)
