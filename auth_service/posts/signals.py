# posts/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Like,Comment, Rating 
from django.db.models import Avg # 

@receiver(post_save, sender=Like)
def increment_like_count(sender, instance, created, **kwargs):
    """
    وقتی یک لایک جدید ایجاد می‌شود، تعداد لایک‌های پست مربوطه را یکی زیاد کن.
    """
    if created:
        instance.post.likes_count += 1
        instance.post.save(update_fields=['likes_count'])

@receiver(post_delete, sender=Like)
def decrement_like_count(sender, instance, **kwargs):
    """
    وقتی یک لایک حذف می‌شود (آنلایک)، تعداد لایک‌های پست مربوطه را یکی کم کن.
    """
    instance.post.likes_count -= 1
    instance.post.save(update_fields=['likes_count'])
    
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

@receiver(post_save, sender=Comment)
def increment_comment_count(sender, instance, created, **kwargs):
    """
    وقتی یک کامنت جدید ایجاد می‌شود، تعداد کامنت‌های پست مربوطه را یکی زیاد کن.
    """
    if created:
        instance.post.comments_count += 1
        instance.post.save(update_fields=['comments_count'])

@receiver(post_delete, sender=Comment)
def decrement_comment_count(sender, instance, **kwargs):
    """
    وقتی یک کامنت حذف می‌شود، تعداد کامنت‌های پست مربوطه را یکی کم کن.
    """
    instance.post.comments_count -= 1
    instance.post.save(update_fields=['comments_count'])
    
@receiver([post_save, post_delete], sender=Rating)
def update_business_profile_rating(sender, instance, **kwargs):
    """
    پس از هر ایجاد یا حذف امتیاز، میانگین امتیاز و تعداد امتیازهای
    کسب‌وکار مربوطه را دوباره محاسبه و ذخیره می‌کند.
    """
    business_profile = instance.business_profile
    ratings_queryset = Rating.objects.filter(business_profile=business_profile)
    
    # تعداد امتیازها را آپدیت کن
    business_profile.rating_count = ratings_queryset.count()
    
    # میانگین امتیازها را آپدیت کن
    # .aggregate یک دیکشنری برمی‌گرداند، مثلاً {'score__avg': 4.5}
    average = ratings_queryset.aggregate(Avg('score'))['score__avg']
    business_profile.average_rating = average or 0.0 # اگر هیچ امتیازی نباشد (پس از حذف آخرین امتیاز)، میانگین را صفر کن
    
    business_profile.save(update_fields=['rating_count', 'average_rating'])
    
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------ 