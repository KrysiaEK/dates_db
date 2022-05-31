from rest_framework import routers

from dates_db.apps.dates.views import DateViewSet, PopularityViewSet


class OptionalSlashRouter(routers.DefaultRouter):

    def __init__(self):
        super().__init__()
        self.trailing_slash = '/?'


router = OptionalSlashRouter()
router.register(r'dates', DateViewSet, basename='dates')
router.register(r'popular', PopularityViewSet, basename='popular')

urlpatterns = router.urls
