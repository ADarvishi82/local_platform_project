from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify # برای ساختن اسلاگ از نام

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    address_string = models.CharField(max_length=255, blank=True, null=True, verbose_name="آدرس متنی")
    latitude = models.FloatField(blank=True, null=True, verbose_name="عرض جغرافیایی")
    longitude = models.FloatField(blank=True, null=True, verbose_name="طول جغرافیایی")
    
    # اضافه کردن فیلد عکس پروفایل
    profile_picture = models.ImageField(
        upload_to='profile_pics/',  # عکس‌ها در پوشه MEDIA_ROOT/profile_pics/ ذخیره می‌شوند
        blank=True,                 # می‌تواند خالی باشد
        null=True,                  # در دیتابیس می‌تواند null باشد
        verbose_name="عکس پروفایل"
    )
    # phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="شماره تلفن")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="زمان ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="زمان بروزرسانی")

    def __str__(self):
        return f"پروفایل کاربری {self.user.username}"

    class Meta:
        verbose_name = "پروفایل کاربر"
        verbose_name_plural = "پروفایل‌های کاربران"

# ... سایر مدل‌های شما (Category, Tag, BusinessProfile) بدون تغییر باقی می‌مانند ...

# مدل Category
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="نام دسته‌بندی")
    slug = models.SlugField(max_length=100, unique=True, blank=True, verbose_name="اسلاگ")
    # parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE, verbose_name="دسته‌بندی مادر") # برای دسته‌بندی‌های تو در تو (اختیاری)
    # icon = models.CharField(max_length=50, blank=True, null=True, verbose_name="آیکون") # نام آیکون از یک مجموعه آیکون

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"
        ordering = ['name'] # مرتب‌سازی بر اساس نام

# مدل Tag
class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="نام تگ")
    slug = models.SlugField(max_length=100, unique=True, blank=True, verbose_name="اسلاگ")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "تگ"
        verbose_name_plural = "تگ‌ها"
        ordering = ['name']

# مدل BusinessProfile (به‌روز شده با Category و Tag و نوع سازمان)
class BusinessProfile(models.Model):
    ACCOUNT_TYPE_CHOICES = [
        ('BUSINESS', 'کسب‌وکار عادی'),
        ('ORGANIZATION', 'سازمان/اداره'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='business_profile')
    account_type = models.CharField(
        max_length=20,
        choices=ACCOUNT_TYPE_CHOICES,
        default='BUSINESS',
        verbose_name="نوع حساب"
    )
    business_name = models.CharField(max_length=200, verbose_name="نام کسب‌وکار/سازمان")
    
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL, # اگر دسته‌بندی حذف شد، این فیلد null شود
        null=True,
        blank=True, # می‌تواند خالی باشد
        related_name='businesses', # از یک Category به تمام BusinessProfile های آن دسترسی داریم
        verbose_name="دسته‌بندی"
    )
    
    tags = models.ManyToManyField(
        Tag,
        blank=True, # می‌تواند هیچ تگی نداشته باشد
        related_name='businesses', # از یک Tag به تمام BusinessProfile های آن دسترسی داریم
        verbose_name="تگ‌ها"
    )
    
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")
    address_string = models.CharField(max_length=255, blank=True, null=True, verbose_name="آدرس متنی")
    latitude = models.FloatField(blank=True, null=True, verbose_name="عرض جغرافیایی")
    longitude = models.FloatField(blank=True, null=True, verbose_name="طول جغرافیایی")
    
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="شماره تلفن")
    website = models.URLField(blank=True, null=True, verbose_name="وب‌سایت")
    logo = models.ImageField(upload_to='business_logos/', blank=True, null=True, verbose_name="لوگو") # نیاز به تنظیم MEDIA_ROOT و MEDIA_URL

    is_verified = models.BooleanField(default=False, verbose_name="تأیید شده (تیک آبی)") # برای تأیید کسب‌وکار/سازمان توسط ادمین

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="زمان ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="زمان بروزرسانی")

    def __str__(self):
        return f"{self.get_account_type_display()}: {self.business_name} (مدیر: {self.user.username})"

    class Meta:
        verbose_name = "پروفایل کسب‌وکار/سازمان"
        verbose_name_plural = "پروفایل‌های کسب‌وکارها/سازمان‌ها"
        ordering = ['business_name']