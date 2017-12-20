from django.apps import apps
from django.http import JsonResponse
from django.views.generic import View


class HealthCheckMixin:
    """
    Very basic health check mixin that allows the health checker
    instance to be retrieved from the corresponding AppConfig
    and the status to be retrieved and returned
    """
    @staticmethod
    def get_health_checker():
        """
        Retrieves and returns the health checker instance associated
        with the app config for the django healthysnake app

        :return: healthysnake.healthcheck.HealthCheck instance
        """
        return apps.get_app_config('healthysnake').health_checker

    def get_health_status(self):
        """
        Retrieves the health checker instance then returns the data
        generated by the status method

        :return: Dict of health check status data
        """
        return self.get_health_checker().status()


class HealthCheckView(HealthCheckMixin, View):
    """
    View for running the health checker and returning
    the status data sa a json encoded response object
    """
    def get(self, request, *args, **kwargs):
        """
        Generates and returns a health check status for the server

        :param request: Incoming HTTP request instance
        :param args: Default positional args
        :param kwargs: Default keyword args

        :return: JSON encoded health status response
        """
        status = self.get_health_status()
        response = JsonResponse(status)
        if not status.get('healthy', False):
            response.status_code = 503
        return response
