from rest_framework.throttling import UserRateThrottle


class AdminUserRateThrottle(UserRateThrottle):
    scope = "admin"


class GeneralUserRateThrottle(UserRateThrottle):
    scope = "general"


class UserRoleBasedThrottleMixin:
    def get_throttles(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                return [AdminUserRateThrottle()]
            else:
                return [GeneralUserRateThrottle()]
        return super().get_throttles()
