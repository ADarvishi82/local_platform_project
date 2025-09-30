# recommender/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from neighborhoods.models import Neighborhood
from .engine import recommendation_engine # نمونه موتور توصیه‌گر را import کنید

class BusinessRecommendationAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated] # یا IsAdminUser، بسته به نیاز

    def get(self, request, *args, **kwargs):
        # ID محله را از پارامتر کوئری بگیر
        neighborhood_id = request.query_params.get('neighborhood_id')
        if not neighborhood_id:
            return Response({'error': 'neighborhood_id is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            neighborhood = Neighborhood.objects.get(pk=neighborhood_id)
            neighborhood_name = neighborhood.name
        except Neighborhood.DoesNotExist:
            return Response({'error': 'Neighborhood not found.'}, status=status.HTTP_404_NOT_FOUND)

        # از موتور توصیه‌گر برای گرفتن پیشنهادها استفاده کن
        recommendations = recommendation_engine.recommend_new_businesses(neighborhood_name)
        
        if not recommendations:
            return Response({'message': 'No specific recommendations found for this neighborhood.'}, status=status.HTTP_200_OK)

        return Response(recommendations, status=status.HTTP_200_OK)