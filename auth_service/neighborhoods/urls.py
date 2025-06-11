# neighborhoods/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NeighborhoodViewSet # ViewSet خود را import کنید

# یک router برای NeighborhoodViewSet ایجاد کنید
router = DefaultRouter()
router.register(r'neighborhoods', NeighborhoodViewSet, basename='neighborhood')
# r'neighborhoods' پیشوند URL برای این ViewSet خواهد بود (مثلاً /api/neighborhoods/)
# basename='neighborhood' برای نام‌گذاری خودکار URL ها توسط router استفاده می‌شود (مفید برای reverse URL ها)

urlpatterns = [
    # URL های ایجاد شده توسط router را به urlpatterns اضافه کنید
    path('', include(router.urls)),
]