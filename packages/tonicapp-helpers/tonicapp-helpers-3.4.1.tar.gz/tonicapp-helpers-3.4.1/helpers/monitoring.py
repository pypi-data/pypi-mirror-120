class BaseMonitoringTest():
    response = None

    def check(self):
        return True


class BaseDataBaseMonitoringTest(BaseMonitoringTest):
    cls = None

    def __init__(self, cls):
        self.cls = cls

    def check(self):
        try:
            return len(self.cls.objects.all()) >= 0
        except Exception as e:
            self.response = f'BaseDataBaseMonitoringTest Error {str(e)}'
            return False


class BaseElasticacheMonitoringTest(BaseMonitoringTest):
    django_rq = None

    def __init__(self, django_rq):
        self.django_rq = django_rq

    def check(self):
        try:
            self.django_rq.get_connection('default')
            return True
        except Exception as e:
            self.response = f'BaseElasticacheMonitoringTest Error {str(e)}'
            return False


class BaseAlgoliaMonitoringTest(BaseMonitoringTest):
    client = None

    def __init__(self, client):
        self.client = client

    def check(self):
        try:
            self.client.search('', None, None, 0, 1)
            return True
        except Exception as e:
            self.response = f'BaseAlgoliaMonitoringTest Error {str(e)}'
            return False
