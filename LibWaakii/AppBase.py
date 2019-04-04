#-*- coding:utf-8 -*-
import sys

def appExit(message = 'app is exit now',type_exit = 0,callback_proc = None,callback_args = None):
    try:
        sys.exit(type_exit)
    except SystemExit:
        if callback_proc != None:
            callback_proc(*callback_args)
        print(message)