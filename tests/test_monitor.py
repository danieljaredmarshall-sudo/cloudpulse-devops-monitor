import unittest
from unittest.mock import Mock, patch
from requests.exceptions import Timeout
from monitor import check_url


class MonitorTests(unittest.TestCase):
    @patch("monitor.requests.get")
    def test_healthy_site(self, get):
        get.return_value = Mock(status_code=200)
        result = check_url("https://example.com")
        self.assertEqual(result[4], 1)
        self.assertEqual(result[2], 200)

    @patch("monitor.requests.get")
    def test_server_error(self, get):
        get.return_value = Mock(status_code=503)
        self.assertEqual(check_url("https://example.com")[4], 0)

    @patch("monitor.requests.get", side_effect=Timeout("timed out"))
    def test_timeout(self, get):
        result = check_url("https://example.com")
        self.assertEqual(result[4], 0)
        self.assertIn("timed out", result[5])


if __name__ == "__main__":
    unittest.main()
