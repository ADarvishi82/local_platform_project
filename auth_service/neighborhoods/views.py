# neighborhoods/views.py
from rest_framework import viewsets, permissions
from .models import Neighborhood
from .serializers import NeighborhoodSerializer, NeighborhoodDetailSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class NeighborhoodViewSet(viewsets.ReadOnlyModelViewSet): # فقط خواندنی برای شروع
    queryset = Neighborhood.objects.all()
    # serializer_class = NeighborhoodSerializer # برای لیست

    def get_serializer_class(self):
        if self.action == 'retrieve': # برای جزئیات از سریالایزر کامل‌تر استفاده کن
            return NeighborhoodDetailSerializer
        return NeighborhoodSerializer # برای لیست از سریالایزر ساده‌تر

    permission_classes = [permissions.AllowAny] # همه می‌توانند لیست محله‌ها را ببینند
    #lookup_field = 'slug' # یا 'id' - اگر می‌خواهید با اسلاگ هم قابل دسترسی باشد، باید اسلاگ را به مدل Neighborhood اضافه کنید
    
    @action(detail=True, methods=['get'], url_path='stats')
    def stats(self, request, pk=None): # اگر از id استفاده می‌کنید، pk؛ اگر از slug، slug=None
        """
        آمار یک محله خاص را برمی‌گرداند.
        """
        neighborhood = self.get_object() # محله با pk مربوطه را پیدا می‌کند
        
        stats_data = {
            'id': neighborhood.id,
            'name': neighborhood.name,
            'city': neighborhood.city,
            'resident_count': neighborhood.user_profiles_in_neighborhood.count(),
            'business_count': neighborhood.business_profiles_in_neighborhood.count(),
            # می‌توانید آمار دیگری هم اضافه کنید، مثلاً تعداد پست‌های این محله
            'post_count': neighborhood.post_set.count() # فرض می‌کنیم related_name پیش‌فرض استفاده شده
                                                          # یا post_set را به related_name در مدل Post تغییر دهید
        }
        return Response(stats_data)