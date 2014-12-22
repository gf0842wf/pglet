import sys; sys.modules.pop("threading", None)
from gevent import monkey; monkey.patch_all()
import gevent
import urllib2
import time

urls = ["http://www.baidu.com"] * 100

def fetch_20(url):
    return urllib2.urlopen(url).read(20)

t0 = time.time()
[ gevent.spawn(fetch_20, url).get() for url in urls ]
print time.time() - t0

gevent.wait()