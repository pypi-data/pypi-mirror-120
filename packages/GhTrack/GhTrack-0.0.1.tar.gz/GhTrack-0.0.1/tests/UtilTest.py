import unittest

from ghtrack.Util import Util


class UtilTest(unittest.TestCase):

    def test_is_not_blank(self):
        self.assertFalse(Util.is_not_blank(""), msg="it should be true")
        self.assertTrue(Util.is_not_blank("tests"), msg="tests is not blank")

    def testOneWeekOld(self):
        post = "2014-06-06T22:56:04Z"
        self.assertFalse(Util.oneWeekOld(post))
