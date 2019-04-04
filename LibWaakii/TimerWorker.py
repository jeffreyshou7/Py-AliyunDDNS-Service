#-*- coding:utf-8 -*-
from threading import Timer

from datetime import datetime

class ScheduleTimer( object ):

    def __init__( self, start_time = datetime.now(), interval = 0, callback_proc = None, args=None, kwargs=None ):

        self.__timer = None
        self.__start_time = start_time
        self.__interval = interval
        self.__callback_pro = callback_proc
        self.__args = args if args is not None else []
        self.__kwargs = kwargs if kwargs is not None else {}

    def exec_callback( self, args=None, kwargs=None ):
        self.__callback_pro( *self.__args, **self.__kwargs )
        self.__timer = Timer( self.__interval, self.exec_callback )
        self.__timer.start()

    def start( self ):
        if self.__callback_pro != None:
            interval = self.__interval - ( datetime.now().timestamp() - self.__start_time.timestamp() )
            # print( interval )
            self.__timer = Timer( interval, self.exec_callback )
            self.__timer.start()

    def cancel( self ):
        self.__timer.cancel() 
        self.__timer = None