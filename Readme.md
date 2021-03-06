# Problem
You want to load a ton of slow things and then test something, and then make changes and retry
it takes a long time to load libs and other data into your base.

# Solution

Load your libs in the the main program, fork it with a simple call to forker.main, and then use nose tests that get the global data to test your changes. Optionally spawn a pdb in the child to allow you to test your changes.
each child can import more code. If you want to lose the changes, just exit and it will be restored. You can kill the child process any time and a new one will spawn. The program will wait for changes to the file system to rerun the tests.

# Usage

Simple forking like pdb

    import forkr
    data = { 'foo': 1 }
    forkr.main(data)

# Recursive forks.

In theory, you can start a new forking loop in the child process after you have done the changes you want to change, so have a spawnloop function you can call to start a new fork from the child to allow you to connect to the new children. You can do that by invoking the forker.main


## RDB Usage

Optional :
	  You use the simple telnet client to connect to the server from another shell.

In your client lib if you want to enable remote debugging, you can use the celery rdb.
	
	call rdb.set_trace()  in your code to debug
	
and then connect 

	python client.py localhost 6899


### RDB Deps

    	https://github.com/celery/billiard
	https://github.com/celery/celery
	https://github.com/celery/vine

# Improvement

Normal nose test 
```
host:~/experiments/forking$ nosetests --verbose
clientcode_test.test_series ... ok
multiproc_test.test ... FAIL
multiproc_test.test2 ... ok

======================================================================
FAIL: multiproc_test.test
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/lib/python2.7/dist-packages/nose/case.py", line 197, in runTest
    self.test(*self.arg)
  File "/home/mdupont/experiments/forking/multiproc_test.py", line 2, in test
    assert False
AssertionError

----------------------------------------------------------------------
Ran 3 tests in 0.374s
```

Now inside of the forked process we have a 100x speedup

```
('dotest2 called', '/home/mdupont/experiments/forking/Readme.md')
clientcode_test.test_series ... ok
multiproc_test.test ... FAIL
multiproc_test.test2 ... ok

======================================================================
FAIL: multiproc_test.test
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/lib/python2.7/dist-packages/nose/case.py", line 197, in runTest
    self.test(*self.arg)
  File "/home/mdupont/experiments/forking/multiproc_test.py", line 2, in test
    assert False
AssertionError

----------------------------------------------------------------------
Ran 3 tests in 0.004s

FAILED (failures=1)
```

# Sources
	
Attaching to debugger 
* https://github.com/ionelmc/python-remote-pdb
* https://github.com/celery/celery
* http://stolarscy.com/dryobates/2014-03/debugging_python_code/
* http://docs.celeryproject.org/en/latest/userguide/debugging.html
* https://stackoverflow.com/questions/9178751/use-pdb-set-trace-in-a-script-that-reads-stdin-via-a-pipe#34687825
* http://code.activestate.com/recipes/576515/
* https://stackoverflow.com/questions/4163964/python-is-it-possible-to-attach-a-console-into-a-running-process

Forking
* https://docs.python.org/2/library/multiprocessing.html#module-multiprocessing
* http://www.python-course.eu/forking.php
* https://docs.python.org/2/library/os.html#os.waitpid
* https://stackoverflow.com/questions/11996632/multiprocessing-in-python-while-limiting-the-number-of-running-processes

Nose

* http://ivory.idyll.org/articles/nose-intro.html
* http://nose.readthedocs.io/en/latest/api/core.html
* https://nose.readthedocs.io/en/latest/usage.html

Pyinotify
* https://github.com/seb-m/pyinotify
