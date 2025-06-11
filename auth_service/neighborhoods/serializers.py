# neighborhoods/serializers.py
from rest_framework import serializers
from .models import Neighborhood
# سریالایزرهای ساده شده برای نمایش در لیست محله (برای جلوگیری از circular import و حجم زیاد داده)
from users.serializers import UserProfileSimpleSerializer, BusinessProfileSimpleSerializer 
# شما باید این سریالایزرهای Simple را در users/serializers.py بسازید
# که فقط شامل فیلدهای ضروری مانند id، نام، و شاید عکس باشند.

class NeighborhoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Neighborhood
        fields = ['id', 'name', 'city', 'center_latitude', 'center_longitude']
        
        
class NeighborhoodSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Neighborhood
        fields = ['id', 'name', 'city']

class NeighborhoodDetailSerializer(serializers.ModelSerializer):
    user_profiles_in_neighborhood = UserProfileSimpleSerializer(many=True, read_only=True)
    business_profiles_in_neighborhood = BusinessProfileSimpleSerializer(many=True, read_only=True)
    
    # برای نمایش تعداد (به جای لیست کامل که ممکن است سنگین باشد)
    user_profile_count = serializers.SerializerMethodField()
    business_profile_count = serializers.SerializerMethodField()

    class Meta:
        model = Neighborhood
        fields = [
            'id', 'name', 'city', 'center_latitude', 'center_longitude', 
            'user_profile_count', 'business_profile_count',
            'user_profiles_in_neighborhood', 
            'business_profiles_in_neighborhood'
        ]
    
    def get_user_profile_count(self, obj):
        return obj.user_profiles_in_neighborhood.count()

    def get_business_profile_count(self, obj):
        return obj.business_profiles_in_neighborhood.count()