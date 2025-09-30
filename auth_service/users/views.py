# users/views.py
from rest_framework import viewsets, permissions, status, serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from .models import UserProfile, BusinessProfile, Category, Tag
from .serializers import (UserProfileSerializer, BusinessProfileSerializer, CategorySerializer, TagSerializer, UserDisplaySerializer) # اگر بخواهید API برای لیست کاربران هم داشته باشید)
from rest_framework.parsers import MultiPartParser, FormParser # اضافه کنید
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken # برای ایجاد توکن JWT
from google.oauth2 import id_token
from google.auth.transport import requests
from posts.models import Post # مدل Post را import کنید
from posts.serializers import PostSerializer # سریالایزر Post را import کنید
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from neighborhoods.models import Neighborhood # import کنید
from posts.models import Post # import کنید
from django_filters.rest_framework import DjangoFilterBackend
from .filters import BusinessProfileFilter

class MyNeighborhoodStatsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        user_neighborhood = None

        try:
            if hasattr(user, 'profile') and user.profile.neighborhood:
                user_neighborhood = user.profile.neighborhood
            elif hasattr(user, 'business_profile') and user.business_profile.neighborhood:
                user_neighborhood = user.business_profile.neighborhood
        except:
            pass

        if not user_neighborhood:
            return Response({'error': 'محله‌ای برای شما ثبت نشده است.'}, status=status.HTTP_404_NOT_FOUND)

        stats_data = {
            'id': user_neighborhood.id,
            'name': user_neighborhood.name,
            'city': user_neighborhood.city,
            'resident_count': user_neighborhood.user_profiles_in_neighborhood.count(),
            'business_count': user_neighborhood.business_profiles_in_neighborhood.count(),
            'post_count': Post.objects.filter(neighborhood=user_neighborhood).count()
        }
        return Response(stats_data)


User = get_user_model()

