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