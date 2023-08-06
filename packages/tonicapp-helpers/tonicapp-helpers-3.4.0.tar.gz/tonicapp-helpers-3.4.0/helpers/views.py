from rest_framework import status

from django.http import HttpResponse
from django.views import View


class BaseMonitoringView(View):
    checks = []

    def get(self, request):
        not_ok = []

        for check in self.checks:
            if not check.ok():
                not_ok.append(check.response)

        if len(not_ok) > 0:
            return HttpResponse(not_ok, status.HTTP_500_INTERNAL_SERVER_ERROR)

        return HttpResponse('OK', status.HTTP_200_OK)
