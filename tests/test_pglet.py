# -*- coding: utf-8 -*-

import unittest

from pglet import PPool
import gevent

import logging
logger = logging.getLogger(__name__)


def task_func(x):
    return x
    
    
class PgletTestCase(unittest.TestCase):
        
    def setUp(self):
        logging.basicConfig(level=logging.DEBUG, format='[%(asctime)-15s %(levelname)s:%(module)s] %(message)s')
        ppool = PPool(2)
        self._ppool = ppool
        self._ppool.init()
        
        gevent.spawn(gevent.sleep, 5).join()

    def test_spawn(self):
        ppool = self._ppool
        
        future = ppool.spawn(task_func, 1)
        self.assertIsNotNone(future)
        self.assertEqual(future.get(), 1)
        
    def test_spawn_sub(self):
        ppool = self._ppool
        
        result = ppool.spawn_sub(task_func, 1)
        self.assertIsNone(result)
        
    def tearDown(self):
        ppool = self._ppool
        ppool.close()
        
if __name__ == "__main__":
    unittest.main()        
