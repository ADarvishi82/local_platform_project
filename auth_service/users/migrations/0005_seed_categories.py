# users/migrations/0005_seed_categories.py

from django.db import migrations
from django.utils.text import slugify

def create_categories(apps, schema_editor):
    """
    داده‌های اولیه برای مدل Category را ایجاد می‌کند.
    """
    Category = apps.get_model('users', 'Category')

    categories_data = [
        'رستوران', 'کافه', 'سوپرمارکت', 'نانوایی', 'میوه فروشی',
        'تعمیرات لوازم خانگی', 'خدمات نظافتی', 'خشکشویی',
        'آرایشگاه مردانه', 'آرایشگاه زنانه', 'باشگاه ورزشی',
        'پزشکی و سلامت', 'داروخانه', 'آموزشی', 'کتاب‌فروشی',
        'گل‌فروشی', 'خدمات کامپیوتری', 'تاکسی سرویس', 'دفتر پیشخوان', 'مشاور املاک'
    ]

    for name in categories_data:
        slug = slugify(name, allow_unicode=True)
        if not Category.objects.filter(slug=slug).exists():
            Category.objects.create(name=name, slug=slug)
    print(f"\n{len(categories_data)} categories checked/created.")

def remove_categories(apps, schema_editor):
    Category = apps.get_model('users', 'Category')
    category_names = [
        'رستوران', 'کافه', 'سوپرمارکت', 'نانوایی', 'میوه فروشی',
        'تعمیرات لوازم خانگی', 'خدمات نظافتی', 'خشکشویی',
        'آرایشگاه مردانه', 'آرایشگاه زنانه', 'باشگاه ورزشی',
        'پزشکی و سلامت', 'داروخانه', 'آموزشی', 'کتاب‌فروشی',
        'گل‌فروشی', 'خدمات کامپیوتری', 'تاکسی سرویس', 'دفتر پیشخوان', 'مشاور املاک'
    ]
    Category.objects.filter(name__in=category_names).delete()
    print("\nSeeded categories have been removed.")

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_categories, remove_categories),
    ]
