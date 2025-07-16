# posts/models.py
from django.db import models
from django.contrib.auth.models import User # یا مدل User سفارشی شما اگر دارید
from taggit.managers import TaggableManager

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts', verbose_name="نویسنده")
    content = models.TextField(verbose_name="محتوا")
    tags = TaggableManager(verbose_name="هشتگ‌ها", help_text="یک لیست از هشتگ‌ها که با کاما از هم جدا شده‌اند.", blank=True)
    likes_count = models.PositiveIntegerField(default=0, verbose_name="تعداد لایک‌ها")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="زمان ایجاد")
    updated_at = models.DateTimeField(auto_now=True) # برای ویرایش پست در آینده

    def __str__(self):
        return f"پست توسط {self.author.username} در {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        verbose_name = "پست"
        verbose_name_plural = "پست‌ها"
        ordering = ['-created_at'] # جدیدترین‌ها اول نمایش داده شوند
        
        
class PostImage(models.Model):
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name='images',    
        verbose_name="پست مربوطه"
    )
    image = models.ImageField(
        upload_to='post_images/', # عکس‌ها همچنان در این پوشه ذخیره می‌شوند
        verbose_name="عکس"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="زمان آپلود")

    def __str__(self):
        return f"عکس برای پست شماره {self.post.id}"
    
    class Meta:
        verbose_name = "عکس پست"
        verbose_name_plural = "عکس‌های پست‌ها"
        ordering = ['uploaded_at']
        
        
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes', verbose_name="کاربر لایک‌کننده")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes', verbose_name="پست لایک‌شده")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="زمان لایک")

    def __str__(self):
        return f"{self.user.username} پستِ {self.post.id} را لایک کرده"
    
    class Meta:
        verbose_name = "لایک"
        verbose_name_plural = "لایک‌ها"
        # یک کاربر فقط می‌تواند یک بار یک پست را لایک کند
        unique_together = ('user', 'post')
        ordering = ['-created_at']