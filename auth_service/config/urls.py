# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    
    path('api/', include('users.urls')), # <<<< این خط را اضافه کنید (مثلاً تحت پیشوند /api/)
                                        # یا هر پیشوند دیگری که دوست دارید، مثلاً /api/v1/
                                        
    path('api/' , include('neighborhoods.urls')),   
    path("api/" , include('posts.urls')),                          
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # اگر STATIC_ROOT هم دارید