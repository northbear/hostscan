##

from helpers import parselastrows
from helpers import reducelastrows
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

class TestReduceLastRows(TestCase):
    def setUp(self):
        with open('tests/data/last.input') as f:
            self.testdata = f.read()
        self.rows = parselastrows(self.testdata)

    def test_reducerows(self):
        rows = reducelastrows(self.rows)
        self.assertEqual(2326, len(rows))


class TestParseLastRecord(TestCase):
    def setUp(self):
        with open('tests/data/last.input') as f:
            rows = parselastrows(f.read())
            reduced = reducelastrows(rows)
            self.testdata = reduced[0]

    def test_returns_dict(self):
        self.assertIsInstance(parselastrecord(''), dict)

    def test_contains_required_fields(self):
        rec = parselastrecord(self.testdata)
        self.assertSetEqual(set(rec.keys()), set(['user', 'console', 'from', 'logintime', 'duration']))

    def test_parse_simple_data(self):
        rec = parselastrecord(self.testdata)
        user, console, frm = rec['user'], rec['console'], rec['from'] 
        self.assertEqual((user, console, frm), ('boriska', 'pts/70', ':pts/110:S.1'))

    def test_parse_logintime(self):
        rec = parselastrecord(self.testdata)
        curr_year = datetime.now().year
        self.assertEqual(rec['logintime'], datetime(curr_year, 06, 19, 6, 4))
        # self.assertEqual(rec['logintime'], 'Mon Jun 19 06:04')

    

        
