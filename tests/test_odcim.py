##
##

from unittest import TestCase

import json

from odcim import HostDBFromDcim

class TestHostDBFromDcim(TestCase):
    def setUp(self):
        with open('tests/data/dcim_devices.json') as f:
            self.devices = json.load(f)
        with open('tests/data/dcim_depts.json') as f:
            self.depts = json.load(f)
        self.hostdb = HostDBFromDcim(self.devices, self.depts)

    def test_building_hostdb(self):
        self.assertIn('ajna01', self.hostdb.keys())

    def test_dictionaries(self):
        self.assertEqual(set(['owner']), set(self.hostdb.dictionaries.keys()))

    def test_owner_dictionaries(self):
        self.assertIn('owner', set(self.hostdb.dictionaries.keys()))


class TestDCimToHostDBRec(TestCase):
    def setUp(self):
        with open('tests/data/dcim_devices.json') as f:
            self.devices = json.load(f)
        with open('tests/data/dcim_depts.json') as f:
            self.depts = json.load(f)
        self.hostdb = HostDBFromDcim(self.devices, self.depts)

    def test_return_dict(self):
        result = self.hostdb.makerec(self.devices[2], self.hostdb.dictionaries)
        self.assertIsInstance(result, dict)

    def test_rec_has_fields(self):
        result = self.hostdb.makerec(self.devices[2], self.hostdb.dictionaries)
        print result
        self.assertEqual(set(['host', 'owner', 'type']), set(result.keys())) 
        
    def test_rec_store_owner(self):
        result = self.hostdb.makerec(self.devices[2], self.hostdb.dictionaries)
        self.assertEqual(result['owner'], 'SHArP') 
        
    def test_rec_store_host(self):
        result = self.hostdb.makerec(self.devices[2], self.hostdb.dictionaries)
        self.assertEqual(result['host'], 'ajna01') 
        
    def test_rec_store_type(self):
        result = self.hostdb.makerec(self.devices[2], self.hostdb.dictionaries)
        self.assertEqual(result['type'], 'server') 
        

