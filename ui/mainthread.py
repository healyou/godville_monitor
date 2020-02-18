from threading import Thread, Event
from .application import Application
import time


class ApplicationThread(Thread):
    __stop: Event = None
    __runTkinter: Event = None
    __credential: bool = None
    __app: Application = None

    def __init__(self):
        Thread.__init__(self)
        self.__stop = Event()
        self.__runTkinter = Event()
        self.__credential = True

    def runCredential(self):
        self.__credential = True
        self.__runTkinter.set()

    def runInfo(self):
        self.__credential = False
        self.__stop.clear()
        self.__runTkinter.set()

    def quit(self):
        self.__runTkinter.clear()
        self.__stop.set()

    def closeTkinter(self):
        self.__runTkinter.clear()
        self.__app.destroy()

    def run(self):
        while True:
            if (self.__runTkinter.isSet()):
                self.__app = Application(self.__credential)
                self.__app.run()
            elif not self.__stop.isSet():
                time.sleep(0.3)
            else:
                break
