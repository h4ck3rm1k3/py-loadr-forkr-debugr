from multiprocessing import Pool, Manager, Process
import pdb
import os
import sys
import time

sys.path.append('./celery')
sys.path.append('./vine')
sys.path.append('./billiard')

import billiard
from billiard.process import current_process
from celery.contrib import rdb

from nose.core import TestProgram
import nose

import  pyinotify
#pyinotify.log.setLevel(2)
# def do_test(x):
#     print ("dotest called",x)
    
#     t = TestProgram()
#     t.runTests()

def do_test2(x):
    print ("dotest2 called",x)

    testRunner = nose.core.TextTestRunner(#stream=self.config.stream,
                                          verbosity=3, #self.config.verbosity,
        #config=self.config
    )
       
    t = TestProgram(testRunner=testRunner)
    t.runTests()

class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        print "Creating:", event.pathname
        do_test2(event.pathname)
        
    def process_IN_DELETE(self, event):
        print "Removing:", event.pathname
        do_test2(event.pathname)
        
    def process_IN_MOVED_FROM(self, event):
        print "moved from:", event.pathname
        do_test2(event.pathname)
        
    def process_IN_CLOSE_WRITE(self, event):
        print "closed:", event.pathname
        do_test2(event.pathname)
        
    def process_IN_MODIFY(self, event):
        print "modified:", event.pathname
        do_test2(event.pathname)
        
def do_work():
    print('\nA new child ',  os.getpid())
    #os._exit(0)
    # reply = input("q for quit / c for new fork")
    # if reply == 'c':
    #     print ("cont")
    # else:
    #     return 
    #rdb.set_trace()

    wm = pyinotify.WatchManager()
    handler = EventHandler()
    notifier = pyinotify.Notifier(wm, handler)
    mask =pyinotify.IN_MODIFY | pyinotify.IN_CREATE | pyinotify.IN_MOVED_TO  | pyinotify.IN_MOVED_FROM | pyinotify.IN_CLOSE_WRITE | pyinotify.IN_DELETE
    #pyinotify.ALL_EVENTS
    wm.add_watch(".", mask, rec=True, auto_add=True, do_glob="*")
    # Loop forever (until sigint signal get caught)
    notifier.loop()

    print "after loop"
    time.sleep(1)
    
    # could instantiate some other library class,
    # call out to the file system,
    # or do something simple right here.
    #return "FOO: %s" % val


if __name__ == "__main__":

    manager = Manager()
    results = manager.list()
    num_workers = 1
    work = manager.Queue(num_workers)

    # start for workers    
    pool = []
    while (True):
        for i in xrange(num_workers):
            p = Process(target=do_work)
            p.start()
            pool.append(p)
        for p in pool:
            p.join()
