# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# ویو گوگل را اینجا نگه می‌داریم تا api_urls.py شلوغ نشود
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.openid_connect.views import OpenIDConnectOAuth2Adapter
from allauth.socialaccount.providers.google.provider import GoogleProvider

class GoogleOpenIDConnectAdapter(OpenIDConnectOAuth2Adapter):
    provider_id = GoogleProvider.id

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOpenIDConnectAdapter

# یک لیست برای تمام URL های api
api_urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('auth/google/', GoogleLogin.as_view(), name='google_login'),
    
    # include کردن URL های هر اپلیکیشن
    path('', include('users.urls')),
    path('', include('neighborhoods.urls')),
    path('', include('posts.urls')),
    path('', include('recommender.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    # فقط یک include برای تمام API ها
    path('api/', include(api_urlpatterns)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)