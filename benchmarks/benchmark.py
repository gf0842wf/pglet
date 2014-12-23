import sys; sys.modules.pop("threading", None)
from gevent import monkey; monkey.patch_all()
from pglet import PPool
import gevent
import urllib2
import time

urls = ["http://www.baidu.com"] * 100

def fetch_20(url):
    return urllib2.urlopen(url).read(20)
    
ppool = PPool(2)
ppool.init()

t0 = time.time()
ppool._benchmark_join_start(fetch_20, urls)
ppool._benchmark_join_end()
print time.time() - t0

gevent.wait()