# users/migrations/0008_seed_business_profiles.py

from django.db import migrations
import random
from faker import Faker
# ***** این import جدید لازم است *****
from django.contrib.auth.hashers import make_password

def create_business_profiles(apps, schema_editor):
    """
    داده‌های اولیه برای مدل BusinessProfile و کاربران مربوط به آنها را ایجاد می‌کند.
    """
    User = apps.get_model('auth', 'User')
    BusinessProfile = apps.get_model('users', 'BusinessProfile')
    Category = apps.get_model('users', 'Category')
    Neighborhood = apps.get_model('neighborhoods', 'Neighborhood')

    if not Category.objects.exists() or not Neighborhood.objects.exists():
        print("\nSkipping business profile seeding: No categories or neighborhoods found.")
        return

    fake = Faker('fa_IR')
    all_categories = list(Category.objects.all())
    all_neighborhoods = list(Neighborhood.objects.all())
    NUM_PROFILES_TO_CREATE = 100 
    print(f"\nCreating {NUM_PROFILES_TO_CREATE} new business profiles...")

    users_to_create = []
    business_profiles_data = []

    for i in range(NUM_PROFILES_TO_CREATE):
        first_name = fake.first_name()
        last_name = fake.last_name()
        username = f"{first_name.lower()}{last_name.lower()}{random.randint(10, 99)}"
        email = f"{username}@example.com"

        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            continue

        # به جای create_user، از create استفاده می‌کنیم و پسورد غیرقابل استفاده را دستی می‌سازیم
        # UNUSABLE_PASSWORD_PREFIX یک رشته خاص است که جنگو برای این کار استفاده می‌کند
        # make_password(None) هم همین کار را می‌کند.
        unusable_password = make_password(None)

        # آبجکت User را برای bulk_create آماده می‌کنیم
        users_to_create.append(
            User(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=unusable_password,
                is_active=True # فعال بودن کاربر
            )
        )
        
        # داده‌های مربوط به BusinessProfile را هم برای بعد نگه می‌داریم
        random_category = random.choice(all_categories)
        random_neighborhood = random.choice(all_neighborhoods)
        business_name = f"{random_category.name} {fake.company_suffix()} {random_neighborhood.name}"
        base_price = random.randint(50, 500) * 1000
        
        business_profiles_data.append({
            'username': username, # از username برای پیدا کردن User بعد از bulk_create استفاده می‌کنیم
            'data': {
                'account_type': 'BUSINESS',
                'business_name': business_name,
                'category': random_category,
                'neighborhood': random_neighborhood,
                'description': fake.paragraph(nb_sentences=4),
                'address_string': f"{random_neighborhood.city}، {random_neighborhood.name}، {fake.street_address()}",
                'latitude': random_neighborhood.center_latitude + random.uniform(-0.01, 0.01),
                'longitude': random_neighborhood.center_longitude + random.uniform(-0.01, 0.01),
                'phone_number': fake.phone_number(),
                'website': f"https://{username}.ir",
                'base_price': base_price,
                'price_string': f"شروع از {base_price:,} تومان",
                'is_verified': True
            }
        })

    # ۱. تمام کاربران را به صورت یکجا ایجاد کن
    if users_to_create:
        User.objects.bulk_create(users_to_create)
        print(f"Created {len(users_to_create)} new users.")
    
    # ۲. تمام BusinessProfile ها را به صورت یکجا ایجاد کن
    business_profiles_to_create = []
    # کاربران ایجاد شده را با دیکشنری‌ای که username را به آبجکت user مپ می‌کند، پیدا کن
    created_users = {user.username: user for user in User.objects.filter(username__in=[d['username'] for d in business_profiles_data])}

    for data in business_profiles_data:
        user_obj = created_users.get(data['username'])
        if user_obj:
            business_profiles_to_create.append(
                BusinessProfile(user=user_obj, **data['data'])
            )

    if business_profiles_to_create:
        BusinessProfile.objects.bulk_create(business_profiles_to_create)
        print(f"Created {len(business_profiles_to_create)} new business profiles.")


def remove_business_profiles(apps, schema_editor):
    """
    تمام کاربرانی را که پروفایل کسب‌وکار دارند، حذف می‌کند.
    """
    User = apps.get_model('auth', 'User')
    # کاربرانی را پیدا کن که business_profile آنها null نیست
    users_with_business_profile = User.objects.filter(business_profile__isnull=False)
    
    # فقط کاربرانی را حذف کن که توسط این اسکریپت ایجاد شده‌اند (با ایمیل example.com)
    # این کار از حذف کاربران واقعی شما جلوگیری می‌کند
    script_generated_users = users_with_business_profile.filter(email__endswith='@example.com')
    
    count = script_generated_users.count()
    if count > 0:
        script_generated_users.delete()
        print(f"\nRemoved {count} script-generated business users and their profiles.")

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'), # <<<< نام آخرین migration اپ users (همان migration دسته‌بندی)
        ('neighborhoods', '0001_initial'), # <<<< نام migration محله‌ها
    ]

    operations = [
        migrations.RunPython(create_business_profiles, remove_business_profiles),
    ]