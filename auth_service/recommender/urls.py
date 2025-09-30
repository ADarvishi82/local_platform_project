# recommender/urls.py
from django.urls import path
from .views import BusinessRecommendationAPIView

urlpatterns = [
    path('recommendations/businesses/', BusinessRecommendationAPIView.as_view(), name='business-recommendations'),
]