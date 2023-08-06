class BaseCheck():
    def check(self):
        return True


class BaseDataBaseCheck(BaseCheck):
    cls = None

    def __init__(self, cls):
        self.cls = cls

    def check(self):
        return len(self.cls.objects.all()) >= 0
