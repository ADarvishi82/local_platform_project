# users/filters.py
from django_filters import rest_framework as filters
from .models import BusinessProfile

class BusinessProfileFilter(filters.FilterSet):
    # فیلترهای سفارشی
    min_price = filters.NumberFilter(field_name="base_price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="base_price", lookup_expr='lte')
    min_rating = filters.NumberFilter(field_name="average_rating", lookup_expr='gte')
    name = filters.CharFilter(field_name='business_name', lookup_expr='icontains')
    category_name = filters.CharFilter(field_name='category__name', lookup_expr='iexact')
    tags = filters.CharFilter(field_name='tags__name', lookup_expr='iexact')
    
    class Meta:
        model = BusinessProfile

        fields = {
            'neighborhood': ['exact'], # فیلتر بر اساس ID دقیق محله
            
        }        # اگر می‌خواهید برای category بر اساس ID هم فیلتر کنید، می‌توانید 'category' را هم اینجا اضافه کنید.