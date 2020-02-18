from tkinter import *
from logic.session import Session
from tkinter import messagebox


class Application(object):
    __root: Tk = None

    # Реализация одиночки
    # def __new__(cls):
    #     if not hasattr(cls, 'instance'):
    #         cls.instance = super(Application, cls).__new__(cls)
    #     return cls.instance

    def __init__(self, credential: bool):
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

    def quit(self):
        if messagebox.askokcancel('Выход', 'Вы действительно хотите выйти?'):
            Session.get().quit()
            self.destroy()

    def destroy(self):
        self.__root.destroy()

    def run(self):
        if (not self.isStarted()):
            self.__root.mainloop()

    def isStarted(self):
        return self.__root.winfo_ismapped() == 1
