from rest_framework import routers

from .views import PlantViewSet

router = routers.DefaultRouter()
router.register('plants', PlantViewSet, 'plants')

urlpatterns = router.urls
