"""
Django settings for linenow project.

Generated by 'django-admin startproject' using Django 5.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
import environ

from pathlib import Path

from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


env = environ.Env(DEBUG=(bool, True))

environ.Env.read_env(
    env_file=os.path.join(BASE_DIR, '.env')
)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = ['https://linenow.xyz', "https://211.188.52.202"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    
    'dj_rest_auth',
    'dj_rest_auth.registration',
    
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.kakao',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    
    'celery',
    
    'accounts',
    'booth',
    'waiting',
    'manager',
    'sms',
]

SITE_ID = 1

ACCOUNT_USER_MODEL_USERNAME_FIELD = "name"
ACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "username"

ACCOUNT_EMAIL_VERIFICATION = "none"

AUTH_USER_MODEL = 'accounts.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # "utils.CustomCookieAuthentication.CustomCookieAuthentication",
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        #"rest_framework.authentication.TokenAuthentication",
        #"rest_framework.authentication.SessionAuthentication",
        #"dj_rest_auth.jwt_auth.JWTCookieAuthentication",
    ),
    'EXCEPTION_HANDLER': 'utils.exceptions.custom_exception_handler',
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}

REST_AUTH = {
    'USE_JWT' : True,
    'JWT_AUTH_COOKIE' : None, 
    'JWT_AUTH_REFRESH_COOKIE' : None,
    'JWT_AUTH_HTTPONLY': False,
    'SESSION_LOGIN' : False

}

REST_USE_JWT = True

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=14),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'TOKEN_USER_CLASS': "accounts.models.User",
}

ACCOUNT_ADAPTER = 'accounts.adapters.CustomUserAccountAdapter'

MIDDLEWARE = [
    'allauth.account.middleware.AccountMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'linenow.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'linenow.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

IS_DEPLOY = env('DJANGO_DEPLOY')

# 데이터베이스 설정
if IS_DEPLOY == 'True':
    # 배포 환경: MySQL 사용
    DATABASES = {
        'default': {
            'ENGINE': env('DATABASE_ENGINE'),
            'NAME': env('DATABASE_NAME'),
            'USER': env('DATABASE_USER'),
            'PASSWORD': env('DATABASE_USER_PASSWORD'),
            'HOST': env('DATABASE_HOST'),
            'PORT': env('DATABASE_PORT')
        }
    }
else:
    # 개발 환경: SQLite3 사용 (기본값)
    DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            }
        }


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
# STATIC_ROOT 설정
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# STATIC_URL 설정
STATIC_URL = '/static/'


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# corsheaders
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    # 로컬 개발용 주소
    'http://localhost:3000', 
    'http://localhost:5173', 
    'http://127.0.0.1:3000', 
    'http://127.0.0.1:5173',
    'http://127.0.0.1:8000',

    # 프론트엔드 도메인 또는 IP주소
    
    # 백엔드 도메인 또는 IP주소
    'https://211.188.52.202',
    'https://linenow.xyz',
    'http://linenow-manager.co.kr',
    'https://linenow-manager.co.kr',
    'http://linenow.co.kr',
    'https://linenow.co.kr'
]

# Celery 관련 설정
CELERY_BROKER_URL = env('CELERY_BROKER_URL')  # Redis 브로커 주소
CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND')  # 결과 백엔드 주소

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# SMS 관련 설정
SMS_TOKEN_KEY = env("SMS_TOKEN_KEY")
SMS_API_KEY = env("SMS_API_KEY")
SEND_PHONE = env("SEND_PHONE")
SSODAA_BASE_URL = env("SSODAA_BASE_URL")

# Turnstile 관련 설정
TURNSTILE_SECRET_KEY = env("TURNSTILE_SECRET_KEY")