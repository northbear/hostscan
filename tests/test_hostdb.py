##
##

from unittest import TestCase

import json

from hostdb import HostDB
from hostdb import dict_in

class TestHostDB(TestCase):
    def setUp(self):
        self.jsn_fname = 'tests/data/hostdb_json.input'

    def test_load_by_filename(self):
        hostdb = HostDB(self.jsn_fname)
        self.assertIn('hpchead', hostdb.keys())

    def test_load_by_file(self):
        with open(self.jsn_fname) as f:
            hostdb = HostDB(f)
        self.assertIn('hpchead', hostdb.keys())
        
    def test_load_by_hostlist(self):
        hostlist = ['host1', 'host2']
        hostdb = HostDB(hostlist)
        self.assertIn('host2', hostdb.keys())


    def test_init_by_dict(self):
        dct = {'hostname': { 'field': 'content' } }
        hostdb = HostDB(dct)
        self.assertEqual(hostdb, dct)

    def test_select(self):
        hostdb = HostDB(self.jsn_fname)
        query = { 'owner': 'HPC'}
        selected = hostdb.select(query)
        self.assertIsInstance(selected, HostDB)
        self.assertIn('hpchead', selected.keys()) 
        

class TestDictIn(TestCase):
    def setUp(self):
        self.sample = { 'key1': 'value1', 'key2': 'value2', 'key3': 'value3', 'key4': 'value4' }
        self.subset = { 'key2': 'value2', 'key3': 'value3' }
        self.other = { 'other1': 'value1' }
        self.other_value = { 'key2': 'value2', 'key3': 'other_value' }
        self.wrongval = 10

    def test_false_on_wrong_param(self):
        self.assertFalse(dict_in(self.wrongval, self.sample))
        self.assertFalse(dict_in(self.sample, self.wrongval))

    def test_with_other_false(self):
        self.assertFalse(dict_in(self.other, self.sample))

    def test_with_other_value_false(self):
        self.assertFalse(dict_in(self.other_value, self.sample))

    def test_subset_true(self):
        self.assertTrue(dict_in(self.subset, self.sample))

