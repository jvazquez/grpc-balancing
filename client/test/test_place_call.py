import unittest

from application.client import ClientFactory
from protos.calculation_pb2 import PingRequest


class TestPlaceCall(unittest.TestCase):
    def test_assert_ping_has_response(self):
        ping_client = ClientFactory.get_client()
        response = ping_client.Ping(PingRequest())
        self.assertIsNotNone(response)
        self.assertTrue(len(response.message) > 0)
