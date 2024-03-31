from queue import Queue, Empty
from threading import Thread, Event
import time
import os

class ThreadPool:
    def __init__(self):
        # You must implement a ThreadPool of TaskRunners
        # Your ThreadPool should check if an environment variable TP_NUM_OF_THREADS is defined
        # If the env var is defined, that is the number of threads to be used by the thread pool
        # Otherwise, you are to use what the hardware concurrency allows
        # You are free to write your implementation as you see fit, but
        # You must NOT:
        #   * create more threads than the hardware concurrency allows
        #   * recreate threads for each task

        cpu_count = os.cpu_count()
        self.num_threads = int(os.getenv('TP_NUM_OF_THREADS', cpu_count))
        self.tasks_queue = Queue()
        self.shutdown_event = Event()
        self.workers = []

        for _ in range(self.num_threads):
            worker = TaskRunner(self.tasks_queue, self.shutdown_event)
            worker.start()
            self.workers.append(worker)

    def add_task(self, func, *args, **kwargs):
        # Adaugă un task în coada de task-uri
        self.tasks_queue.put((func, args, kwargs))

    def shutdown(self):
        # Notifică thread-urile să finalizeze
        self.shutdown_event.set()
        # Așteaptă ca toate task-urile să fie procesate
        self.tasks_queue.join()
        # Așteaptă ca toate thread-urile să se oprească
        for worker in self.workers:
            worker.join()


        
        pass

class TaskRunner(Thread):
    def __init__(self, task_queue, shutdown_event):
        Thread.__init__(self)
        self.task_queue = task_queue
        self.shutdown_event = shutdown_event
        self.daemon = True  # Asigură că thread-ul nu va preveni închiderea programului

    def run(self):
        while not self.shutdown_event.is_set() or not self.task_queue.empty():
            try:
                # Ia următorul task din coadă
                func, args, kwargs = self.task_queue.get(timeout=0.05)
                # Rulează task-ul
                func(*args, **kwargs)
                self.task_queue.task_done()
            except Empty:
                continue
