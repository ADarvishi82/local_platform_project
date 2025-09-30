# neighborhoods/utils.py
from geopy.distance import geodesic
from .models import Neighborhood # از مدل Neighborhood در همین اپلیکیشن

def assign_neighborhood_to_profile(profile_instance):
    """
    نزدیک‌ترین محله را به یک نمونه پروفایل (UserProfile یا BusinessProfile)
    بر اساس مختصات آن اختصاص می‌دهد.
    پروفایل باید فیلدهای latitude, longitude و neighborhood داشته باشد.
    """
    if profile_instance.latitude is None or profile_instance.longitude is None:
        profile_instance.neighborhood = None # اگر مختصات ندارد، محله‌ای ندارد
        # profile_instance.save(update_fields=['neighborhood']) # اگر می‌خواهید بلافاصله ذخیره شود
        return False # نشان‌دهنده عدم موفقیت در تخصیص

    profile_coords = (profile_instance.latitude, profile_instance.longitude)
    
    closest_neighborhood = None
    min_distance = float('inf')

    # تمام محله‌های موجود را از دیتابیس بگیر
    # برای بهینه‌سازی، اگر تعداد محله‌ها خیلی زیاد است، می‌توانید فقط محله‌های یک شهر خاص را بگیرید
    # یا از کوئری‌های مکانی دیتابیس استفاده کنید.
    all_neighborhoods = Neighborhood.objects.all() 
    if not all_neighborhoods.exists():
        profile_instance.neighborhood = None
        return False # هیچ محله‌ای برای تخصیص وجود ندارد

    for hood in all_neighborhoods:
        if hood.center_latitude is not None and hood.center_longitude is not None:
            hood_coords = (hood.center_latitude, hood.center_longitude)
            distance = geodesic(profile_coords, hood_coords).km
            if distance < min_distance:
                min_distance = distance
                closest_neighborhood = hood
    
    if closest_neighborhood:
        profile_instance.neighborhood = closest_neighborhood
        # profile_instance.save(update_fields=['neighborhood']) # اگر می‌خواهید بلافاصله ذخیره شود
        return True # نشان‌دهنده موفقیت در تخصیص
    
    profile_instance.neighborhood = None # اگر هیچ محله نزدیکی پیدا نشد
    return False