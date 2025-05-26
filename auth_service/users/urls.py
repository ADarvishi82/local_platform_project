# users/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserProfileViewSet,
    BusinessProfileViewSet,
    CategoryViewSet,
    TagViewSet,
    # UserViewSet # اگر دارید
)

router = DefaultRouter()
router.register(r'user-profiles', UserProfileViewSet, basename='userprofile')
router.register(r'business-profiles', BusinessProfileViewSet, basename='businessprofile')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'tags', TagViewSet, basename='tag')
# router.register(r'users', UserViewSet, basename='user') # اگر دارید

urlpatterns = [
    path('', include(router.urls)),
]