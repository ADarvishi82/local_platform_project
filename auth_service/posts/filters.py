# posts/filters.py
from django_filters import rest_framework as filters
from .models import Post, Neighborhood # مدل‌های لازم را import کنید
from users.models import BusinessProfile # برای فیلتر بر اساس نوع حساب تجاری

class PostFilter(filters.FilterSet):
    # فیلتر بر اساس نام شهر (از طریق محله مربوط به پست)
    # city = filters.CharFilter(field_name='neighborhood__city', lookup_expr='icontains')

    # فیلتر بر اساس ID محله
    neighborhood = filters.NumberFilter(field_name='neighborhood__id')

    # فیلتر بر اساس نوع پست (تجاری/سازمانی یا شخصی)
    # این کمی پیچیده‌تر است چون نوع پست مستقیماً در مدل Post نیست
    # ما یک فیلتر سفارشی برای آن می‌نویسیم
    post_type = filters.ChoiceFilter(
        label='نوع پست',
        choices=(('personal', 'شخصی'), ('business', 'کسب‌وکار/سازمان')),
        method='filter_by_post_type'
    )
    tag = filters.CharFilter(field_name='tags__name', lookup_expr='iexact')

    class Meta:
        model = Post
        # اینجا فقط فیلترهایی را که مستقیماً روی مدل Post هستند تعریف می‌کنیم
        # فیلترهای پیچیده‌تر را به صورت سفارشی در بالا تعریف کردیم
        fields = ['neighborhood', 'post_type', 'tag']

    def filter_by_post_type(self, queryset, name, value):
        """
        پست‌ها را بر اساس نوع نویسنده (شخصی یا تجاری/سازمانی) فیلتر می‌کند.
        """
        if value == 'personal':
            # پست‌هایی که نویسنده آنها پروفایل کسب‌وکار ندارد
            return queryset.filter(author__business_profile__isnull=True)
        elif value == 'business':
            # پست‌هایی که نویسنده آنها پروفایل کسب‌وکار دارد
            return queryset.filter(author__business_profile__isnull=False)
        return queryset