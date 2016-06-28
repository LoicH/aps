# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 10:57:34 2016

@author: loic
"""

import time
import threading

threadNumber = 0


def count(n):
    for i in range(1,6):
        print "Thread",n,":",i
        time.sleep(0.5)
     
    
def launch_thread(): 
    global threadNumber      
    threadNumber += 1
    threading.Thread(target=count, args=(threadNumber,)).start()
    time.sleep(.25)
    threadNumber += 1
    threading.Thread(count(threadNumber)).start()