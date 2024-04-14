from queue import Queue, Empty
from threading import Thread, Event
import time
import os

class ThreadPool:
    def __init__(self):
        cpu_count = os.cpu_count()
        # self.num_threads = int(os.getenv('TP_NUM_OF_THREADS', cpu_count))
        self.num_threads = 1
        self.tasks_queue = Queue()
        self.shutdown_event = Event()
        self.workers = []

        for _ in range(self.num_threads):
            worker = TaskRunner(self.tasks_queue, self.shutdown_event)
            worker.start()
            self.workers.append(worker)

    def add_task(self, func, *args):
        self.tasks_queue.put((func, args))

    def shutdown(self):
        self.shutdown_event.set()
        self.tasks_queue.join()
        for worker in self.workers:
            worker.join()

class TaskRunner(Thread):
    def __init__(self, task_queue, shutdown_event):
        Thread.__init__(self)
        self.task_queue = task_queue
        self.shutdown_event = shutdown_event

    def run(self):
        while not self.shutdown_event.is_set() or not self.task_queue.empty():
            try:
                func, args = self.task_queue.get(timeout=0.05)
                func(*args)
                self.task_queue.task_done()
            except Empty:
                continue