##
##

from unittest import TestCase

import json

from odcim import HostDBFromDcim

class TestHostDBFromDcim(TestCase):
    def setUp(self):
        with open('tests/data/dcim_devices.json') as f:
            self.devices = json.load(f)
        with open('tests/data/odcim_depts.json') as f:
            self.depts = json.load(f)

    def test_building_hostdb(self):
        hostdb = HostDBFromDcim(self.devices, self.depts)
        self.assertIn('ajna01', hostdb.keys())
