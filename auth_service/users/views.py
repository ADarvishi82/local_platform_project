# users/views.py
from rest_framework import viewsets, permissions, status, serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from .models import UserProfile, BusinessProfile, Category, Tag
from .serializers import (
    UserProfileSerializer,
    BusinessProfileSerializer,
    CategorySerializer,
    TagSerializer,
    UserDisplaySerializer # اگر بخواهید API برای لیست کاربران هم داشته باشید
)
from rest_framework.parsers import MultiPartParser, FormParser # اضافه کنید


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser) # << برای مدیریت آپلود فایل

    # ... متدهای get_queryset و perform_create شما بدون تغییر ...

    def get_queryset(self):
        # کاربران فقط می‌توانند پروفایل خودشان را ببینند (مگر اینکه ادمین باشند)
        if self.request.user.is_staff:
            return UserProfile.objects.all()
        return UserProfile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # هنگام ایجاد پروفایل، آن را به کاربر لاگین شده فعلی اختصاص بده
        # فرض می‌کنیم هر کاربر فقط یک پروفایل می‌تواند داشته باشد (به خاطر OneToOneField)
        # باید بررسی کنیم که کاربر قبلاً پروفایل نداشته باشد
        if UserProfile.objects.filter(user=self.request.user).exists():
            # می‌توانید یک خطا برگردانید یا پروفایل موجود را آپدیت کنید
            raise serializers.ValidationError({'detail': 'این کاربر قبلاً پروفایل دارد.'}, code=status.HTTP_400_BAD_REQUEST)
        serializer.save(user=self.request.user)

# ViewSet برای Category (معمولاً فقط خواندنی برای کاربران عادی)
class CategoryViewSet(viewsets.ReadOnlyModelViewSet): # فقط خواندنی (GET list, GET detail)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny] # همه می‌توانند دسته‌بندی‌ها را ببینند
    # اگر می‌خواهید ایجاد/آپدیت/حذف دسته‌بندی‌ها فقط توسط ادمین باشد، از ModelViewSet با permission مناسب استفاده کنید.

# ViewSet برای Tag (معمولاً فقط خواندنی برای کاربران عادی)
class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny] # همه می‌توانند تگ‌ها را ببینند

# ViewSet برای BusinessProfile
class BusinessProfileViewSet(viewsets.ModelViewSet):
    queryset = BusinessProfile.objects.all()
    serializer_class = BusinessProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] # کاربران لاگین شده می‌توانند ایجاد/آپدیت کنند، بقیه فقط می‌خوانند

    def get_queryset(self):
        # فیلتر کردن بر اساس پارامترهای query (مثال)
        queryset = BusinessProfile.objects.filter(is_verified=True) # فقط تایید شده‌ها را نمایش بده (یا همه اگر ادمین است)
        
        category_slug = self.request.query_params.get('category', None)
        if category_slug is not None:
            queryset = queryset.filter(category__slug=category_slug)
        
        # می‌توانید فیلترهای بیشتری اضافه کنید (بر اساس تگ، مکان و ...)
        return queryset

    def perform_create(self, serializer):
        # هنگام ایجاد پروفایل کسب‌وکار، آن را به کاربر لاگین شده فعلی اختصاص بده
        if BusinessProfile.objects.filter(user=self.request.user).exists():
            raise serializers.ValidationError({'detail': 'این کاربر قبلاً پروفایل کسب‌وکار دارد.'}, code=status.HTTP_400_BAD_REQUEST)
        serializer.save(user=self.request.user)

    # اکشن سفارشی برای دریافت پروفایل کسب‌وکار کاربر فعلی (اگر وجود داشته باشد)
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated], url_path='my-business')
    def my_business_profile(self, request):
        try:
            profile = BusinessProfile.objects.get(user=request.user)
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except BusinessProfile.DoesNotExist:
            return Response({'detail': 'پروفایل کسب‌وکار برای این کاربر یافت نشد.'}, status=status.HTTP_404_NOT_FOUND)

# (اختیاری) ViewSet برای نمایش لیست کاربران (فقط ادمین)
# class UserViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserDisplaySerializer
#     permission_classes = [permissions.IsAdminUser]