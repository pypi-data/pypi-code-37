
class Notification(object):

    def __init__(self, name, obj = None, user_info = None):
        self._name = name
        self._obj = obj
        self._user_info = user_info

    @property
    def name(self):
        return self._name

    @property
    def obj(self):
        return self._obj

    @property
    def user_info(self):
        return self._user_info


class Singleton(type):
    def __init__(self, *args, **kwargs):
        self._instance = None
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        if self._instance is None:
            self._instance = super().__call__(*args, **kwargs)
            return self._instance
        else:
            return self._instance


class NotificationCenter(metaclass=Singleton):

    def __init__(self):
        self._observer_dict = {}

    def add_observer(self, observer, name):
        # self._observers.append((name, observer));

        if len(name) is 0 or observer is None:
            return
        if name in self._observer_dict:
            observer_queue = self._observer_dict[name]
            observer_queue.append(observer)
        else:
            self._observer_dict[name] = [observer]

    def remove_observer(self, observer, name):
        if len(name) is 0:
            for observer_queue in self._observer_dict.values():
                observer_queue.remove(observer)
        self._observer_dict[name].remove(observer)
        
    def post_notification(self, notification):
        name = notification.name
        if len(name) is 0:
            return
        if len(self._observer_dict[name]) is 0:
            print("_observer_dict[name] length is 0")

            return
        for observer in self._observer_dict[name]:
            observer._notify(notification)
            # print("notify observer" + observer)