from tkinter import *
from tkinter import messagebox
from typing import Callable


# Создание и запуск tkinter ui
class TkinterApplication(object):
    __root: Tk = None
    __quitListener: Callable[[], None] = None

    def __init__(self, credential: bool, quitListener: Callable[[], None]):
        self.__quitListener = quitListener
        self.__root = Tk()
        self.__root.geometry('640x480')
        self.__root.title('Godville следилка')
        self.__root.protocol("WM_DELETE_WINDOW", self.quit)
        if credential:
            from .credential.credentional import CredentionalView
            self.__view = CredentionalView(self.__root)
        else:
            from .info.info import InfoView
            self.__view = InfoView(self.__root)

    # Полное завершение работы приложения - для полного listener
    def quit(self):
        if messagebox.askokcancel('Выход', 'Вы действительно хотите выйти?'):
            if self.__quitListener:
                self.__quitListener()
            self.destroy()

    # Завершение только gui tkinter
    def destroy(self):
        if self.__root:
            self.__root.destroy()
            self.__root = None

    def run(self):
        if (not self.isStarted()):
            self.__root.mainloop()

    def isStarted(self):
        return self.__root.winfo_ismapped() == 1
