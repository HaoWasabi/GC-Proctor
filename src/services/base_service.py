class BaseService(object):
    _instances = {}
    def __new__(class_, *args, **kwargs):
        if class_ not in class_._instances:
            class_._instances[class_] = super(BaseService, class_).__new__(class_, *args, **kwargs)
        return class_._instances[class_]