##

from catchinfo import HostHCAs, HostUsers

from unittest import TestCase


class TestHostHCAs(TestCase):
    def setUp(self):
        self.hosthcas = HostHCAs('hostname', {})
        with open('tests/data/hosthca_postprocess.input') as f:
            self.input = f.read()

    def test_postrocess_return_fields(self):
        resp = self.hosthcas.postprocess(self.input)
        self.assertEqual(set(resp.keys()), set(['hcas']))

    def test_postrocess_return_values(self):
        resp = self.hosthcas.postprocess(self.input)
        self.assertEqual(resp['hcas'], 'MT4103;MT4115;MT4115;MT4118;MT4118;MT4115')


class TestHostUsers(TestCase):
    def setUp(self):
        self.hostlast = HostUsers('hostname', {})
        with open('tests/data/last_new.input') as f:
            self.input = f.read()
            
    def test_querystr(self):
        tq, sq = self.hostlast.querystr() 
        self.assertEqual(sq, 'last -FR')

    def test_postprocess_returns_dict(self):
        resp = self.hostlast.postprocess('')
        self.assertIsInstance(resp, dict) 
        
    def test_postprocess_fields(self):
        resp = self.hostlast.postprocess('')
        self.assertIn('user_activity', set(resp.keys())) 
        
    def test_postprocess_content(self):
        resp = self.hostlast.postprocess(self.input)
        self.assertEqual(resp['user_activity'], 'root:0|0:00:00;others:289|56 days, 15:35:00')

