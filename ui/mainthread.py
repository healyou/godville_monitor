import time
from threading import Event, Thread
from typing import Callable

from .application import TkinterApplication


class ApplicationThread(Thread):
    __stop: Event = None
    __runTkinter: Event = None
    __credential: bool = None
    __app: TkinterApplication = None
    __quitListener: Callable[[], None] = None

    def __init__(self, quitListener: Callable[[], None]):
        Thread.__init__(self)
        self.__quitListener = quitListener
        # При установке будет завершена работа (только, если tkinter не запущен)
        self.__stop = Event()
        # При установке запустит tkinter
        self.__runTkinter = Event()
        # Какую view отобразить
        self.__credential = True

    # Запуск tkinter для ввода имени бога
    def runCredential(self):
        self.__resetToRunTkinter(True)

    # Запуск tkinter для отображения информации о герое (уже должен быть введёно имя бога)
    def runInfo(self):
        self.__resetToRunTkinter(False)

    # завершение работы потока ui (больше tkinter не запустить)
    def quitTkAndThread(self):
        self.__runTkinter.clear()
        self.__stop.set()
        self.__app.destroy()

    # Завершение tkinter и ожидание следующего запуска ui (поток будет ожидать)
    def closeTkinterAndWait(self):
        self.__stop.clear()
        self.__runTkinter.clear()
        self.__app.destroy()

    # Установка переменных для запуска tkinter
    def __resetToRunTkinter(self, credential: bool):
        if self.__app:
            raise Exception('Приложение уже запущено')

        self.__credential = credential
        self.__stop.clear()
        self.__runTkinter.set()

    def run(self):
        while True:
            if (self.__runTkinter.isSet()):
                self.__app = TkinterApplication(self.__credential, self.__quitListener)
                self.__app.run()
                self.__app = None
            elif not self.__stop.isSet():
                time.sleep(0.3)
            else:
                break