class GoogleLoginAPIView(APIView):
    """
    یک API View برای مدیریت ثبت‌نام و ورود کاربران با استفاده از Google ID Token.
    """
    # این endpoint نیازی به توکن احراز هویت ما ندارد، چون خودش قرار است توکن تولید کند.
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        # 1. گرفتن id_token از بدنه درخواست
        token = request.data.get('id_token')
        if not token:
            return Response(
                {'error': 'فیلد id_token الزامی است.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # 2. تأیید اعتبار id_token با سرورهای گوگل
            # CLIENT_ID را از تنظیمات (settings.py) یا یک متغیر محیطی بخوانید.
            # برای سادگی، فعلاً آن را مستقیم اینجا قرار می‌دهیم.
            # در پروژه واقعی، این را به settings.py منتقل کنید.
            # GOOGLE_CLIENT_ID = settings.GOOGLE_CLIENT_ID
            GOOGLE_CLIENT_ID = "279929399898-ir6jp70mc46v6pjojnrdl2veg3ta44h2.apps.googleusercontent.com" # <<<< Client ID خودتان را اینجا قرار دهید
            
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)

            # 3. استخراج اطلاعات کاربر از توکن تأیید شده
            email = idinfo.get('email')
            first_name = idinfo.get('given_name', '')
            last_name = idinfo.get('family_name', '')
            # می‌توانید اطلاعات دیگری مانند URL عکس پروفایل را هم بگیرید:
            # profile_picture_url = idinfo.get('picture')

            if not email:
                return Response({'error': 'ایمیل در توکن گوگل یافت نشد.'}, status=status.HTTP_400_BAD_REQUEST)

            # 4. پیدا کردن کاربر موجود با این ایمیل یا ایجاد یک کاربر جدید
            user = User.objects.filter(email=email).first()

            if user:
                # اگر کاربر از قبل وجود دارد، فقط نام او را (اگر خالی است) به‌روزرسانی می‌کنیم
                updated = False
                if not user.first_name and first_name:
                    user.first_name = first_name
                    updated = True
                if not user.last_name and last_name:
                    user.last_name = last_name
                    updated = True
                
                if updated:
                    user.save(update_fields=['first_name', 'last_name'])
            else:
                # اگر کاربر وجود ندارد، یک کاربر جدید ایجاد می‌کنیم
                # یک نام کاربری یکتا بر اساس بخش اول ایمیل ایجاد می‌کنیم
                username_base = email.split('@')[0]
                username = username_base
                counter = 1
                while User.objects.filter(username=username).exists():
                    username = f"{username_base}{counter}"
                    counter += 1
                
                user = User.objects.create(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name
                )
                # برای کاربران اجتماعی، یک پسورد غیرقابل استفاده تنظیم می‌کنیم
                user.set_unusable_password()
                user.save()

                # (اختیاری) می‌توانید اینجا بر اساس منطق خود، یک UserProfile خالی هم برای او ایجاد کنید
                # from .models import UserProfile
                # UserProfile.objects.create(user=user)

            # 5. ایجاد توکن‌های JWT (Access و Refresh) برای کاربر
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            
            # 6. آماده‌سازی و ارسال پاسخ موفقیت‌آمیز
            user_serializer = UserDisplaySerializer(user)

            return Response({
                'access_token': access_token,
                'refresh_token': str(refresh),
                'user': user_serializer.data,
                # 'key' را هم برای سازگاری با پاسخ پیش‌فرض dj-rest-auth اضافه می‌کنیم
                'key': access_token,
            }, status=status.HTTP_200_OK)

        except ValueError as e:
            # این خطا معمولاً زمانی رخ می‌دهد که توکن نامعتبر باشد
            print(f"Google token verification failed: {e}")
            return Response({'error': 'توکن گوگل نامعتبر است.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # مدیریت خطاهای پیش‌بینی نشده دیگر
            print(f"An unexpected error occurred during Google login: {e}")
            # در حالت DEBUG، می‌توانید جزئیات خطا را برگردانید
            # return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response({'error': 'یک خطای پیش‌بینی نشده رخ داد.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser) # برای آپلود فایل عکس پروفایل

    def get_queryset(self):
        # کاربر فقط می‌تواند پروفایل خودش را ببیند و ویرایش کند
        return UserProfile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # هنگام ایجاد پروفایل، آن را به کاربر لاگین شده فعلی اختصاص بده
        if UserProfile.objects.filter(user=self.request.user).exists():
            raise serializers.ValidationError(
                {'detail': 'این کاربر قبلاً پروفایل دارد. برای تغییر، از متد PUT یا PATCH استفاده کنید.'},
                code=status.HTTP_400_BAD_REQUEST
            )
        serializer.save(user=self.request.user)
        
        # یک اکشن برای دریافت/آپدیت پروفایل کاربر فعلی
    # اگر پروفایل وجود نداشت، می‌توانیم اجازه دهیم با POST به همین endpoint ساخته شود
    # یا اینکه کلاینت خودش تشخیص دهد و به endpoint لیست (POST /api/user-profiles/) بفرستد.
    # برای سادگی، فرض می‌کنیم کلاینت خودش POST یا PUT/PATCH را به endpoint درست می‌زند.
    # اما یک GET برای پروفایل فعلی مفید است:
    @action(detail=False, methods=['get'], url_path='me', url_name='my-profile')
    def my_profile(self, request):
        try:
            profile = UserProfile.objects.get(user=request.user)
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response({'detail': 'پروفایل برای این کاربر یافت نشد.'}, status=status.HTTP_404_NOT_FOUND)

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
    queryset = BusinessProfile.objects.filter(is_verified=True) # <<<< queryset اصلی را اینجا تعریف کنید
    serializer_class = BusinessProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] # کاربران لاگین شده می‌توانند ایجاد/آپدیت کنند، بقیه فقط می‌خوانند

    filter_backends = (DjangoFilterBackend,)
    filterset_class = BusinessProfileFilter
    def list(self, request, *args, **kwargs):
        print("="*30)
        print("DEBUG: Received request for BusinessProfile list.")
        print("DEBUG: Query Parameters received:", request.query_params)
        print("="*30)
        
        # بقیه منطق به صورت عادی ادامه پیدا می‌کند
        return super().list(request, *args, **kwargs)
    
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
        
    @action(detail=True, methods=['get'], url_path='posts')
    def posts(self, request, pk=None):
        business_profile = self.get_object()

        # ***** بهینه‌سازی QuerySet *****
        posts_queryset = Post.objects.filter(
            related_business=business_profile,
            visibility='PUBLIC'
        ).select_related(
            'author__profile', # برای دسترسی به پروفایل شخصی نویسنده (اگر لازم است)
            'author__business_profile' # برای دسترسی به پروفایل کسب‌وکار نویسنده (اگر لازم است)
        ).prefetch_related(
            'images', # برای واکشی تمام عکس‌های هر پست در یک کوئری
            'tags',   # برای واکشی تمام تگ‌های هر پست در یک کوئری
            'likes'   # برای بررسی is_liked_by_user
        ).order_by('-created_at')

        # حالا که تمام داده‌ها به صورت بهینه واکشی شده‌اند، سریالایزر به درستی کار خواهد کرد.
        serializer = PostSerializer(posts_queryset, many=True, context={'request': request})
        return Response(serializer.data)

# (اختیاری) ViewSet برای نمایش لیست کاربران (فقط ادمین)
# class UserViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserDisplaySerializer
#     permission_classes = [permissions.IsAdminUser]

class UserPostsAPIView(ListAPIView):
    """
    یک API View برای نمایش لیست پست‌های یک کاربر خاص.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny] # همه می‌توانند پست‌های عمومی یک کاربر را ببینند

    def get_queryset(self):
        # ID کاربر را از پارامتر URL (user_id) بگیرید
        user_id = self.kwargs.get('user_id')
        try:
            user = User.objects.get(pk=user_id)
            # پست‌ها را بر اساس نویسنده فیلتر کن
            # می‌توانید اینجا منطق visibility را هم اضافه کنید
            # مثلاً اگر کاربر درخواست دهنده، خود نویسنده نیست، فقط پست‌های عمومی را نشان بده
            if self.request.user == user:
                # اگر کاربر پروفایل خودش را می‌بیند، همه پست‌هایش را نشان بده
                return Post.objects.filter(author=user)
            else:
                # اگر کاربر دیگری پروفایل را می‌بیند، فقط پست‌های عمومی را نشان بده
                return Post.objects.filter(author=user, visibility='PUBLIC')
        except User.DoesNotExist:
            return Post.objects.none()