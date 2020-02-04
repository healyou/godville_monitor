from tkinter import *
from .contract import IInfoPresenter, IInfoView
from logic.session import Session
from logic.observer import IObserver
from logic.notification import IEvent, NotificationEvent


class InfoView(IInfoView, IObserver):
    __presenter: IInfoPresenter = None
    __root: Tk = None
    __frame: Frame = None
    __errorLabel: Label = None
    __notificationTextField: Text = None

    def __init__(self, root: Tk):
        IInfoView.__init__(self)
        IObserver.__init__(self)
        self.__presenter = InfoPresenter(self)
        self.__root = root
        self.__initFrame()

    def __initFrame(self):
        self.__clearChildrens()

        self.__frame = Frame(master=self.__root, height=2, bd=1, relief=SUNKEN)
        self.__frame.pack(fill=BOTH, expand=True, padx=5, pady=5)

        self.__errorLabel = Label(master=self.__frame, text='TEST')
        self.__errorLabel.place(relx=.5, rely=.1, anchor='c')

        godNameLabel = Label(master=self.__frame, text='Имя бога')
        godNameLabel.place(relx=.5, rely=.2, anchor='c')

        self.__notificationTextField = Text(master=self.__frame, width=25, height=5, bg="darkgreen", fg='white', wrap=WORD)
        self.__notificationTextField.place(relx=.5, rely=.4, anchor='c')

        enterButton = Button(text='Назад', command=self.__onBackClick)
        enterButton.place(relx=.5, rely=.9, anchor='c')

    def __onBackClick(self):
        self.__presenter.backClick()

    def __clearChildrens(self):
        for widget in self.__root.winfo_children():
            widget.destroy()

    def showCredentionalView(self) -> None:
        from ui.credential.credentional import CredentionalView
        CredentionalView(self.__root)

    def update(self, event: IEvent) -> None:
        if (self.__notificationTextField is not None and isinstance(event, NotificationEvent)):
            event: NotificationEvent = event
            self.__notificationTextField.insert(END, event.message)
            self.__notificationTextField.see(END)


class InfoPresenter(IInfoPresenter):
    __view: IInfoView = None

    def __init__(self, view: IInfoView):
        super(IInfoPresenter, self).__init__()
        self.__view = view
        Session.get().startLoadData([self.__view])

    def backClick(self) -> None:
        Session.get().stopLoadData()
        self.__view.showCredentionalView()
