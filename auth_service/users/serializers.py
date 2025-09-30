# users/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, BusinessProfile , Category, Tag 
#from neighborhoods.serializers import NeighborhoodSimpleSerializer # <<<< سریالایزر ساده محله را import کنید

# ... (UserDisplaySerializer شما) ...
class UserDisplaySerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name','profile']

# ... (CategorySerializer و TagSerializer شما اگر اینجا هستند یا از جای دیگر import شده‌اند) ...
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']
        read_only_fields = ('slug',)

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']
        read_only_fields = ('slug',)


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserDisplaySerializer(read_only=True)
    profile_picture_url = serializers.SerializerMethodField(read_only=True)
    neighborhood = serializers.CharField(source='neighborhood.__str__', read_only=True, allow_null=True )                                                             # این از فیلد neighborhood در مدل UserProfile می‌خواند

    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'address_string', 'latitude', 'longitude',
            'profile_picture', # برای آپلود
            'profile_picture_url',
            'neighborhood', # <<<< اضافه شد
            'created_at', 'updated_at'
        ]
        read_only_fields = ('user', 'created_at', 'updated_at', 'profile_picture_url', 'neighborhood')
        extra_kwargs = {
            'profile_picture': {'write_only': True, 'required': False}
        }
    
    def get_profile_picture_url(self, obj):
        # ... (کد قبلی get_profile_picture_url) ...
        request = self.context.get('request')
        if obj.profile_picture and hasattr(obj.profile_picture, 'url'):
            if request:
                return request.build_absolute_uri(obj.profile_picture.url)
            return obj.profile_picture.url
        return None

class BusinessProfileSerializer(serializers.ModelSerializer):
    user = UserDisplaySerializer(read_only=True)
    category = CategorySerializer(read_only=True) # نمایش آبجکت کامل دسته‌بندی
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True, allow_null=True, required=False
    )
    tags = TagSerializer(many=True, read_only=True) # نمایش لیست آبجکت‌های تگ
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), source='tags', write_only=True, many=True, required=False
    )
    account_type_display = serializers.CharField(source='get_account_type_display', read_only=True)
    neighborhood = serializers.CharField(source='neighborhood.__str__', read_only=True, allow_null=True)    
    logo_url = serializers.SerializerMethodField(read_only=True) 

    class Meta:
        model = BusinessProfile
        fields = [
            'id', 'user', 'account_type', 'account_type_display', 'business_name',
            'category', 'category_id', 
            'tags', 'tag_ids',
            'neighborhood', # <<<< اضافه شد
            'description', 'address_string', 'latitude', 'longitude',
            'phone_number', 'website', 
            'logo', # برای آپلود لوگو
            'logo_url', # برای نمایش URL لوگو
            'price_string',     # <<<< اضافه شد
            'base_price',       # <<<< اضافه شد
            'average_rating',   # <<<< اضافه شد
            'rating_count',     
            'is_verified', 'created_at', 'updated_at'
        ]
        read_only_fields = ('user', 'is_verified', 'created_at', 'updated_at', 'neighborhood', 'logo_url')
        extra_kwargs = {
            'logo': {'write_only': True, 'required': False} # برای آپلود، فقط write_only و اختیاری
        }

    def get_logo_url(self, obj): # اضافه کردن متد برای دریافت URL لوگو
        request = self.context.get('request')
        if obj.logo and hasattr(obj.logo, 'url'):
            if request:
                return request.build_absolute_uri(obj.logo.url)
            return obj.logo.url
        return None

# ... (UserProfileSimpleSerializer و BusinessProfileSimpleSerializer شما از قبل اینجا هستند) ...
class UserProfileSimpleSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    profile_picture_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'profile_picture_url'] 
    
    def get_profile_picture_url(self, obj):
        request = self.context.get('request')
        if obj.profile_picture and hasattr(obj.profile_picture, 'url'):
            if request: return request.build_absolute_uri(obj.profile_picture.url)
            return obj.profile_picture.url
        return None

class BusinessProfileSimpleSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True, allow_null=True)
    logo_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = BusinessProfile
        fields = ['id', 'business_name', 'category_name', 'logo_url', 'address_string']
    
    def get_logo_url(self, obj):
        request = self.context.get('request')
        if obj.logo and hasattr(obj.logo, 'url'):
            if request: return request.build_absolute_uri(obj.logo.url)
            return obj.logo.url
        return None
    

class UserProfileForDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'profile_picture_url'] # فقط ID و URL عکس کافی است
    
    # get_profile_picture_url را از UserProfileSerializer اصلی می‌توانید اینجا هم کپی کنید
    # یا اگر UserProfileSerializer شما این را دارد، می‌توانید از آن ارث‌بری کنید
    # برای سادگی، فرض می‌کنیم URL عکس به روش دیگری (مثلاً property در مدل) در دسترس است
    # یا اینکه سریالایزر اصلی UserProfile شما این را مدیریت می‌کند.
    # یک راه ساده‌تر:
    profile_picture_url = serializers.CharField(source='get_absolute_image_url', read_only=True) # فرض می‌کنیم متدی با این نام در مدل دارید

class BusinessProfileForDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessProfile
        fields = ['id', 'logo_url'] # فقط ID و URL لوگو
    logo_url = serializers.CharField(source='get_absolute_logo_url', read_only=True)


# سریالایزر اصلی برای نمایش کاربر (که در PostSerializer استفاده می‌شود)
class UserDisplaySerializer(serializers.ModelSerializer):
    # از 'source' استفاده می‌کنیم تا به رابطه‌های OneToOne دسترسی پیدا کنیم
    # 'allow_null=True' مهم است چون یک کاربر ممکن است یکی از این پروفایل‌ها را نداشته باشد
    #profile = serializers.PrimaryKeyRelatedField(read_only=True, allow_null=True) # ID پروفایل کاربری
    #business_profile = serializers.PrimaryKeyRelatedField(read_only=True, allow_null=True) # ID پروفایل کسب‌وکار
    profile = UserProfileSimpleSerializer(read_only=True, allow_null=True)
    business_profile = BusinessProfileSimpleSerializer(read_only=True, allow_null=True)
    # یا اگر می‌خواهید اطلاعات بیشتری از پروفایل‌ها را برگردانید:
    # profile = UserProfileForDisplaySerializer(read_only=True, allow_null=True)
    # business_profile = BusinessProfileForDisplaySerializer(read_only=True, allow_null=True)

    class Meta:
        model = User # یا مدل کاربر سفارشی شما
        fields = ['pk', 'username', 'email', 'first_name', 'last_name', 'profile', 'business_profile']