from multiprocessing import Pool, Manager, Process
import pdb
import os
import sys
sys.path.append('./celery')
sys.path.append('./vine')
sys.path.append('./billiard')

import billiard
from billiard.process import current_process
from celery.contrib import rdb

def do_work():
    print('\nA new child ',  os.getpid())
    #os._exit(0)
    # reply = input("q for quit / c for new fork")
    # if reply == 'c':
    #     print ("cont")
    # else:
    #     return 

    rdb.set_trace()
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
