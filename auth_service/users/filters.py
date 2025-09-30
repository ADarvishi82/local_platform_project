# users/filters.py
from django_filters import rest_framework as filters
from .models import BusinessProfile
from django.db.models import Q


class BusinessProfileFilter(filters.FilterSet):
    # فیلتر برای محدوده قیمت و حداقل امتیاز (بدون تغییر)
    min_price = filters.NumberFilter(field_name="base_price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="base_price", lookup_expr='lte')
    min_rating = filters.NumberFilter(field_name="average_rating", lookup_expr='gte')

    # فیلتر بر اساس نام دسته‌بندی
    category_name = filters.CharFilter(field_name='category__name', lookup_expr='icontains')

    # فیلتر بر اساس نام محله
    neighborhood_name = filters.CharFilter(field_name='neighborhood__name', lookup_expr='icontains')

    # ***** فیلتر جستجوی عمومی (بسیار مهم) *****
    search = filters.CharFilter(method='filter_by_search_terms', label="Search")
    name = filters.CharFilter(field_name='business_name', lookup_expr='icontains')

    class Meta:
        model = BusinessProfile
        # فیلتر ساده بر اساس ID محله
        fields = ['neighborhood']

    def filter_by_search_terms(self, queryset, name, value):
        """
        جستجو در نام کسب‌وکار، توضیحات، و تگ‌ها بر اساس کلمات کلیدی.
        """
        if not value:
            return queryset
        
        # کلمات جستجو را از هم جدا کن
        search_terms = value.split()
        
        # یک کوئری OR پیچیده بساز
        query = Q()
        for term in search_terms:
            query |= (
                Q(business_name__icontains=term) |
                Q(description__icontains=term) |
                Q(tags__name__icontains=term)
            )
        
        # queryset را با این کوئری فیلتر کن و نتایج تکراری را حذف کن
        return queryset.filter(query).distinct()