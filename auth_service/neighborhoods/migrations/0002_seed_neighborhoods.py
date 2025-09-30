from django.db import migrations

def create_neighborhoods(apps, schema_editor):
    """
    داده‌های اولیه برای مدل Neighborhood را ایجاد می‌کند.
    فقط شامل ۲۰ محله از شهر تبریز.
    """
    Neighborhood = apps.get_model('neighborhoods', 'Neighborhood')
    
    neighborhoods_data = [
        {'name': 'ولیعصر', 'city': 'تبریز', 'center_latitude': 38.06, 'center_longitude': 46.35},
        {'name': 'آبرسان', 'city': 'تبریز', 'center_latitude': 38.07, 'center_longitude': 46.32},
        {'name': 'شهرک باغمیشه', 'city': 'تبریز', 'center_latitude': 38.10, 'center_longitude': 46.33},
        {'name': 'شهرک پرواز', 'city': 'تبریز', 'center_latitude': 38.08, 'center_longitude': 46.34},
        {'name': 'راسته کوچه', 'city': 'تبریز', 'center_latitude': 38.07, 'center_longitude': 46.29},
        {'name': 'شهرک اندیشه', 'city': 'تبریز', 'center_latitude': 38.09, 'center_longitude': 46.36},
        {'name': 'شهرک امامیه', 'city': 'تبریز', 'center_latitude': 38.05, 'center_longitude': 46.31},
        {'name': 'شهرک خاوران', 'city': 'تبریز', 'center_latitude': 38.11, 'center_longitude': 46.38},
        {'name': 'شهرک مرزداران', 'city': 'تبریز', 'center_latitude': 38.06, 'center_longitude': 46.37},
        {'name': 'شهرک یاغچیان', 'city': 'تبریز', 'center_latitude': 38.04, 'center_longitude': 46.30},
        {'name': 'شهرک گلکار', 'city': 'تبریز', 'center_latitude': 38.03, 'center_longitude': 46.32},
        {'name': 'شهرک منظریه', 'city': 'تبریز', 'center_latitude': 38.02, 'center_longitude': 46.33},
        {'name': 'شهرک فرهنگیان', 'city': 'تبریز', 'center_latitude': 38.01, 'center_longitude': 46.34},
        {'name': 'شهرک طالقانی', 'city': 'تبریز', 'center_latitude': 38.00, 'center_longitude': 46.35},
        {'name': 'شهرک مهرانه', 'city': 'تبریز', 'center_latitude': 38.09, 'center_longitude': 46.31},
        {'name': 'شهرک زعفرانیه', 'city': 'تبریز', 'center_latitude': 38.08, 'center_longitude': 46.30},
        {'name': 'شهرک شهید رجایی', 'city': 'تبریز', 'center_latitude': 38.07, 'center_longitude': 46.28},
        {'name': 'شهرک شهید بهشتی', 'city': 'تبریز', 'center_latitude': 38.06, 'center_longitude': 46.27},
        {'name': 'شهرک شهید باکری', 'city': 'تبریز', 'center_latitude': 38.05, 'center_longitude': 46.26},
        {'name': 'شهرک شهید مدنی', 'city': 'تبریز', 'center_latitude': 38.04, 'center_longitude': 46.25},
    ]

    neighborhood_objects = []
    for data in neighborhoods_data:
        if not Neighborhood.objects.filter(name=data['name'], city=data['city']).exists():
            neighborhood_objects.append(Neighborhood(**data))
    
    if neighborhood_objects:
        Neighborhood.objects.bulk_create(neighborhood_objects)
        print(f"\n{len(neighborhood_objects)} محله جدید در تبریز ایجاد شد.")

def remove_neighborhoods(apps, schema_editor):
    """
    داده‌های ایجاد شده را حذف می‌کند (برای rollback کردن migration).
    """
    Neighborhood = apps.get_model('neighborhoods', 'Neighborhood')
    neighborhood_names = [
        'ولیعصر', 'آبرسان', 'شهرک باغمیشه', 'شهرک پرواز', 'راسته کوچه',
        'شهرک اندیشه', 'شهرک امامیه', 'شهرک خاوران', 'شهرک مرزداران', 'شهرک یاغچیان',
        'شهرک گلکار', 'شهرک منظریه', 'شهرک فرهنگیان', 'شهرک طالقانی', 'شهرک مهرانه',
        'شهرک زعفرانیه', 'شهرک شهید رجایی', 'شهرک شهید بهشتی', 'شهرک شهید باکری', 'شهرک شهید مدنی',
    ]
    Neighborhood.objects.filter(name__in=neighborhood_names, city='تبریز').delete()
    print("\nمحله‌های تبریز حذف شدند.")

class Migration(migrations.Migration):

    dependencies = [
        ('neighborhoods', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_neighborhoods, remove_neighborhoods),
    ]
