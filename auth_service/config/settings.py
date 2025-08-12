from datetime import timedelta
from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.

BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-4_zd2pw$cm#xo+zpjsxo7jhqt#dy@4zv2d-s$(*l4i_@vx&jo^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'django_filters',
    'rest_framework',
    'rest_framework.authtoken', # <<<< اضافه کنید
    'rest_framework_simplejwt',
    'dj_rest_auth',
    'django.contrib.sites', # مورد نیاز dj_rest_auth و allauth
    'allauth',              # مورد نیاز dj_rest_auth
    'allauth.account',      # مورد نیاز dj_rest_auth
    'allauth.socialaccount',# اختیاری، برای ورود با شبکه‌های اجتماعی
    'dj_rest_auth.registration', # برای استفاده از endpoint ثبت نام داخلی dj_rest_auth
    'users.apps.UsersConfig', # یا فقط 'users'
    'neighborhoods.apps.NeighborhoodsConfig',
    "posts.apps.PostsConfig",
    'taggit',

]
SITE_ID = 1
INSTALLED_APPS += [
    'allauth.socialaccount.providers.google', # اضافه کردن Google provider
]
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': '279929399898-ir6jp70mc46v6pjojnrdl2veg3ta44h2.apps.googleusercontent.com',
            'secret': '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',
            'key': ''
        },
        'SCOPE': [
            'profile',
            'email',
            'openid',
        ],
    }
}
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = 'none' # اگر قبلاً دارید
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_REQUIRED = True
SOCIALACCOUNT_AUTO_SIGNUP = True # ایجاد خودکار حساب کاربری برای کاربران جدید
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none' # عدم نیاز به تایید ایمیل برای ورود با گوگل


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware', # <--- قبل از این
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware', # <--- یا قبل از این
    'allauth.account.middleware.AccountMiddleware', # <<<<< این خط را اضافه کنید
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'




DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'auth_service_db',      
        'USER': 'root',                 
        'PASSWORD': 'Aa@123456', 
        'HOST': 'localhost',           
        'PORT': '3306',                 
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'", 
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us' # یا 'fa-ir'
TIME_ZONE = 'Asia/Tehran' # یا منطقه زمانی خودتان
USE_I18N = True
USE_L10N = True # در نسخه‌های جدید جنگو این به USE_TZ تغییر یافته
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': ( # یک پیش‌فرض خوب برای شروع
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}

ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_LOGIN_METHODS = {'username', 'email'} 
ACCOUNT_SIGNUP_FIELDS = ['username', 'email', 'password']


REST_AUTH = {
    'USE_JWT': True,  
    'TOKEN_MODEL': None, 
    'JWT_AUTH_HTTPONLY' :False, 
    'USER_DETAILS_SERIALIZER': 'users.serializers.UserDisplaySerializer',

}

# settings.py



SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5), # << عمر کوتاه برای توکن دسترسی
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),    # << عمر طولانی‌تر برای توکن رفرش
    'ROTATE_REFRESH_TOKENS': False, # اگر True باشد، با هر بار رفرش، یک رفرش توکن جدید هم داده می‌شود. False ساده‌تر است.
    'BLACKLIST_AFTER_ROTATION': False, # مرتبط با گزینه بالا
    'UPDATE_LAST_LOGIN': False, # برای آپدیت last_login کاربر هنگام رفرش توکن

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY, # از SECRET_KEY خود جنگو استفاده می‌کند
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',), # نوع هدر احراز هویت
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id', # یا 'pk' اگر مدل User شما از pk استفاده می‌کند
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5), # برای توکن‌های اسلایدینگ
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1), # برای توکن‌های اسلایدینگ
}


CORS_ALLOWED_ORIGINS = [
    "http://localhost:9000",
    "http://127.0.0.1:9000",
]

CORS_ALLOW_ALL_ORIGINS = True  # در محیط توسعه مجاز است، اما برای محیط تولید باید محدود شود
CORS_ALLOW_CREDENTIALS = True


ACCOUNT_AUTHENTICATION_METHOD = 'username_email' 

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend', # بک‌اند پیش‌فرض جنگو
    'allauth.account.auth_backends.AuthenticationBackend', # بک‌اند allauth
]