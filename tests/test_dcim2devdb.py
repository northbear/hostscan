##
##

from unittest import TestCase

import json

from dcim2devdb import HostDBFromDcim
from hostdb import HostDB

class TestHostDBFromDcim(TestCase):
    def setUp(self):
        with open('tests/data/dcim_devices.json') as f:
            self.devices = json.load(f)
        with open('tests/data/dcim_depts.json') as f:
            self.depts = json.load(f)
        self.devdb = HostDBFromDcim(self.devices, self.depts)

    def test_dictionaries(self):
        self.assertEqual(set(['owner']), set(self.devdb.dictionaries.keys()))

    def test_owner_dictionaries(self):
        self.assertIn('owner', set(self.devdb.dictionaries.keys()))

    def test_produce_devdb(self):
        devdb = HostDB()
        self.devdb.produce(devdb)
        self.assertIn('ajna01', devdb.keys())


class TestDCimToHostDBRec(TestCase):
    def setUp(self):
        with open('tests/data/dcim_devices.json') as f:
            self.devices = json.load(f)
        with open('tests/data/dcim_depts.json') as f:
            self.depts = json.load(f)
        self.devdb = HostDBFromDcim(self.devices, self.depts)

    def test_return_dict(self):
        result = self.devdb.makerec(self.devices[2], self.devdb.dictionaries)
        self.assertIsInstance(result, dict)

    def test_rec_has_fields(self):
        result = self.devdb.makerec(self.devices[2], self.devdb.dictionaries)
        self.assertEqual(set(['host', 'owner', 'type']), set(result.keys())) 
        
    def test_rec_store_owner(self):
        result = self.devdb.makerec(self.devices[2], self.devdb.dictionaries)
        self.assertEqual(result['owner'], 'SHArP') 
        
    def test_rec_store_host(self):
        result = self.devdb.makerec(self.devices[2], self.devdb.dictionaries)
        self.assertEqual(result['host'], 'ajna01') 
        
    def test_rec_store_type(self):
        result = self.devdb.makerec(self.devices[2], self.devdb.dictionaries)
        self.assertEqual(result['type'], 'server') 
        

