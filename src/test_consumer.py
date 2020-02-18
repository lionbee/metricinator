import json
import sys
import unittest
from unittest.mock import patch, MagicMock


sys.modules["consumer_config"] = MagicMock(log_level=100)
from consumer import consume_metrics  # noqa E402


class TestMWriteFunctions(unittest.TestCase):
    def test_loop_exits(self):
        consumer = MagicMock()
        consumer.__iter__.return_value = []
        db = MagicMock()
        consume_metrics(consumer=consumer, db=db)
        db.close.assert_called_once()

    @patch("consumer.set_database")
    def test_set_database(self, mock_set_database):
        consumer = MagicMock()
        consumer.__iter__.return_value = []
        db = MagicMock()
        consume_metrics(consumer=consumer, db=db)
        mock_set_database.assert_called_once_with(db)

    @patch("consumer.write_gauge")
    def test_write_gauge(self, mock_write_gauge):
        test_metric = {"some": "value"}
        test_message = MagicMock(value=json.dumps(test_metric))
        consumer = MagicMock()
        consumer.__iter__.return_value = [test_message]
        db = MagicMock()
        consume_metrics(consumer=consumer, db=db)
        mock_write_gauge.assert_called_once_with(test_metric)
