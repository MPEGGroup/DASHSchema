"""
evaluate manifests from other organisations against the MPEG DASH schema

developed by Paul Higgs using Python 3.9.1
uses the following libraries
 * requests,    python -m pip install requests
 * lxml,        python -m pip install lxml

"""

import sys
import unittest
import logging
import glob
import requests
import json

from lxml import etree

DVBManifestsFile="DVB-manifests.json"
HbbTVManifestsFile="HbbTV-manifests.json"
MPEGCMAFManifestsFile="MPEG-CMAF-manifests.json"
DASHIFManifestsFile="DASH-IF-Manifests.json"

DASHIF_dataset_url = "https://raw.githubusercontent.com/Dash-Industry-Forum/Test-Assets-Dataset-Public/master/dataset/data/testvector.json"


class TestManifests(unittest.TestCase):
	def setUp(self):
		self.log = logging.getLogger('MDP_tests')
		logging.basicConfig(stream=sys.stderr, level=logging.INFO)
		self.log.info('Loading MPEG DASH schema')
		self.xsdParser=etree.XMLParser(load_dtd=True, huge_tree=True, resolve_entities=True)
		with open('../DASH-MPD.xsd', 'r') as schema_file:
			self.mpd_schema = etree.XMLSchema(etree.parse(schema_file, self.xsdParser))
#		is_python3 = sys.version_info.major == 3
		self.xmlParser=etree.XMLParser(load_dtd=True, huge_tree=True, resolve_entities=True)

	def check_a_manifest(self, mpdURL, source):
		with self.subTest(msg=mpdURL):		
			self.log.info('Validating {%s} %s', source, mpdURL)	
			try:
				mpdRequest=requests.get(mpdURL, allow_redirects=True)	
			except Exception as err:
				self.fail(err)
			else:
				self.assertEqual(mpdRequest.status_code, 200, "Request error; expected 200, got %d" % mpdRequest.status_code)
				if mpdRequest.status_code == 200:
					mpd=etree.fromstring((mpdRequest.text).encode('utf8'), self.xmlParser)
					if not self.mpd_schema.validate(mpd):
						self.fail(self.mpd_schema.error_log.filter_from_errors())

	def loadDatasetURL(self, url):
		result=[]
		response=requests.get(url, allow_redirects=True)
		dataset=json.loads(response.text)
		for item in dataset:
			if "url" in item:
				result.append(item["url"])
		return result

	def loadDatasetFile(self, filename):
		result=[]
		with open(filename, 'r') as manifest_file:
			dataset=json.load(manifest_file)
			for item in dataset:
				if "url" in item:
					result.append(item["url"])
		return result

	def check_manifests(self, mpdList, source):
		for mpdURL in mpdList:
			self.check_a_manifest(mpdURL, source)


	def test_DVB(self):
		self.check_manifests(self.loadDatasetFile(DVBManifestsFile), "DVB")

	def test_HbbTV(self):
		self.check_manifests(self.loadDatasetFile(HbbTVManifestsFile), "HbbTV")

	def test_MPEG_CMAF(self):
		self.check_manifests(self.loadDatasetFile(MPEGCMAFManifestsFile), "MPEG CMAF")
		
	def test_DASH_IF_list(self):
		self.check_manifests(self.loadDatasetFile(DASHIFManifestsFile), "DASH-IF Local List")
				
	def test_DASH_IF_dataset(self):
		self.check_manifests(self.loadDatasetURL(DASHIF_dataset_url), "DASH-IF Dataset")
	
#	def test_one(self):
#		mpd="http://html5.cablelabs.com:8100/cenc/prwv/dash.mpd"
#		self.check_a_manifest(mpd, "debugging1")
		
if __name__ == '__main__':
    unittest.main()
