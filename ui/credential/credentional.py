from tkinter import *
from .contract import ICredentionalPresenter, ICredentionalView
from logic.session import Session


class CredentionalView(ICredentionalView):
    __presenter: ICredentionalPresenter = None
    __root: Tk = None
    __frame: Frame = None
    __errorLabel: Label = None
    __godName: StringVar = None
    __token: StringVar = None

    def __init__(self, root: Tk):
        super(ICredentionalView, self).__init__()
        self.__presenter = CredentionalPresenter(self)
        self.__root = root
        self.__initFrame()

    def __initFrame(self):
        self.__clearChildrens()

        self.__frame = Frame(master=self.__root, height=2, bd=1, relief=SUNKEN)
        self.__frame.pack(fill=BOTH, expand=True, padx=5, pady=5)

        self.__errorLabel = Label(master=self.__frame, text='')
        self.__errorLabel.place(relx=.5, rely=.1, anchor='c')

        self.__godName = StringVar()
        godNameLabel = Label(master=self.__frame, text='Имя бога')
        godNameLabel.place(relx=.5, rely=.2, anchor='c')
        godnameEntry = Entry(master=self.__frame, textvariable=self.__godName)
        godnameEntry.place(relx=.5, rely=.3, anchor='c')

        self.__token = StringVar()
        tokenLabel = Label(master=self.__frame, text='Ключ, если нужна приватная информация')
        tokenLabel.place(relx=.5, rely=.4, anchor='c')
        tokenEntry = Entry(master=self.__frame, textvariable=self.__token)
        tokenEntry.place(relx=.5, rely=.5, anchor='c')

        enterButton = Button(text='Вход', command=self.__enterCredentional)
        enterButton.place(relx=.5, rely=.6, anchor='c')

    def __clearChildrens(self):
        for widget in self.__root.winfo_children():
            widget.destroy()

    def __enterCredentional(self):
        godName: str = self.__godName.get()
        token: str = self.__token.get()
        self.__presenter.enterCredentional(godName, token)

    def showInfoView(self, openInfo: bool) -> None:
        from ui.info.info import InfoView
        InfoView(self.__root)

    def showCredentionalError(self, message: str) -> None:
        self.__errorLabel.config(text=message)


class CredentionalPresenter(ICredentionalPresenter):
    __view: ICredentionalView = None

    def __init__(self, view: ICredentionalView):
        super(ICredentionalPresenter, self).__init__()
        self.__view = view

    def enterCredentional(self, godName: str, token: str) -> None:
        if not godName:
            self.__view.showCredentionalError('Необходимо ввести имя бога')
        elif not token:
            Session.get().authenticate(godName)
            self.__view.showInfoView(True)
        else:
            Session.get().authenticate(token)
            self.__view.showInfoView(False)
