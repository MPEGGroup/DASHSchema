"""
MPD validation tests.

"""

import sys
import unittest
import logging
import glob
import requests
from lxml import etree


class PrefixResolver(etree.Resolver):
    # https://lxml.de/resolvers.html
    def __init__(self, prefix):
        self.prefix = prefix.lower()

    def resolve(self, url, pubid, context):
        if url.lower().startswith(self.prefix):
            res=requests.get(url, allow_redirects=True)
            return self.resolve_string(res.text, context)
	  
	  
class TestDASH(unittest.TestCase):
    def setUp(self):
        self.log = logging.getLogger('TestLog')
        logging.basicConfig(stream=sys.stderr, level=logging.INFO)
        self.parser=etree.XMLParser(load_dtd=True, no_network=False, huge_tree=True, resolve_entities=True)
        self.parser.resolvers.add(PrefixResolver("https"))
        self.parser.resolvers.add(PrefixResolver("http"))

    def test_mpds(self):
        """ Test all MPDs found in the repository."""
        with open('../DASH-MPD.xsd', 'r') as schema_file:
            mpd_schema = etree.XMLSchema( etree.parse(schema_file, self.parser) )
        for mpd_path in glob.glob('../*.mpd'):
            self.log.info('Validating %s', mpd_path)
            with open(mpd_path) as mpd_file:
                with self.subTest(mpd=mpd_path):
                    mpd_schema.assertValid( etree.parse(mpd_file) )


    def test_mpps(self):
        """ Test all MPPs found in the repository."""
        with open('../DASH-MPD-PATCH.xsd', 'r') as mpp_schema_file:
            mpp_schema = etree.XMLSchema( etree.parse(mpp_schema_file, self.parser) )		
        for mpp_path in glob.glob('../*.mpp'):
            self.log.info('Validating %s', mpp_path)
            with open(mpp_path) as mpp_file:
                with self.subTest(mpp=mpp_path):
                    mpp_schema.assertValid( etree.parse(mpp_file) )

if __name__ == '__main__':
    unittest.main()
