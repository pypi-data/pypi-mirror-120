import unittest

from ghtrack.RequestInit import RequestInit


class RequestInitTest(unittest.TestCase):

    def setUp(self):
        self.req = RequestInit(token="token")

    def expect(self, url, parameters, input, status, responseHeaders, output):
        pass


