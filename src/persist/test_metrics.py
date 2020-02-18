import datetime
import unittest
import persist.database as pdb
from peewee import SqliteDatabase
from persist.metrics import write_gauge


class TestMWriteFunctions(unittest.TestCase):
    def setUp(self):
        self.db = SqliteDatabase(":memory:")
        pdb.set_database(self.db)

    def tearDown(self):
        self.db.close()

    def test_write_guage(self):
        write_gauge(
            {
                "hostname": "test",
                "id": "test.metric",
                "epoch": 0,
                "measure": 12.3,
            }
        )
        self.assertEqual("test", pdb.Host.get_or_none(id=1).name)
        self.assertEqual("test.metric", pdb.Metric.get_or_none(id=1).name)
        gauge = pdb.Gauge.get_or_none(id=1, host=1, metric=1)
        self.assertEqual(
            datetime.datetime(1970, 1, 1, 0, 0), gauge.created_date
        )
        self.assertEqual(12.3, gauge.measure)

    def test_epoch(self):
        write_gauge(
            {
                "hostname": "test",
                "id": "test.metric",
                "epoch": 1581949143000,
                "measure": 12.3,
            }
        )
        gauge = pdb.Gauge.get_or_none(id=1, host=1, metric=1)
        self.assertEqual(
            datetime.datetime(2020, 2, 17, 14, 19, 3), gauge.created_date
        )
        self.assertEqual(12.3, gauge.measure)
