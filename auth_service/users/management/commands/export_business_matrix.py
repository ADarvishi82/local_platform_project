# your_app/management/commands/export_business_matrix.py

import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from users.models import BusinessProfile, Category
from neighborhoods.models import Neighborhood

class Command(BaseCommand):
    help = 'Exports the Neighborhood x Business Category matrix to a CSV file.'

    def add_arguments(self, parser):
        # یک آرگومان برای مشخص کردن مسیر فایل خروجی اضافه می‌کنیم
        parser.add_argument(
            'output_file', 
            type=str, 
            help='The path to the output CSV file (e.g., data/business_matrix.csv)'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting data export process...'))

        # ۱. واکشی تمام محله‌ها و دسته‌بندی‌های فعال
        all_neighborhoods = Neighborhood.objects.all()
        all_categories = Category.objects.filter(businesses__is_verified=True).distinct() # فقط دسته‌بندی‌هایی که کسب‌وکار تایید شده دارند

        if not all_neighborhoods.exists() or not all_categories.exists():
            raise CommandError('No neighborhoods or categories found. Please add some data first.')

        self.stdout.write(f'Found {all_neighborhoods.count()} neighborhoods and {all_categories.count()} business categories.')

        # ۲. آماده‌سازی ساختار داده برای ماتریس
        # از یک دیکشنری برای نگه داشتن داده‌ها قبل از تبدیل به DataFrame استفاده می‌کنیم
        matrix_data = {}
        
        # نام ستون‌ها (دسته‌بندی‌ها)
        category_names = [cat.name for cat in all_categories]

        # ۳. پر کردن ماتریس
        for neighborhood in all_neighborhoods:
            # یک ردیف جدید برای این محله ایجاد کن (مقدار اولیه همه ۰ است)
            row = [0] * len(all_categories)
            
            # کسب‌وکارهای تایید شده در این محله را پیدا کن
            businesses_in_hood = BusinessProfile.objects.filter(
                neighborhood=neighborhood,
                is_verified=True,
                category__isnull=False # کسب‌وکارهایی که دسته‌بندی دارند
            )
            
            # برای هر کسب‌وکار در محله، ستون دسته‌بندی مربوطه را ۱ کن
            for business in businesses_in_hood:
                try:
                    # پیدا کردن ایندکس ستون مربوط به دسته‌بندی این کسب‌وکار
                    category_index = category_names.index(business.category.name)
                    row[category_index] = 1
                except ValueError:
                    # این اتفاق نباید بیفتد اگر all_categories را درست ساخته باشیم
                    pass
            
            # اضافه کردن ردیف به دیکشنری داده‌ها
            matrix_data[neighborhood.name] = row

        # ۴. تبدیل دیکشنری به DataFrame در Pandas
        df = pd.DataFrame.from_dict(matrix_data, orient='index', columns=category_names)
        df.index.name = 'Neighborhood' # نام‌گذاری ستون ایندکس

        # ۵. ذخیره DataFrame به صورت فایل CSV
        output_file_path = options['output_file']
        try:
            df.to_csv(output_file_path)
            self.stdout.write(self.style.SUCCESS(f'Successfully exported matrix to {output_file_path}'))
        except IOError as e:
            raise CommandError(f'Error writing to file: {e}')