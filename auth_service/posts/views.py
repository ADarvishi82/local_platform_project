# posts/views.py
from rest_framework import viewsets, permissions, status, serializers
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Post, Like, PostImage,Comment
from .serializers import PostSerializer,CommentSerializer
from django.db.models import Q # برای کوئری‌های پیچیده OR
from django_filters.rest_framework import DjangoFilterBackend # <<<< این را import کنید
from .filters import PostFilter
from taggit.models import Tag # <<<< مدل Tag را از taggit import کنید
from django.db.models import Count # برای شمارش
from rest_framework.views import APIView # <<<< این import باید اضافه شود
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated # <<<< این را import کنید
from django.utils import timezone
from .models import Event
from .serializers import EventSerializer
from .models import Rating
from .serializers import RatingSerializer

# می‌توانید این را به عنوان یک APIView جداگانه بسازید
class PopularTagsAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        # تگ‌ها را بر اساس تعداد پست‌هایی که به آنها متصل هستند، شمارش و مرتب کن
        # و مثلا ۱۰ تگ برتر را برگردان
        popular_tags = Tag.objects.annotate(
            num_posts=Count('taggit_taggeditem_items') # related_name داخلی taggit
        ).order_by('-num_posts')[:10] # ۱۰ تگ برتر

        # نتیجه را به فرمت دلخواه درآور
        tags_data = [{'name': tag.name, } for tag in popular_tags]
        
        return Response(tags_data)

# یا می‌توانید این را به عنوان یک اکشن در PostViewSet اضافه کنید (که شاید خیلی مرتبط نباشد)


# کلاس Permission در همین فایل تعریف می‌شود
class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
    


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = (MultiPartParser, FormParser)


    # ***** تنظیمات جدید برای فیلترینگ *****
    filter_backends = (DjangoFilterBackend,) # به DRF می‌گوییم از این بک‌اند استفاده کن
    filterset_class = PostFilter # کلاس فیلتر خودمان را معرفی می‌کنیم
    
    
    def get_queryset(self):
        # منطق قبلی برای visibility همچنان مهم است
        # ما آن را با فیلترینگ جدید ترکیب می‌کنیم
        user = self.request.user
        if not user.is_authenticated:
            return Post.objects.filter(visibility='PUBLIC')

        try:
            user_neighborhood = user.profile.neighborhood if hasattr(user, 'profile') and user.profile.neighborhood else None
            if not user_neighborhood and hasattr(user, 'business_profile') and user.business_profile.neighborhood:
                user_neighborhood = user.business_profile.neighborhood

            if user_neighborhood:
                return Post.objects.filter(
                    Q(visibility='PUBLIC') | 
                    Q(visibility='NEIGHBORHOOD', neighborhood=user_neighborhood)
                ).distinct()
            else:
                return Post.objects.filter(visibility='PUBLIC')
        
        except (AttributeError, user.profile.RelatedObjectDoesNotExist, user.business_profile.RelatedObjectDoesNotExist):
             return Post.objects.filter(visibility='PUBLIC')


        # فیلتر بر اساس تگ (همچنان کار می‌کند)
        tag_name = self.request.query_params.get('tag', None)
        if tag_name:
            queryset = queryset.filter(tags__name__in=[tag_name])
        
        # بر اساس جدیدترین مرتب کن و برگردان
        return queryset.order_by('-created_at').distinct() # distinct برای جلوگیری از نتایج تکراری در کوئری‌های پیچیده

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsAuthorOrReadOnly()]
        if self.action == 'like':
            return [permissions.IsAuthenticated()]
        return super().get_permissions()
    
    def perform_create(self, serializer):
        """
        یک پست جدید ایجاد می‌کند و به طور خودکار محله نویسنده را به آن متصل می‌کند.
        """
        author = self.request.user
        post_neighborhood = None

        # همیشه سعی کن محله نویسنده را پیدا کنی
        try:
            if hasattr(author, 'profile') and author.profile.neighborhood:
                post_neighborhood = author.profile.neighborhood
            elif hasattr(author, 'business_profile') and author.business_profile.neighborhood:
                post_neighborhood = author.business_profile.neighborhood
        except (AttributeError, author.profile.RelatedObjectDoesNotExist, author.business_profile.RelatedObjectDoesNotExist):
            # اگر کاربر پروفایل یا محله ندارد، مشکلی نیست. post_neighborhood برابر None باقی می‌ماند.
            pass

        # اگر visibility محله‌ای است اما کاربر محله ندارد، خطا بده
        visibility = serializer.validated_data.get('visibility', 'PUBLIC')
        if visibility == 'NEIGHBORHOOD' and not post_neighborhood:
            # از serializers.ValidationError استفاده می‌کنیم تا پاسخ 400 Bad Request برگردانده شود
            raise serializers.ValidationError(
                {'detail': 'برای ارسال پست فقط برای هم‌محله‌ای‌ها، ابتدا باید محله خود را در پروفایل مشخص کنید.'}
            )

        # پست را با نویسنده و محله (اگر پیدا شد) ذخیره کن
        post_instance = serializer.save(author=self.request.user, neighborhood=post_neighborhood)
        
        # عکس‌ها را ذخیره کن
        images_data = self.request.FILES.getlist('uploaded_images')
        for image_data in images_data:
            PostImage.objects.create(post=post_instance, image=image_data)

    

    @action(detail=True, methods=['post'], url_path='like')
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        try:
            like = Like.objects.get(user=user, post=post)
            like.delete()
            return Response({'status': 'unliked'}, status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            Like.objects.create(user=user, post=post)
            return Response({'status': 'liked'}, status=status.HTTP_201_CREATED)
        
        
class CommentViewSet(viewsets.ModelViewSet):
    """
    یک ViewSet برای مشاهده و مدیریت کامنت‌ها.
    """
    queryset = Comment.objects.all().select_related('author__profile') # بهینه‌سازی برای گرفتن پروفایل نویسنده
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend] # اگر قبلاً اضافه نکرده‌اید
    filterset_fields = ['post'] # <<<< روش ساده‌تر و استانداردتر برای فیلتر

    def get_permissions(self):
        """
        دسترسی ویرایش/حذف را فقط به نویسنده کامنت محدود می‌کند.
        """
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsCommentAuthorOrReadOnly()]
        return super().get_permissions()

    def perform_create(self, serializer):
        """
        هنگام ایجاد کامنت، نویسنده را به کاربر لاگین شده فعلی تنظیم می‌کند.
        فیلد 'post' باید توسط کلاینت در بدنه درخواست ارسال شود.
        """
        # serializer.save() داده‌های اعتبارسنجی شده را می‌گیرد
        # و ما author را به صورت یک kwarg اضافی به آن پاس می‌دهیم.
        serializer.save(author=self.request.user)

    # get_queryset قبلی را می‌توانیم با استفاده از django-filter ساده‌تر کنیم
    # def get_queryset(self):
    #     post_id = self.request.query_params.get('post_id')
    #     if post_id:
    #         return Comment.objects.filter(post_id=post_id).select_related('author')
    #     return super().get_queryset()

