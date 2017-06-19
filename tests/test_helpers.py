##

from helpers import parselastrows
from helpers import parselastrecord

from unittest import TestCase
from datetime import datetime

class TestParseLastRows(TestCase):
    def setUp(self):
        with open('tests/data/last.input') as f:
            self.testdata = f.read()

    def test_return_list(self):
        self.assertIsInstance(parselastrows(''), list)

    def test_amount_of_record_loading(self):
        outp = parselastrows(self.testdata)
        self.assertEqual(2366, len(outp))

class TestParseLastRecord(TestCase):
    def setUp(self):
        with open('tests/data/last.input') as f:
            self.testdata = f.readline()

    def test_returns_dict(self):
        self.assertIsInstance(parselastrecord(''), dict)

    def test_contains_required_fields(self):
        rec = parselastrecord(self.testdata)
        self.assertSetEqual(set(rec.keys()), set(['user', 'console', 'from', 'logintime', 'duration']))

    def test_parse_simple_data(self):
        rec = parselastrecord(self.testdata)
        user, console, frm = rec['user'], rec['console'], rec['from'] 
        self.assertEqual((user, console, frm), ('alinas', 'pts/124', '10.223.3.114'))

    def test_parse_logintime(self):
        rec = parselastrecord(self.testdata)
        # print self.testdata
        self.assertEqual(rec['logintime'], 'Mon Jun 19 09:44')



        
