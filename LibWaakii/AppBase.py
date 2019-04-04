#-*- coding:utf-8 -*-
import sys

def appExit(callback_proc = None,callback_args = None,message = 'app is exit now',type_exit = 0):
    try:
        sys.exit(type_exit)
    except SystemExit:
        callback_proc(*callback_args)
        print(message)