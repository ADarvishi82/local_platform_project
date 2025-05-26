from django.contrib import admin
from .models import UserProfile, BusinessProfile, Category, Tag # Category و Tag را import کنید
from django.utils.text import slugify # برای prepopulated_fields

# users/admin.py
from django.utils.html import format_html # برای نمایش عکس در ادمین

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_profile_picture', 'address_string', 'created_at', 'updated_at')
    search_fields = ('user__username', 'address_string')
    readonly_fields = ('created_at', 'updated_at', 'image_preview') # image_preview را هم readonly می‌کنیم
    fields = ('user', 'address_string', 'latitude', 'longitude', 'profile_picture', 'image_preview', 'created_at', 'updated_at') # ترتیب نمایش در فرم

    def display_profile_picture(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" width="50" height="50" style="border-radius:50%;" />', obj.profile_picture.url)
        return "بدون عکس"
    display_profile_picture.short_description = "عکس پروفایل"

    def image_preview(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" width="150" />', obj.profile_picture.url)
        return "عکسی برای نمایش وجود ندارد."
    image_preview.short_description = 'پیش‌نمایش عکس'

# ... سایر کلاس‌های ادمین شما ...

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug') # 'parent' را هم اضافه کنید اگر دارید
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)} # به طور خودکار اسلاگ را از نام می‌سازد

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(BusinessProfile)
class BusinessProfileAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'user', 'account_type', 'category', 'is_verified', 'created_at')
    list_filter = ('is_verified', 'account_type', 'category') # فیلتر بر اساس category هم اضافه شد
    search_fields = ('business_name', 'user__username', 'category__name') # جستجو بر اساس نام category
    # برای نمایش ManyToManyField (مانند tags) در فرم ادمین، می‌توانید از filter_horizontal یا filter_vertical استفاده کنید:
    filter_horizontal = ('tags',) # یا filter_vertical = ('tags',)
    readonly_fields = ('created_at', 'updated_at')
    actions = ['verify_entities', 'unverify_entities'] # نام اکشن را عمومی‌تر کردم

    def verify_entities(self, request, queryset):
        queryset.update(is_verified=True)
    verify_entities.short_description = "تأیید موارد انتخاب شده (تیک آبی)"

    def unverify_entities(self, request, queryset):
        queryset.update(is_verified=False)
    unverify_entities.short_description = "لغو تأیید موارد انتخاب شده (حذف تیک آبی)"