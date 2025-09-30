# users/urls.py
from django.urls import path, include
from .views import GoogleLoginAPIView, UserPostsAPIView # <<<< ویو جدید را import کنید
from .views import MyNeighborhoodStatsAPIView # import کنید


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
    path('auth/google/', GoogleLoginAPIView.as_view(), name='google_login_custom'), # <<<< URL جدید
    path('users/<int:user_id>/posts/', UserPostsAPIView.as_view(), name='user-posts-list'),
    path('my-neighborhood/stats/', MyNeighborhoodStatsAPIView.as_view(), name='my-neighborhood-stats'),

]
