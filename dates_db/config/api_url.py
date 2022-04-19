from rest_framework import routers

from dates_db.apps.dates.views import DateViewSet, PopularityViewSet

router = routers.DefaultRouter()
router.register(r'dates', DateViewSet, basename='dates')
router.register(r'popular', PopularityViewSet, basename='popular')

urlpatterns = router.urls
