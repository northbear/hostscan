##

from catchinfo import HostHCAs

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


