"""
Django settings for remorex project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from dotenv import load_dotenv
from pathlib import Path

import dj_database_url
from django.utils.translation import gettext_lazy as _

load_dotenv()

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    default=str(os.getenv("SECRET_KEY")),
)


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = "RENDER" not in os.environ

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# SECURITY WARNING: don't run with debug turned on in production!

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    ".fly.dev",
    "remorex.onrender.com",
    "remoreks.ee",
    "*",
]

RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Application definition

INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "widget_tweaks",
    "accounts",
    "yard",
    "posts",
    "compressor",
    "storages",
    "coverage",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "remorex.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "remorex.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases


DATABASES = {
    "default": dj_database_url.config(
        default=str(os.getenv("DATABASE_URI")),
        conn_max_age=600,
    )
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib./.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

# LANGUAGE_CODE = "en-us"
LANGUAGE_CODE = "et"
# LANGUAGE_CODE = "ru"
# LANGUAGE_CODE = "de"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

# https://flowbite.com/docs/getting-started/django/
STATICFILES_FINDERS = [
    "compressor.finders.CompressorFinder",
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

COMPRESS_ROOT = BASE_DIR / "static"
COMPRESS_ENABLED = True

if not DEBUG:
    STATIC_ROOT = BASE_DIR / "staticfiles"
    STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

AUTH_USER_MODEL = "accounts.CustomUser"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"

# AWS settings
USE_S3 = os.getenv("USE_S3") == "TRUE"

if os.getenv("USE_S3"):
    # aws settings
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
    AWS_DEFAULT_ACL = None

    # http://bucket-name.s3-website.Region.amazonaws.com/object-name
    AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.eu-north-1.amazonaws.com"

    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}

    PUBLIC_MEDIA_LOCATION = "media"
    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/"

    DEFAULT_FILE_STORAGE = (
        "storages.backends.s3boto3.S3Boto3Storage"  # /remorex/storage_backends.py
    )

LANGUAGES = (
    ("en", _("English")),
    ("et", _("Estonian")),
    ("de", _("German")),
    ("ru", _("Russian")),
)

LOCALE_PATHS = [
    BASE_DIR / "locale",
]

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
DEFAULT_FROM_EMAIL = "remoreks@remoreks.ee"
EMAIL_HOST = "csmtp.telia.ee"

if not DEBUG:
    EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
    EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
else:
    EMAIL_HOST_PASSWORD = str(os.getenv("EMAIL_HOST_PASSWORD"))
    EMAIL_HOST_USER = str(os.getenv("EMAIL_HOST_USER"))

EMAIL_PORT = 587
EMAIL_USE_TLS = True
