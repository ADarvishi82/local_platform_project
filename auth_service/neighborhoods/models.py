# neighborhoods/models.py
from django.db import models

class Neighborhood(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="نام محله")
    city = models.CharField(max_length=100, verbose_name="شهر", default="پیش فرض", help_text="نام شهری که این محله در آن قرار دارد.")
    center_latitude = models.FloatField(verbose_name="عرض جغرافیایی مرکز محله")
    center_longitude = models.FloatField(verbose_name="طول جغرافیایی مرکز محله")
    radius_km = models.FloatField(default=1.0, verbose_name="شعاع تقریبی محله (کیلومتر)")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.city})"

    class Meta:
        verbose_name = "محله"
        verbose_name_plural = "محله‌ها"
        ordering = ['city', 'name']
        unique_together = ('name', 'city') # نام محله در هر شهر باید یکتا باشد