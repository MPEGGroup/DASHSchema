"""
MPD valication tests.

"""

import sys
import unittest
import logging
import glob
from lxml import etree
from lxml import isoschematron

class TestStringMethods(unittest.TestCase):
    def setUp(self):
        self.log = logging.getLogger('TestLog')
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
        with open('../DASH-MPD.xsd', 'r') as schema_file:
            self.mpd_schema = etree.XMLSchema(etree.parse(schema_file))
            
    def test_MPDs(self):
        i = 0
        for mpd_path in glob.glob('../*.mpd'):
            i += 1
            self.log.debug('Validating %s', mpd_path)
            with open(mpd_path) as mpd_file:
                with self.subTest(i=i):
                    mpd = etree.parse(mpd_file)
                    self.assertTrue(self.mpd_schema.validate(mpd))


if __name__ == '__main__':
    unittest.main()
