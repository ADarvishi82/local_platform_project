# posts/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Like

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