"""
MPD validation tests.

"""

import sys
import unittest
import logging
import glob
from lxml import etree

class TestDASH(unittest.TestCase):
    def setUp(self):
        self.log = logging.getLogger('TestLog')
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
        parser=etree.XMLParser(load_dtd=True, huge_tree=True, resolve_entities=True)


    def test_mpds(self):
        """ Test all MPDs found in the repository."""
        with open('../DASH-MPD.xsd', 'r') as schema_file:
            self.mpd_schema = etree.XMLSchema(etree.parse(schema_file, parser))
        for mpd_path in glob.glob('../*.mpd'):
            self.log.debug('Validating %s', mpd_path)
            with open(mpd_path) as mpd_file:
                with self.subTest(mpd=mpd_path):
                    mpd = etree.parse(mpd_file)
                    self.mpd_schema.assertValid(mpd)


    def test_mpps(self):
        """ Test all MPPs found in the repository."""
		with open('../DASH-MPD-PATCH.xsd', 'r') as schema_file:
            self.mpd_schema = etree.XMLSchema(etree.parse(schema_file, parser))
        for mpp_path in glob.glob('../*.mpp'):
            self.log.debug('Validating %s', mpp_path)
            with open(mpp_path) as mpp_file:
                with self.subTest(mpp=mpp_path):
                    mpp = etree.parse(mpp_file)
                    self.mpp_schema.assertValid(mpp)

if __name__ == '__main__':
    unittest.main()
