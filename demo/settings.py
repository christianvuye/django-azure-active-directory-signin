"""
Django settings for demo project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-c4na0q5cvl41df&nby(wo%)5vk*rv_c#n!y)ss^8-)c2_96m6@"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "user",
    "tests",
    # thirdparty
    "sslserver",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "demo.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["demo/templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "demo.context_processors.context",
            ],
        },
    },
]

WSGI_APPLICATION = "demo.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

AUTH_USER_MODEL = "user.ExtendedUser"


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

"""
SECURE_SSL_REDIRECT
https://docs.djangoproject.com/en/3.1/ref/settings/#secure-proxy-ssl-header
"""

SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

"LOGGING"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {
            "format": "{asctime} {levelname} {name} {message}",
            "style": "{",
        }
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "console"},
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG" if DEBUG else "INFO",
    },
}


# Enable your Python Django web app to sign in users to your Azure Active Directory tenant with the Microsoft identity platform
# https://github.com/Azure-Samples/ms-identity-python-django-tutorial/tree/main/1-Authentication/sign-in

from ms_identity_web.configuration import AADConfig
from ms_identity_web import IdentityWebPython

AAD_CONFIG = AADConfig.parse_json(file_path=os.environ.get("AAD_CONFIG_PATH"))
MS_IDENTITY_WEB = IdentityWebPython(AAD_CONFIG)
ERROR_TEMPLATE = (
    "auth/{}.html"  # for rendering 401 or other errors from msal_middleware
)
MIDDLEWARE.append("ms_identity_web.django.middleware.MsalMiddleware")


# Django Azure AD Sign-In
# https://pypi.org/project/django-azure-active-directory-signin/

INSTALLED_APPS += [
    "azure_signin",
]

AZURE_SIGNIN = {
    "CLIENT_ID": os.environ.get("AZAD_CLIENT_ID"),
    "CLIENT_SECRET": os.environ.get("AZAD_SECRET_ID"),
    "TENANT_ID": os.environ.get("AZAD_TENANT_ID"),
    "RENAME_ATTRIBUTES": [
        ("employeeNumber", "employee_id"),
        ("sduAppKtoOmkostningssted", "omk2"),
        ("sduAppDKDepartmentNumber", "hcm"),
    ],
    # Permissions
    # https://docs.microsoft.com/en-us/graph/api/user-get?view=graph-rest-1.0&tabs=http#permissions
    "SCOPES": [
        "User.Read",
        "User.ReadBasic.All",
    ],
}

AUTHENTICATION_BACKENDS += [
    "azure_signin.backends.AzureSigninBackend",
]

LOGIN_URL = "azure_signin:login"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = LOGIN_REDIRECT_URL
