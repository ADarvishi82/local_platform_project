# posts/models.py
from django.db import models
from django.contrib.auth.models import User # یا مدل User سفارشی شما اگر دارید
from taggit.managers import TaggableManager
from neighborhoods.models import Neighborhood # <<<< مدل محله را import کنید
from django.utils import timezone # برای مقایسه با زمان حال
from users.models import BusinessProfile # <<<< BusinessProfile را import کنید

class Post(models.Model):
    class VisibilityChoices(models.TextChoices):
        PUBLIC = 'PUBLIC', 'عمومی (برای همه)'
        NEIGHBORHOOD = 'NEIGHBORHOOD', 'فقط هم‌محله‌ای‌ها'
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts', verbose_name="نویسنده")
    content = models.TextField(verbose_name="محتوا")
    tags = TaggableManager(verbose_name="هشتگ‌ها", help_text="یک لیست از هشتگ‌ها که با کاما از هم جدا شده‌اند.", blank=True)
    likes_count = models.PositiveIntegerField(default=0, verbose_name="تعداد لایک‌ها")
    comments_count = models.PositiveIntegerField(default=0, verbose_name="تعداد کامنت‌ها")
    visibility = models.CharField(
        max_length=20,
        choices=VisibilityChoices.choices,
        default=VisibilityChoices.PUBLIC, # <<<< مقدار پیش‌فرض را عمومی در نظر می‌گیریم
        verbose_name="قابلیت مشاهده"
    )
    neighborhood = models.ForeignKey(
        Neighborhood,
        on_delete=models.SET_NULL, # اگر محله حذف شد، پست حذف نشود
        null=True,
        blank=True,
        verbose_name="محله مربوطه"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="زمان ایجاد")
    updated_at = models.DateTimeField(auto_now=True) # برای ویرایش پست در آینده
    related_business = models.ForeignKey(
        BusinessProfile,
        on_delete=models.SET_NULL, # اگر پروفایل کسب‌وکار حذف شد، پست باقی بماند
        null=True,
        blank=True,
        related_name='posts', # برای دسترسی از business_profile.posts.all()
        verbose_name="کسب‌وکار مرتبط"
    )
    

    def __str__(self):
        # از کد قبلی شما استفاده می‌کنیم و فقط visibility را به آن اضافه می‌کنیم
        return f"پست توسط {self.author.username} ({self.get_visibility_display()}) در {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        verbose_name = "پست"
        verbose_name_plural = "پست‌ها"
        ordering = ['-created_at'] # جدیدترین‌ها اول نمایش داده شوند
     
    class PostTypeChoices(models.TextChoices):
        POST = 'POST', 'پست عادی'
        NEWS = 'NEWS', 'خبر'
        EVENT = 'EVENT', 'رویداد' # برای آینده

    # ... (فیلدهای قبلی: author, content, visibility, neighborhood, ...)
    
    post_type = models.CharField(
        max_length=20,
        choices=PostTypeChoices.choices,
        default=PostTypeChoices.POST,
        verbose_name="نوع پست"
    )
    
    is_pinned = models.BooleanField(default=False, verbose_name="سنجاق شده (مهم)")
    
   
        
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



class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="نویسنده کامنت"
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments', # برای دسترسی به کامنت‌ها از post.comments.all()
        verbose_name="پست مربوطه"
    )
    content = models.TextField(verbose_name="محتوای کامنت")
    
    # برای کامنت‌های تو در تو (پاسخ به کامنت) - در فاز بعدی می‌توانیم استفاده کنیم
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies',
        verbose_name="پاسخ به"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="زمان ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="زمان بروزرسانی")

    def __str__(self):
        return f"کامنت توسط {self.author.username} برای پست شماره {self.post.id}"

    class Meta:
        verbose_name = "کامنت"
        verbose_name_plural = "کامنت‌ها"
        ordering = ['created_at']
        

# ***** مدل جدید برای رویدادها *****
class Event(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان رویداد")
    description = models.TextField(verbose_name="توضیحات")
    
    # رویداد به کدام محله تعلق دارد
    neighborhood = models.ForeignKey(
        'neighborhoods.Neighborhood',
        on_delete=models.CASCADE,
        related_name='events',
        verbose_name="محله"
    )

    # چه کسی این رویداد را ایجاد کرده (می‌تواند ادمین، کسب‌وکار یا کاربر عادی باشد)
    creator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL, # اگر کاربر حذف شد، رویداد باقی بماند
        null=True,
        related_name='created_events',
        verbose_name="ایجاد کننده"
    )
    
    start_time = models.DateTimeField(verbose_name="زمان شروع")
    end_time = models.DateTimeField(verbose_name="زمان پایان", null=True, blank=True)
    
    location_name = models.CharField(max_length=255, verbose_name="نام مکان", help_text="مثال: پارک لاله، کافه روبرو", blank=True)
    is_approved = models.BooleanField(default=False, verbose_name="تایید شده") # برای تایید توسط ادمین

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "رویداد"
        verbose_name_plural = "رویدادها"
        ordering = ['start_time'] # رویدادهای نزدیک‌تر اول نمایش داده شوند
        
        
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='business_ratings')
    business_profile = models.ForeignKey(
        BusinessProfile, 
        on_delete=models.CASCADE, 
        related_name='ratings' # برای دسترسی به امتیازها از business_profile.ratings.all()
    )
    score = models.PositiveSmallIntegerField(
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')],
        verbose_name="امتیاز"
    )
    # می‌توانید یک فیلد نظر هم به امتیاز اضافه کنید
    # comment = models.TextField(blank=True, null=True, verbose_name="نظر")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "امتیاز کسب‌وکار"
        verbose_name_plural = "امتیازهای کسب‌وکارها"
        # هر کاربر فقط یک بار می‌تواند به یک کسب‌وکار امتیاز دهد
        unique_together = ('user', 'business_profile')