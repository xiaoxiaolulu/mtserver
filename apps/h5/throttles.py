from rest_framework import throttling


class SMSCodeRateThrottle(throttling.SimpleRateThrottle):
    """
    Limits the rate of API calls that may be made by a given user.

    The user id will be used as a unique cache key if the user is
    authenticated.  For anonymous requests, the IP address of the request will
    be used.
    """
    scope = 'smscode'

    def get_cache_key(self, request, view):
        telephone = request.GET.get("tel")
        if telephone:
            ident = telephone
        else:
            ident = self.get_ident(request)

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }
