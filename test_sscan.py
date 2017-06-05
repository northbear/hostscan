#!/usr/bin/env python 

import unittest

from sscan import DcimApi

class TestingDcimApi(unittest.TestCase):
    def test_DcimApi(self):
        dcim = DcimApi()
        self.assertIsInstance(dcim, DcimApi, "wrong instance of DcimApi")

