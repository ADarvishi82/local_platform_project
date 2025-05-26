# users/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, BusinessProfile, Category, Tag

# سریالایزر برای مدل User (فقط برای نمایش اطلاعات، نه ایجاد یا آپدیت مستقیم User از اینجا)
class UserDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


from .models import UserProfile 

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserDisplaySerializer(read_only=True)
    profile_picture_url = serializers.SerializerMethodField(read_only=True) 
    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'address_string', 'latitude', 'longitude',
            'profile_picture', # خود فیلد برای آپلود
            'profile_picture_url', # فیلد سفارشی برای نمایش URL
            'created_at', 'updated_at'
        ]
        read_only_fields = ('user', 'created_at', 'updated_at', 'profile_picture_url')
        extra_kwargs = {
            'profile_picture': {'write_only': True, 'required': False} 
        }
    
    def get_profile_picture_url(self, obj):
        request = self.context.get('request')
        if obj.profile_picture and hasattr(obj.profile_picture, 'url'):
            if request:
                return request.build_absolute_uri(obj.profile_picture.url)
            return obj.profile_picture.url
        return None




# سریالایزر برای Category
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug'] # 'parent', 'icon' را هم اضافه کنید اگر دارید
        read_only_fields = ('slug',) # اسلاگ به طور خودکار ساخته می‌شود

# سریالایزر برای Tag
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']
        read_only_fields = ('slug',)

# سریالایزر برای BusinessProfile
class BusinessProfileSerializer(serializers.ModelSerializer):
    user = UserDisplaySerializer(read_only=True) # نمایش اطلاعات کاربر مدیر (فقط خواندنی)
    category = CategorySerializer(read_only=True) # نمایش اطلاعات دسته‌بندی (فقط خواندنی)
    # برای ایجاد/آپدیت، ID دسته‌بندی را می‌گیریم:
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True, allow_null=True, required=False
    )

    tags = TagSerializer(many=True, read_only=True) # نمایش لیست تگ‌ها (فقط خواندنی)
    # برای ایجاد/آپدیت، لیستی از ID های تگ‌ها را می‌گیریم:
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), source='tags', write_only=True, many=True, required=False
    )

    # نمایش نام فارسی account_type
    account_type_display = serializers.CharField(source='get_account_type_display', read_only=True)


    class Meta:
        model = BusinessProfile
        fields = [
            'id', 'user', 'account_type', 'account_type_display', 'business_name',
            'category', 'category_id', 'tags', 'tag_ids',
            'description', 'address_string', 'latitude', 'longitude',
            'phone_number', 'website', # 'logo' را هم اضافه کنید اگر دارید و برایش راه‌حل آپلود فایل دارید
            'is_verified', 'created_at', 'updated_at'
        ]
        read_only_fields = ('user', 'is_verified', 'created_at', 'updated_at') # کاربر و وضعیت تایید توسط ادمین یا منطق دیگر مدیریت می‌شود

    # می‌توانید متدهای create و update را برای مدیریت خاص ایجاد/آپدیت پروفایل کسب‌وکار بازنویسی کنید
    # به خصوص اگر می‌خواهید پروفایل به کاربر لاگین شده فعلی اختصاص یابد.
    # def create(self, validated_data):
    #     # ... منطق اختصاص کاربر ...
    #     return super().create(validated_data)