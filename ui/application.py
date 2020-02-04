from tkinter import *
from .credential.credentional import CredentionalView, CredentionalPresenter
from logic.session import Session
from tkinter import messagebox


class Application(object):
    __root: Tk = None

    # Реализация одиночки
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Application, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.__root = Tk()
        self.__root.geometry('640x480')
        self.__root.title('Godville следилка')
        self.__root.protocol("WM_DELETE_WINDOW", self.quit)
        self.__credView: CredentionalView = CredentionalView(self.__root)

    def quit(self):
        if messagebox.askokcancel('Выход', 'Вы действительно хотите выйти?'):
            Session.get().quit()
            self.__root.destroy()

    def run(self):
        if (not self.isStarted()):
            self.__root.mainloop()

    def isStarted(self):
        return self.__root.winfo_ismapped() == 1
