import unittest
from unittest.mock import MagicMock
from kafka_utils.send import get_topic_send


class TestMWriteFunctions(unittest.TestCase):
    def test_sender_is_callable(self):
        mock_send = MagicMock()
        send = get_topic_send("test", mock_send)
        self.assertTrue(callable(send))

    def test_send_to_topic(self):
        mock_send = MagicMock()
        send = get_topic_send("test_topic", mock_send)
        send("some data")
        mock_send.assert_called_once_with("test_topic", "some data")
