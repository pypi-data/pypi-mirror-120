import sqlite3
from queue import Queue
import threading


# this is used so that in run_queue we can check the .type of the object passed
class CommitObject:
    def __init__(self):
        self.type = 'Commit'


class Session:
    def __init__(self, db_path):
        self.db_path = db_path

        # making db connection
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.c = self.conn.cursor()

        # making running thread
        self.queue = Queue(maxsize=0)
        self.done = {}
        self.running = True
        self.t = threading.Thread(target=self.run_queue)
        self.t.start()

    def run_queue(self):
        while self.running:
            item = self.queue.get()
            # checking if its a select query to return the result
            if item.type == 'SELECT':
                data = item.execute(self.c)
                self.done[str(item)] = data
            elif item.type == 'Commit':
                self.conn.commit()
                self.done[str(item)] = None
            else:
                item.execute(self.conn, self.c)
                self.done[str(item)] = None

    def select(self, selectobj):
        if self.running:
            self.queue.put(selectobj)
            # waiting for the query to be run then returning it
            while str(selectobj) not in list(self.done.keys()):
                pass
            data = self.done[str(selectobj)]
            del self.done[str(selectobj)]
            return data

    def add(self, obj):
        if self.running:
            # adding a insert, update or delete object to the queue for the run_queue thread to execute
            self.queue.put(obj)
            while str(obj) not in list(self.done.keys()):
                pass
            del self.done[str(obj)]

    def commit(self):
        if self.running:
            obj = CommitObject()
            self.queue.put(obj)
            while str(obj) not in list(self.done.keys()):
                pass
            del self.done[str(obj)]

    def stop(self):
        # stopping queue thread and closing db
        self.running = False
        self.conn.close()
