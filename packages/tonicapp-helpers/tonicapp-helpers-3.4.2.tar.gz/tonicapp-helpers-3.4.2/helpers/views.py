from rest_framework import status

from django.http import HttpResponse
from django.views import View


class BaseMonitoringView(View):
    tests = []

    def get(self, request):
        failed = []

        for test in self.tests:
            if not test.check():
                failed.append(test.response)

        if len(failed) > 0:
            return HttpResponse(failed, status.HTTP_500_INTERNAL_SERVER_ERROR)

        return HttpResponse('OK', status.HTTP_200_OK)