class ImportantNewsAPIView(ListAPIView):
    """
    API برای نمایش لیست اخبار مهم (پست‌های سنجاق شده از نوع خبر)
    برای محله کاربر لاگین شده.
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated] # <<<< فقط کاربران لاگین شده می‌توانند این را ببینند

    def get_queryset(self):
        user = self.request.user
        user_neighborhood = None

        # محله کاربر را از پروفایل‌هایش پیدا کن
        try:
            if hasattr(user, 'profile') and user.profile.neighborhood:
                user_neighborhood = user.profile.neighborhood
            elif hasattr(user, 'business_profile') and user.business_profile.neighborhood:
                user_neighborhood = user.business_profile.neighborhood
        except (AttributeError, user.profile.RelatedObjectDoesNotExist, user.business_profile.RelatedObjectDoesNotExist):
            # اگر کاربر پروفایل ندارد یا پروفایلش محله ندارد
            return Post.objects.none() # لیست خالی برگردان

        # اگر کاربر محله‌ای ندارد، لیست خالی برگردان
        if not user_neighborhood:
            return Post.objects.none()

        # پست‌هایی را که از نوع 'NEWS' هستند، سنجاق شده‌اند، و مربوط به محله کاربر هستند، برگردان
        # و مثلا ۵ مورد آخر را نمایش می‌دهد.
        queryset = Post.objects.filter(
            post_type='NEWS', 
            is_pinned=True, 
            neighborhood=user_neighborhood
        ).order_by('-created_at')[:5]
        
        return queryset
    
class UpcomingEventsAPIView(ListAPIView):
    """
    API برای نمایش لیست رویدادهای آینده (تایید شده)
    برای محله کاربر لاگین شده.
    """
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        print(f"DEBUG: Checking upcoming events for user: {user.username}")

        user_neighborhood = None
        try:
            if hasattr(user, 'profile') and user.profile.neighborhood:
                user_neighborhood = user.profile.neighborhood
            elif hasattr(user, 'business_profile') and user.business_profile.neighborhood:
                user_neighborhood = user.business_profile.neighborhood
        except:
            pass

        print(f"DEBUG: User's neighborhood found: {user_neighborhood}")

        if not user_neighborhood:
            print("DEBUG: User has no neighborhood. Returning empty list.")
            return Event.objects.none()

        now = timezone.now()
        print(f"DEBUG: Current time (UTC): {now}")

        queryset = Event.objects.filter(
            is_approved=True,
            neighborhood=user_neighborhood,
            start_time__gte=now
        ).order_by('start_time')[:5]
        
        print(f"DEBUG: Found {queryset.count()} upcoming events in this neighborhood.")
        for event in queryset:
            print(f"  - Event: '{event.title}', Start time: {event.start_time}")

        return queryset
    
class RatingViewSet(viewsets.ModelViewSet):
    """
    یک ViewSet برای مدیریت امتیازهای کسب‌وکارها.
    """
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_fields = ['user', 'business_profile']

    def perform_create(self, serializer):
        # نویسنده امتیاز را به کاربر لاگین شده فعلی تنظیم می‌کند
        serializer.save(user=self.request.user)