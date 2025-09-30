# users/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import UserProfile, BusinessProfile # مدل‌های UserProfile و BusinessProfile
# از neighborhoods.models هم import می‌کنیم اگر بخواهیم به طور خاص به آن دسترسی داشته باشیم
# اما برای list_filter و list_display نیازی نیست اگر فقط نام فیلد را می‌نویسیم.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_profile_picture', 'address_string', 'neighborhood', 'created_at', 'updated_at')
    search_fields = ('user__username', 'address_string', 'neighborhood__name', 'neighborhood__city') # جستجو بر اساس نام و شهر محله
    list_filter = ('neighborhood__city', 'neighborhood') # فیلتر بر اساس شهر محله و خود محله
    readonly_fields = ('created_at', 'updated_at', 'image_preview')
    # ترتیب فیلدها در فرم ویرایش، neighborhood را هم اضافه می‌کنیم
    fields = ('user', 'address_string', 'latitude', 'longitude', 'neighborhood', 'profile_picture', 'image_preview', 'created_at', 'updated_at')
    raw_id_fields = ('user', 'neighborhood',) # برای انتخاب راحت‌تر کاربر و محله با جستجو

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


@admin.register(BusinessProfile)
class BusinessProfileAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'user', 'account_type', 'category', 'neighborhood', 'is_verified', 'created_at')
    list_filter = ('is_verified', 'account_type', 'category', 'neighborhood__city', 'neighborhood')
    search_fields = ('business_name', 'user__username', 'category__name', 'neighborhood__name', 'neighborhood__city')
    filter_horizontal = ('tags',)
    readonly_fields = ('created_at', 'updated_at')
    actions = ['verify_entities', 'unverify_entities']
    raw_id_fields = ('user', 'category', 'neighborhood',) # tags چون ManyToMany است، با filter_horizontal بهتر است

    def verify_entities(self, request, queryset):
        queryset.update(is_verified=True)
    verify_entities.short_description = "تأیید موارد انتخاب شده (تیک آبی)"

    def unverify_entities(self, request, queryset):
        queryset.update(is_verified=False)
    unverify_entities.short_description = "لغو تأیید موارد انتخاب شده (حذف تیک آبی)"

# CategoryAdmin و TagAdmin بدون تغییر باقی می‌مانند (اگر در همین فایل بودند)
# from .models import Category, Tag (اگر Category و Tag در اپلیکیشن users بودند)
# از آنجایی که Category و Tag حالا باید در اپلیکیشن neighborhoods یا یک اپلیکیشن مشترک دیگر باشند،
# admin آنها هم باید در همان اپلیکیشن تعریف شود.
# اگر Category و Tag را در users/models.py نگه داشته‌اید، کد admin آنها اینجا باقی می‌ماند.
# اگر به neighborhoods/models.py منتقل کرده‌اید، admin آنها هم باید به neighborhoods/admin.py برود.
# فرض می‌کنیم Category و Tag هنوز در users.models هستند برای این مثال:

from .models import Category, Tag # اگر این مدل‌ها در users.models هستند
from django.utils.text import slugify

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}