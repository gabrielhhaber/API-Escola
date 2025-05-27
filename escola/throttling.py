from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
class MatriculaAnonRateThrottle(AnonRateThrottle):
    rate = "1/second"

class MatriculaUserRateThrottle(UserRateThrottle):
    rate = "5/second"