from urllib.request import Request, urlopen
from urllib.parse import urlencode
from urllib.error import URLError, HTTPError
from html.parser import HTMLParser
from re import compile

from setux.targets import Local


class Parser(HTMLParser):
    packages = dict()
    name = None
    attr = None

    def handle_starttag(self, tag, attrs):
        if tag=='span':
            attrs = dict(attrs)
            cls = attrs.get('class')
            if cls=='package-snippet__name':
                self.attr = 'name'
            elif cls=='package-snippet__version':
                self.attr = 'version'

    def handle_data(self, value):
        if self.attr=='name':
            value = value.strip()
            if value:
                self.name = value
        elif self.name and self.attr=='version':
            self.packages[self.name] = value.strip()
            self.name = None


class Pypi:
    def __init__(self, pip):
        self.pip = pip

    def cache(self):
        local = Local(outdir=self.pip.cache_dir)
        url = 'https://pypi.org/simple'
        org = f'{self.pip.cache_dir}/pypi.simple'
        local.download(url=url, dst=org)
        pat = compile(r'^.*?<a href="/simple/.*?/">(?P<name>.*?)</a>')
        with open(self.pip.cache_file, 'w') as out:
            for line in open(org):
                try:
                    name = pat.search(line).groupdict()['name']
                    out.write(f'{name} -\n')
                except AttributeError: pass
        local.file(org).rm()

    def search(self, pattern):
        url = "https://pypi.org/search"
        query = urlencode({'q':pattern})

        req = Request(url+'?'+query)
        try:
            rsp = urlopen(req)
        except HTTPError as x:
            print('HTTP Error code: ', x.code)
        except URLError as x:
            print('URL ERROR Reason: ', x.reason)
        else:
            html = rsp.read().decode('utf-8')

        parser = Parser()
        parser.feed(html)
        items = parser.packages.items()

        yield from sorted(items)
