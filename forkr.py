
"""
import forkr

"""
from multiprocessing import Pool, Manager, Process
import pdb
import os
import sys
import time
import pprint

#sys.path.append('./celery')
#sys.path.append('./vine')
#sys.path.append('./billiard')

#import billiard
#from billiard.process import current_process
#from celery.contrib import rdb

from nose.core import TestProgram
import nose

import  pyinotify

#import clientcode
#from clientcode import *


from nose.plugins.base import Plugin

import sys

import logging

def set_logging(level=logging.DEBUG):
    for x in sys.modules:
        d = logging.getLogger(x)
        if d:
            #print "setting log for ", x
            d.setLevel(level)
        else:
            print "no logger", x

set_logging()

class DataPlugin(Plugin):
    
    def __init__(self, data):
        self.data = data
        print "data plugin loaded"
        Plugin.__init__(self)
        
    def configure(self, options, conf):
        self.conf = conf
        self.enabled = True

    def prepareTest(self, test):
        print "data plugin prepared"
        #pprint.pprint(test)
        return test

    def install_data(self, test):
        if 'test' not in dir(test):
            raise Exception("no test in test")
        if 'test' not in dir(test.test):
            ttt= test.test
            ttt._xdata_ = self.data
            m = sys.modules[ttt.__module__]
            m.__global_test_data__=self.data

        else:
            ttt= test.test.test
            ttt._xdata_ = self.data
            m = sys.modules[ttt.__module__]
            m.__global_test_data__=self.data

    def prepareTestCase(self, test):
        print "data plugin prepare test case"
        #pprint.pprint(test)

        # #pprint.pprint(test.__dict__)
        # print "test.test"
        # pprint.pprint(test.test)
        # print "test.test.__dict__"
        # pprint.pprint(test.test.__dict__)

        # print "dir test.test"
        # pprint.pprint(dir(test.test))
        # print "class"
        # pprint.pprint(test.__class__)
        # print "module"
        # pprint.pprint(test.__module__)

        ####################3

        # print "ttt.__dict__"
        # pprint.pprint(ttt.__dict__)
        # print "dir test.test"
        # pprint.pprint(dir(ttt))
        # print "ttt class"
        # pprint.pprint(ttt.__class__)
        # print "ttt module"
        # pprint.pprint(ttt.__module__)
            
            #._xdata_ = self.data
        #ttt.__class__._xdata_ = self.data
    
        def run(result):

            self.install_data(test)

            print "going to call: ",test.test
            t = test.test(result)
            
            print "warnings captured: ",t

        return run

class RunObject:
    def __init__(self, forkr) :
        self.forkr= forkr
    
    def do_nose(self):
        t0 = time.time()
        print "do nose"
        dp = DataPlugin(self.forkr._data)
        noseConfig = nose.config.Config(
            showPlugins =True,
            #debug =99,
    

        )
        #noseConfig.testMatchPat = 'Tests|_test'
        #noseConfig.verbosity = 9999
        #sys.exit(0 if nose.run() else 1)
        
        testRunner = nose.core.TextTestRunner(#stream=self.config.stream,
            config=noseConfig,
            #verbosity=1000, #self.config.verbosity,
            #config=self.config
        )
        t = TestProgram(testRunner=testRunner,
                        #config=noseConfig,
                        plugins = [
                            dp,
                        ],


        )
        t.runTests()
        t1 = time.time()

        total_n = t1-t0
        print ("took total",total_n)

    def do_test2(self, x):
        print ("dotest2 called",x)
        print ("params are",pprint.pformat(self.forkr._data))
        self.do_nose()

class EventHandler(pyinotify.ProcessEvent):
    def __init__(self, forkr) :
        self.forkr= forkr
        
    def do_test2(self,e):
        self.forkr.runobj.do_test2(e)
        
    def process_IN_CREATE(self, event):
        print "Creating:", event.pathname
        self.do_test2(event.pathname)

    def process_IN_DELETE(self, event):
        print "Removing:", event.pathname
        self.do_test2(event.pathname)

    def process_IN_MOVED_FROM(self, event):
        print "moved from:", event.pathname
        self.do_test2(event.pathname)

    def process_IN_CLOSE_WRITE(self, event):
        print "closed:", event.pathname
        self.do_test2(event.pathname)

    def process_IN_MODIFY(self, event):
        print "modified:", event.pathname
        self.do_test2(event.pathname)

    def process_IN_MOVED_TO (self, event):
        print "moved to:", event.pathname
        self.do_test2(event.pathname)

    def process_IN_UNMOUNT    (self, event):
        print "unmount:", event.pathname
        self.do_test2(event.pathname)

    def process_IN_Q_OVERFLOW(self, event):
        print "overflow:", event.pathname
        self.do_test2(event.pathname)

    def process_IN_DONT_FOLLOW(self, event):
        print "dont follow:", event.pathname
        self.do_test2(event.pathname)



class Forkr :
    def __init__(self,data):
        self._data = data
        self.manager = Manager()
        self.exec_count  = 0
        self.runobj=None

    def main(self):
        results = self.manager.list()
        num_workers = 1
        work = self.manager.Queue(num_workers)

        # start for workers
        pool = []
        while (True):
            for i in xrange(num_workers):
                p = Process(target=self.child_process)
                p.start()
                pool.append(p)
            for p in pool:
                p.join()

    def child_process(self):
        print('A new child ',  os.getpid())
        #os._exit(0)
        # reply = input("q for quit / c for new fork")
        # if reply == 'c':
        #     print ("cont")
        # else:
        #     return
        #rdb.set_trace()

        wm = pyinotify.WatchManager()

        handler = EventHandler(self)

        notifier = pyinotify.Notifier(wm, handler)
        mask =pyinotify.IN_MODIFY | pyinotify.IN_CREATE | pyinotify.IN_MOVED_TO  | \
               pyinotify.IN_MOVED_FROM | pyinotify.IN_CLOSE_WRITE | pyinotify.IN_DELETE \
               | pyinotify.IN_UNMOUNT      \
               | pyinotify.IN_Q_OVERFLOW \
               | pyinotify.IN_DONT_FOLLOW
        #pyinotify.ALL_EVENTS
        wm.add_watch(".", mask, rec=True, auto_add=True, do_glob="*")

        print "Waiting for a change before triggering"

        if self.exec_count == 0:
            print "running one time"
            #handler.do_test2("None")


        # Loop forever (until sigint signal get caught)
        notifier.loop()

        print "after loop"
        time.sleep(1)

        # could instantiate some other library class,
        # call out to the file system,
        # or do something simple right here.
        #return "FOO: %s" % val


def main(data = None):
    forkr = Forkr(data)
    r = RunObject(forkr)
    forkr.runobj=r
#   forkr.runobj.do_test2("data")
    forkr.main()

def do_one(data = None):
    forkr = Forkr(data)
    r = RunObject(forkr)
    forkr.runobj=r
    forkr.runobj.do_test2("data")

    
if __name__ == "__main__":
    main()
