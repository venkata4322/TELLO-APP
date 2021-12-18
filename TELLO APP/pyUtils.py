#!/usr/bin/python3
# File name   : pyUtils.py
# Description : utility module for python

import threading
from datetime import datetime

def timePrint(msg):
    """ print with time stamp """
    print(str(datetime.now()) + ' ' + msg)

def splitAndTrim(string, delimiter):
    """ split the string and remove all empty parts """
    parts = string.split(delimiter)
    results = []
    for item in parts:
        if len(item) == 0:
            continue
        results.append(item)
    return results

def startThread(context, target, front=True, args=()):
    """ start a thread to run the specified target function """
    timePrint('Starting thread: ' + context)
    thread = threading.Thread(target=target, args=args)
    thread.setDaemon(front)                            # 'True' for a front thread and would close when the mainloop() closes
    thread.start()
    return thread

def timestamp():
    """ get current time stamp format as yyyy-mmdd-hhmmss """
    return datetime.now().strftime('%Y-%m%d-%H%M%S')
