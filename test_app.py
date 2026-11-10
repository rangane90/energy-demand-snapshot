import json
import threading
import unittest
from urllib.error import HTTPError
from urllib.request import urlopen

from app import make_server


class DemandApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        server = make_server("127.0.0.1", 0)
        cls.addClassCleanup(server.server_close)
        thread = threading.Thread(target=server.serve_forever)
        thread.start()
        cls.addClassCleanup(thread.join)
        cls.addClassCleanup(server.shutdown)
        cls.base_url = f"http://127.0.0.1:{server.server_port}"

    def get_json(self, path):
        with urlopen(self.base_url + path, timeout=3) as response:
            self.assertEqual(response.status, 200)
            self.assertEqual(response.headers.get_content_type(), "application/json")
            return json.load(response)

    def test_health(self):
        self.assertEqual(self.get_json("/health"), {"status": "ok"})

    def test_summary(self):
        self.assertEqual(self.get_json("/summary"), {
            "data_source": "synthetic",
            "samples": 8,
            "average_mw": 490,
            "peak_mw": 720,
        })

    def test_unknown_route(self):
        with self.assertRaises(HTTPError) as result:
            self.get_json("/missing")
        with result.exception as response:
            self.assertEqual(response.code, 404)
            self.assertEqual(json.load(response), {"error": "not found"})


if __name__ == "__main__":
    unittest.main()
