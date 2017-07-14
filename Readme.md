# Problem
	You want to load a ton of slow things and then test something, and then make changes and retry
	it takes a long time to load libs and other data into your base.

# Solution

Load your libs in the the main program, fork it and then spawn a pdb in the child to allow you to test your changes.
each child can import more code. If you want to lose the changes, just exit and it will be restored.

You use the simple telnet client to connect to the server from another shell.

# Ideas

For the future, be able to start a new loop in the child after you have changes you want to change, so have a spawnloop function you can call to start a new fork from the child to allow you to connect to the new children.
	
# Usage

    python multiproc.py
	
and then connect 

	python client.py localhost 6899

# Deps

	git@github.com:celery/billiard.git
	git@github.com:celery/celery.git
	git@github.com:celery/vine.git
	

# Sources
	
https://github.com/ionelmc/python-remote-pdb
https://docs.python.org/2/library/os.html#os.waitpid
https://github.com/celery/celery
http://stolarscy.com/dryobates/2014-03/debugging_python_code/
http://docs.celeryproject.org/en/latest/userguide/debugging.html
https://stackoverflow.com/questions/9178751/use-pdb-set-trace-in-a-script-that-reads-stdin-via-a-pipe#34687825
https://stackoverflow.com/questions/11996632/multiprocessing-in-python-while-limiting-the-number-of-running-processes
https://docs.python.org/2/library/multiprocessing.html#module-multiprocessing
http://code.activestate.com/recipes/576515/
https://stackoverflow.com/questions/4163964/python-is-it-possible-to-attach-a-console-into-a-running-process
http://www.python-course.eu/forking.php
