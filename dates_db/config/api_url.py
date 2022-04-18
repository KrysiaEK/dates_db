from rest_framework import routers

from dates_db.apps.dates.views import DateViewSet

router = routers.DefaultRouter()
router.register(r'dates', DateViewSet)

urlpatterns = router.urls
