#-*- coding:utf-8 -*-
import sys
import os
import time
import atexit
import signal
import traceback

def appExit(message = 'app is exit now',type_exit = 0,callback_proc = None,callback_args = None):
    try:
        sys.exit(type_exit)
    except SystemExit:
        if callback_proc != None:
            callback_proc(*callback_args)
        print(message)


def term_sig_handler(signum, frame):
    print('catched singal: %d' % signum)
    sys.exit()
 
@atexit.register
def atexit_fun():
    #print('i am exit, stack track:')
    #appExit()
    exc_type, exc_value, exc_tb = sys.exc_info()
    traceback.print_exception(exc_type, exc_value, exc_tb)
