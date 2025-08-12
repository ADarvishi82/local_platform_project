# posts/serializers.py
from rest_framework import serializers
from .models import Post, PostImage,Comment,Like, Event, Rating
from users.serializers import UserDisplaySerializer
from taggit.serializers import (TagListSerializerField, TaggitSerializer) # <<<< ایمپورت کنید
#from rest_framework import serializers


class PostImageSerializer(serializers.ModelSerializer):
    """
    سریالایزر برای نمایش عکس‌های یک پست.
    """
    class Meta:
        model = PostImage
        # فیلد 'image' به طور خودکار URL کامل را برمی‌گرداند
        fields = ['id', 'image']
        
class CommentSerializer(serializers.ModelSerializer):
    author = UserDisplaySerializer(read_only=True)
    # برای کامنت‌های تو در تو، می‌توانید فیلد replies را هم اضافه کنید
    #replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        # فیلدهای post و parent فقط برای نوشتن هستند (کلاینت آنها را می‌فرستد)
        fields = ['id', 'author', 'post', 'content', 'parent', 'created_at', 'updated_at']
        read_only_fields = ('author', 'created_at', 'updated_at')
        extra_kwargs = {
            'post': {'write_only': True},
            'parent': {'write_only': True, 'required': False, 'allow_null': True}
        }


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    """
    سریالایزر برای مدل Post.
    اطلاعات نویسنده و عکس‌ها را به صورت فقط خواندنی نمایش می‌دهد.
    """
    author = UserDisplaySerializer(read_only=True)
    is_liked_by_user = serializers.SerializerMethodField()

    # نمایش لیستی از عکس‌ها با استفاده از سریالایزر بالا
    images = PostImageSerializer(many=True, read_only=True)
    tags = TagListSerializerField(required=False) # این فیلد لیستی از رشته‌های تگ را می‌پذیرد و نمایش می‌دهد
    visibility_display = serializers.CharField(source='get_visibility_display', read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'author', 'content', 
            'tags',
            'images', # برای نمایش لیست عکس‌ها
            'visibility', # <<<< اضافه شد (برای نوشتن)
            'visibility_display', # <<<< اضافه شد (برای خواندن)
            'post_type', # <<<< اضافه شد
            'is_pinned', # <<<< اضافه شد
            'neighborhood', # اگر می‌خواهید اطلاعات محله را هم نشان دهید
            'created_at', 'updated_at',
            'likes_count',
            'comments_count',
            'is_liked_by_user'
        ]
        # فیلد uploaded_images کاملاً حذف شده است
        read_only_fields = ('author', 'images', 'created_at', 'updated_at','is_pinned', 
                            'likes_count', 'comments_count', 'visibility_display', 'neighborhood')
    def get_is_liked_by_user(self, obj):
        request = self.context.get('request', None)
        if request and hasattr(request, "user") and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False
    


class EventSerializer(serializers.ModelSerializer):
    neighborhood_name = serializers.CharField(source='neighborhood.name', read_only=True)
    creator_username = serializers.CharField(source='creator.username', read_only=True, allow_null=True)

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'neighborhood', 'neighborhood_name',
            'creator', 'creator_username', 'start_time', 'end_time', 'location_name',
            'is_approved', 'created_at'
        ]
        # برای ایجاد، فیلدهای کمتری از کاربر می‌گیریم
        read_only_fields = ('creator', 'is_approved', 'created_at', 'neighborhood_name', 'creator_username')
        
class RatingSerializer(serializers.ModelSerializer):
    """
    سریالایزر برای ایجاد و نمایش امتیازها.
    """
    author = UserDisplaySerializer(source='user', read_only=True) # نمایش اطلاعات کاربری که امتیاز داده

    class Meta:
        model = Rating
        fields = ['id', 'author', 'business_profile', 'score', 'created_at']
        read_only_fields = ('author', 'created_at')
        # business_profile و score باید توسط کلاینت ارسال شوند
        # پس آنها را write_only می‌کنیم تا در پاسخ GET تکراری نباشند (اختیاری)
        extra_kwargs = {
            'business_profile': {'write_only': True},
        }