# -*- coding: utf-8 -*-

import unittest

from pglet import PPool

import logging
logger = logging.getLogger(__name__)


class PgletTestCase(unittest.TestCase):
    
    def setUp(self):
        logging.basicConfig(level=logging.DEBUG, format='[%(asctime)-15s %(levelname)s:%(module)s] %(message)s')
        ppool = PPool(2)
        self._ppool = ppool
        self._ppool.init()
        self._task_func = lambda x : x

    def test_spawn(self):
        ppool = self._ppool
        task_func = self._task_func
        
        future = ppool.spawn(task_func, 1)
        self.assertIsNotNone(future)
        self.assertEqual(future.get(), 1)
        
    def test_spawn_sub(self):
        ppool = self._ppool
        task_func = self._task_func
        
        result = ppool.spawn(task_func, 1)
        self.assertIsNone(result)
        
if __name__ == "__main__":
    unittest.main()        
