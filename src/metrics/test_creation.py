import unittest
import metrics.creation as metrics


class TestMetricFunctions(unittest.TestCase):
    def test_create_metric_function(self):
        fn = metrics.create_metric_function(
            "some.test", lambda: "metric value"
        )
        received = fn()
        self.assertEqual(("some.test", "metric value"), received)

    def test_create_metric_functions(self):
        fns = metrics.create_metric_functions(
            [
                ("metric.1", lambda: "metric.1.value"),
                ("metric.2", lambda: "metric.2.value"),
            ]
        )
        self.assertEqual(2, len(fns))
        received = [fn() for fn in fns]
        self.assertListEqual(
            [("metric.1", "metric.1.value"), ("metric.2", "metric.2.value")],
            received,
        )

    def test_enricher_is_callable(self):
        enrich = metrics.get_enricher()
        self.assertTrue(callable(enrich))

    def test_enricher_format(self):
        enrich = metrics.get_enricher("testHost", lambda: 1234)

        recevied = enrich(("test.metric", "test.measure"))

        self.assertDictEqual(
            {
                "hostname": "testHost",
                "epoch": 1234,
                "id": "test.metric",
                "measure": "test.measure",
            },
            recevied,
        )
