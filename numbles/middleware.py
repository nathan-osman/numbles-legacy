from django.utils import timezone


class TimezoneMiddleware:
    """
    Ensures that all timezones are displayed in the user's timezone.
    """

    def process_request(self, request):
        if request.user.is_authenticated:
            timezone.activate(request.user.profile.timezone)
