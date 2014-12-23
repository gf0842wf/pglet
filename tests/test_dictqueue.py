# -*- coding: utf-8 -*-

import sys; sys.modules.pop("threading", None)
from gevent import monkey; monkey.patch_all()
import unittest

from pglet import DictQueue
import gevent

import logging
logger = logging.getLogger(__name__)


class DictQueueTestCase(unittest.TestCase):
        
    def setUp(self):
        logging.basicConfig(level=logging.DEBUG, format='[%(asctime)-15s %(levelname)s:%(module)s] %(message)s')
        dictqueue = DictQueue()
        self._dictqueue = dictqueue
        
        gevent.spawn(gevent.sleep, 10).join()

    def test_multi_greenlet(self):
        dictqueue = self._dictqueue
        gevent.spawn_later(2, dictqueue.put, "k1", "v1", override=True)
        v1 = dictqueue.pop("k1", block=True, timeout=None)
        self.assertEqual(v1, "v1")
        
        gevent.spawn_later(4, dictqueue.put, "k2", "v2", override=True)
        g2 = gevent.spawn_later(3, dictqueue.pop, "k2", block=True, timeout=None)
        self.assertEqual(g2.get(), "v2")
        
    def tearDown(self):
        pass
    
        
if __name__ == "__main__":
    unittest.main()        
