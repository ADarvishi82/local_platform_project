# posts/serializers.py
from rest_framework import serializers
from .models import Post, PostImage
from users.serializers import UserDisplaySerializer
from taggit.serializers import (TagListSerializerField, TaggitSerializer) # <<<< ایمپورت کنید


class PostImageSerializer(serializers.ModelSerializer):
    """
    سریالایزر برای نمایش عکس‌های یک پست.
    """
    class Meta:
        model = PostImage
        # فیلد 'image' به طور خودکار URL کامل را برمی‌گرداند
        fields = ['id', 'image']


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

    class Meta:
        model = Post
        fields = [
            'id', 'author', 'content', 
            'tags',
            'images', # برای نمایش لیست عکس‌ها
            'created_at', 'updated_at',
            'likes_count',
            'is_liked_by_user'
        ]
        # فیلد uploaded_images کاملاً حذف شده است
        read_only_fields = ('author', 'images', 'created_at', 'updated_at', 'likes_count')

    def get_is_liked_by_user(self, obj):
        request = self.context.get('request', None)
        if request and hasattr(request, "user") and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False