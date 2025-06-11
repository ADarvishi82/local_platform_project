# neighborhoods/views.py
from rest_framework import viewsets, permissions
from .models import Neighborhood
from .serializers import NeighborhoodSerializer, NeighborhoodDetailSerializer

class NeighborhoodViewSet(viewsets.ReadOnlyModelViewSet): # فقط خواندنی برای شروع
    queryset = Neighborhood.objects.all()
    # serializer_class = NeighborhoodSerializer # برای لیست

    def get_serializer_class(self):
        if self.action == 'retrieve': # برای جزئیات از سریالایزر کامل‌تر استفاده کن
            return NeighborhoodDetailSerializer
        return NeighborhoodSerializer # برای لیست از سریالایزر ساده‌تر

    permission_classes = [permissions.AllowAny] # همه می‌توانند لیست محله‌ها را ببینند
    #lookup_field = 'slug' # یا 'id' - اگر می‌خواهید با اسلاگ هم قابل دسترسی باشد، باید اسلاگ را به مدل Neighborhood اضافه کنید