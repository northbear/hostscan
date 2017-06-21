##
##

from helpers import parselastrows
from helpers import reducelastrows
from helpers import parselastrecord, getstat, stat2string, trimelderrecs

from unittest import TestCase
from datetime import datetime, timedelta

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
        self.assertEqual(2325, len(rows))


class TestParseLastRecord(TestCase):
    def setUp(self):
        with open('tests/data/last.input') as f:
            rows = parselastrows(f.read())
            reduced = reducelastrows(rows)
            self.testdata = reduced[247]
            self.testdata_gt_day = reduced[247]
            self.testdata_lt_day = reduced[0]
            self.testdata_sboot = rows[2102]

    def test_returns_dict(self):
        self.assertIsInstance(parselastrecord(''), dict)

    def test_contains_required_fields(self):
        rec = parselastrecord(self.testdata)
        self.assertSetEqual(set(rec.keys()), set(['user', 'console', 'from', 'logintime', 'duration']))

    def test_parse_simple_data(self):
        rec = parselastrecord(self.testdata)
        user, console, frm = rec['user'], rec['console'], rec['from'] 
        self.assertEqual((user, console, frm), ('yosefe', 'pts/93', 'hpchead-old.mtr.'))

    def test_parse_sboot_record(self):
        rec = parselastrecord(self.testdata_sboot)
        user, console, frm = rec['user'], rec['console'], rec['from'] 
        self.assertEqual((user, console, frm), ('reboot', 'system boot', '3.10.0-327.el7.x'))

    def test_parse_logintime(self):
        rec = parselastrecord(self.testdata)
        curr_year = datetime.now().year
        self.assertEqual(rec['logintime'], datetime(curr_year, 6, 16, 13, 38))

    def test_parse_duration_gt_day(self):
        rec = parselastrecord(self.testdata_gt_day)
        self.assertEqual(rec['duration'], timedelta(1, 0, 0, 0, 52, 2))

    def test_parse_duration_lt_day(self):
        rec = parselastrecord(self.testdata_lt_day)
        self.assertEqual(rec['duration'], timedelta(0, 0, 0, 0, 39, 1))

       
class TestLastGetStat(TestCase):
    def setUp(self):
        self.db, rows = [], []
        with open('tests/data/last.input') as f:
            rows = reducelastrows(parselastrows(f.read()))
        for item in rows:
            try:
                self.db.append(parselastrecord(item))
            except ValueError:
                print item, rows.index(item)
        
    def test_getlist(self):
        stat = getstat(self.db)
        self.assertIsInstance(stat, list)

    def test_rootstat(self):
        stat = getstat(self.db)
        self.assertEqual(stat[0], {'user': 'root', 'amount': 76, 'duration': timedelta(1, 14940)})

    def test_otherstat(self):
        stat = getstat(self.db)
        self.assertEqual(stat[1], {'user': 'others', 'amount': 2249, 'duration': timedelta(576, 4860)})

class TestStat2String(TestCase):
    def setUp(self):
        self.user_root = { 'user': 'root', 'amount': 10, 'duration': timedelta(0, 600)}
        self.user_others = { 'user': 'others', 'amount': 300, 'duration': timedelta(0, 19830)}
        # self.teststat = [user_root, user_others]
    
    def test_single_row_string(self):
        self.assertEqual(stat2string([self.user_root]), "root:10|0:10:00")

    def test_multiple_row_string(self):
        self.assertEqual(stat2string([self.user_root, self.user_others]), "root:10|0:10:00;others:300|5:30:30")

class TestTrimRows(TestCase):
    def setUp(self):
        rows, self.recs = [], []
        with open('tests/data/last.input') as f:
            rows = parselastrows(f.read())
        reduced = reducelastrows(rows)
        for row in reduced:
            self.recs.append(parselastrecord(row))
        self.curr_data = self.recs[0]['logintime']

    def test_trim_old_records(self):
        days = 10
        trimmed = trimelderrecs(self.recs, days) 
        self.assertGreater(trimmed[-1]['logintime'], self.curr_data - timedelta(days))
