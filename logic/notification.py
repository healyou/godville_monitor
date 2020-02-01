from .observer import IEvent, IObserver, IObservable, LoadErrorEvent, LoadDataEvent


class ConsoleObserver(IObserver):
    def __init__(self):
        pass

    def update(self, event: IEvent) -> None:
        if (isinstance(event, LoadErrorEvent)):
            errorEvent: LoadErrorEvent = event
            print(errorEvent.error)
        elif (isinstance(event, LoadDataEvent)):
            loadDataEvent: LoadDataEvent = event
            print(loadDataEvent.loadDate)
            print(loadDataEvent.info.__dict__)
        else:
            raise Exception('Неизвестный тип уведомления')