##
##

from helpers import parselastrows
from helpers import reducelastrows
from helpers import parselastrecord, getstat, stat2string, trimelderrecs

from unittest import TestCase
from datetime import datetime, timedelta

class TestParseLastRows(TestCase):
    def setUp(self):
        with open('tests/data/last_new.input') as f:
            self.testdata = f.read()

    def test_return_list(self):
        self.assertIsInstance(parselastrows(''), list)

    def test_amount_of_record_loading(self):
        outp = parselastrows(self.testdata)
        self.assertEqual(3153, len(outp))

class TestReduceLastRows(TestCase):
    def setUp(self):
        with open('tests/data/last_new.input') as f:
            self.testdata = f.read()
        self.rows = parselastrows(self.testdata)

    def test_reducerows(self):
        rows = reducelastrows(self.rows)
        # for r in rows:
        #     print r
        self.assertEqual(3073, len(rows))


class TestParseLastRecord(TestCase):
    def setUp(self):
        with open('tests/data/last_new.input') as f:
            rows = parselastrows(f.read())
            reduced = reducelastrows(rows)
            self.testdata = 'eugene   pts/51       Sun Jun 25 08:37:59 2017 - Sun Jun 25 18:01:21 2017  (09:23)'
            self.testdata_gt_day = 'amirse   pts/103      Wed Jun 21 10:19:49 2017 - Sun Jun 25 17:11:31 2017 (4+06:51)'
            self.testdata_lt_day = self.testdata
            self.testdata_sboot = rows[2102]

    # def test_returns_dict(self):
    #     self.assertIsInstance(parselastrecord(''), dict)

    def test_contains_required_fields(self):
        rec = parselastrecord(self.testdata)
        self.assertSetEqual(set(rec.keys()), set(['user', 'console', 'logintime', 'duration']))

    def test_parse_simple_data(self):
        rec = parselastrecord(self.testdata)
        user, console = rec['user'], rec['console'] 
        self.assertEqual((user, console), ('eugene', 'pts/51'))

    # def test_parse_sboot_record(self):
    #     rec = parselastrecord(self.testdata_sboot)
    #     user, console = rec['user'], rec['console'] 
    #     self.assertEqual((user, console), ('reboot', 'system boot'))

    def test_parse_logintime(self):
        rec = parselastrecord(self.testdata)
        self.assertEqual(rec['logintime'], datetime(2017, 6, 25, 8, 37, 59))

    def test_parse_duration_gt_day(self):
        rec = parselastrecord(self.testdata_gt_day)
        self.assertEqual(rec['duration'], timedelta(4, 0, 0, 0, 51, 6))

    def test_parse_duration_lt_day(self):
        rec = parselastrecord(self.testdata_lt_day)
        self.assertEqual(rec['duration'], timedelta(0, 0, 0, 0, 23, 9))

       
class TestLastGetStat(TestCase):
    def setUp(self):
        self.db, rows = [], []
        with open('tests/data/last_new.input') as f:
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
        self.assertEqual(stat[0], {'user': 'root', 'amount': 127, 'duration': timedelta(1, 14940)})

    def test_otherstat(self):
        stat = getstat(self.db)
        self.assertEqual(stat[1], {'user': 'others', 'amount': 2946, 'duration': timedelta(805, 4740)})

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
        with open('tests/data/last_new.input') as f:
            rows = parselastrows(f.read())
        reduced = reducelastrows(rows)
        for row in reduced:
            self.recs.append(parselastrecord(row))
        self.curr_data = self.recs[0]['logintime']
        self.olderdate = datetime(2017, 6, 12, 0, 0, 0)

    def test_trim_old_records(self):
        # days = 10
        # date = 'Jun 27 14:15:27 2017'
        # date = datetime(2017, 6, 27, 14, 15, 27)
        trimmed = trimelderrecs(self.recs, self.olderdate) 
        self.assertGreater(trimmed[-1]['logintime'], self.olderdate)
