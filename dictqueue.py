# -*- coding: utf-8 -*-
"""key-value dict queue
	1.just can set & get
	2.thread safe
	3.support block get
"""

import threading
import time


class Empty(Exception):
    pass


class Full(Exception):
    pass


class DictQueue(object):

	def __init__(self, dictqueue={}):
	    self.dictqueue = dictqueue
	    self.mutex = threading.Lock()
	    self.not_empty = threading.Condition(self.mutex)
	    self.not_full = threading.Condition(self.mutex)

	def get(self, key, block=True, timeout=None):
		self.not_empty.acquire()
		try:
			if not block:
				if not key in self.dictqueue:
					raise Empty
			elif timeout is None:
				while not key in self.dictqueue:
					self.not_empty.wait()
			else:
				endtime = time.time() + timeout
				while not key in self.dictqueue:
					remaining = endtime - time.time()
					if remaining <= 0.0:
						raise Empty
					self.not_empty.wait(remaining)
			value = self.dictqueue.pop(key)
			self.not_full.notify()
			return value
		finally:
			self.not_empty.release()

	def put(self, key, value, override=True, timeout=None):
		"""
		@param override: 是否覆写(针对值存在情况,值不存在情况不用管后面参数,直接存进去), False-不覆写一直阻塞,直到timeout才开始覆写, True-直接覆写
		"""
		self.not_full.acquire()
		try:
			if key in self.dictqueue:
				if not override:
					if timeout is None:
						raise Full
					else:
						endtime = time.time() + timeout
						while key in self.dictqueue:
							remaining = endtime - time.time()
							if remaining <= 0.0:
								break
							self.not_full.wait(remaining)
			self.dictqueue[key] = value
			self.not_empty.notify()
		finally:
			self.not_full.release()

	def has_value(self, key):
		self.mutex.acquire()
		r = key in self.dictqueue
		self.mutex.release()
		return r

if __name__ == "__main__":
	dq = DictQueue()
	dq.put("k", "xxxx", override=False, timeout=10)
	dq.put("k", "yyyy", override=False, timeout=10)
	print dq.get("k", block=True, timeout=10)
