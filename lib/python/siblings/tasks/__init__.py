# Copyright 2007 Mikael Lind.

"""Task for deferred execution by a unit.

Tasks follow the Command pattern; their execution can be deferred until later.
Tasks are enqueued in units and executed in FIFO order. Tasks can also be
created and executed by other tasks.
    
Tasks provide cooperative multiprocessing using generators. It is generally
simpler to implement a complex task as a generator than as a state machine. For
tracking purposes, tasks yield their current progress as a float in the range
[0.0, 1.0].
"""
