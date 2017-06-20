##
##

from unittest import TestCase

from hostdb import HostDB


class TestHostDB(TestCase):
    def setUp(self):
        self.jsn_fname = 'tests/data/hostdb_json.input'

    def test_load_by_filename(self):
        hostdb = HostDB(self.jsn_fname)
        self.assertIn('hpchead', hostdb.db.keys())

    def test_load_by_file(self):
        with open(self.jsn_fname) as f:
            hostdb = HostDB(f)
        self.assertIn('hpchead', hostdb.db.keys())
        
    def test_load_by_hostlist(self):
        hostlist = ['host1', 'host2']
        hostdb = HostDB(hostlist)
        self.assertIn('host2', hostdb.db.keys())
        
