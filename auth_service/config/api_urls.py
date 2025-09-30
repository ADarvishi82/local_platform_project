# config/api_urls.py
from django.urls import path, include

urlpatterns = [
    # تمام URL هایی که قبلاً /api/ داشتند را به اینجا منتقل می‌کنیم
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    
    # URL های ویو سفارشی گوگل
    # (این بخش را باید از config/urls.py اصلی به اینجا منتقل کنید)
    # from .urls import GoogleLogin 
    # path('auth/google/', GoogleLogin.as_view(), name='google_login'),

    # URL های اپلیکیشن‌های شما
    path('', include('users.urls')),
    path('', include('neighborhoods.urls')),
    path('', include('posts.urls')),
    path('', include('recommender.urls')),
]