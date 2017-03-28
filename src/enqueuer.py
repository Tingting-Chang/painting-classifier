#!/usr/bin/env python
import os, sys, time

from concurrent.futures import ThreadPoolExecutor
from threading import RLock

class Enqueuer(object):
    def __init__(self, generator, workers = 8, max_q_size = 16,
            wait_time = 0.05):
        self.generator = generator
        self.workers = workers
        self.max_q_size = max_q_size
        #self.num_batches = generator.n_batches()
        #self.epoch = 0
        self.lock = RLock()
        self.executor = None
        self.queue = []
        #self.submitted = 0
        self.wait_time = wait_time

    def start(self):
        with lock:
            if self.executor is not None:
                self.executor.shutdown(wait = False)
            self.executor = ThreadPoolExecutor(max_workers = self.workers)
            #self.epoch = 0
            self._submit_to_queue()

    def __iter__(self):
        return self

    def next(self):
        with self.lock:
            if len(self.queue) > 0:
                execution = self.pop(0)
                while not execution.done():
                    time.sleep(self.wait_time)
                to_return = execution.result()
                self._submit_to_queue()
                return to_return
            else:
                raise StopIteration
    
    def _submit_to_queue(self):
        with lock:
            while len(self.queue) < max_q_size:
                self.queue.append(executor.submit(generator.next))
                #self.submitted += 1
    
