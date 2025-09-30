# posts/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet,CommentViewSet
from .views import PostViewSet, CommentViewSet, PopularTagsAPIView, ImportantNewsAPIView  # import کنید
from .views import UpcomingEventsAPIView, RatingViewSet # import کنید

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'Ratings', RatingViewSet, basename='ratings')


urlpatterns = [
    path('', include(router.urls)),
    path('popular-tags/', PopularTagsAPIView.as_view(), name='popular-tags'), # <<<< URL جدید
    path('important-news/', ImportantNewsAPIView.as_view(), name='important-news'), # <<<< URL جدید
    path('upcoming-events/', UpcomingEventsAPIView.as_view(), name='upcoming-events'), # <<<< URL جدید
]

