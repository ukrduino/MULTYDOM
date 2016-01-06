import os
import sys

TRIM_PATH = 0
TRIM_PATH_PROD = 0
SITE_ADDR = "http://127.0.0.1:8000"

if sys.platform.startswith('win32'):
    TRIM_PATH = 30
    TRIM_PATH_PROD = 28
if sys.platform.startswith('linux'):
    TRIM_PATH = 24
    SITE_ADDR = "http://multydom.pythonanywhere.com/"
if sys.platform.startswith('darwin'):
    TRIM_PATH = 39


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

SECRET_KEY = 'ir2u0zd7gpxfad@d5eocvwdn0ulmb@9*k)^4*whtupzyo$qcca'

DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = (
    'django_admin_bootstrapped',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'store',
    'management',
    'cart',
    #http://django-imagekit.readthedocs.org/en/latest/
    'imagekit',
    'bootstrap3',
    'captcha',
    'mptt',
    'ckeditor',
)

DEBUG_APPS = ('debug_toolbar',)

if not sys.platform.startswith('linux'):
    if DEBUG:
        INSTALLED_APPS += DEBUG_APPS

MIDDLEWARE_CLASSES = (

    'debug_toolbar.middleware.DebugToolbarMiddleware',  # comment on pythonanywhere
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'MULTYDOM.urls'

WSGI_APPLICATION = 'MULTYDOM.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,  'templates'),
)

# https://github.com/django-admin-bootstrapped/django-admin-bootstrapped
DAB_FIELD_RENDERER = 'django_admin_bootstrapped.renderers.BootstrapFieldRenderer'
#
#
# #In your templates, load the bootstrap3 library and use the bootstrap_* tags
# #https://github.com/dyve/django-bootstrap3
#
#
#  доступ к сессии из шаблона
TEMPLATE_CONTEXT_PROCESSORS = (  # http://stackoverflow.com/questions/2551933/
                                 # django-accessing-session-variables-from-within-a-template
    'django.core.context_processors.request',
    # 'django.core.context_processors.media',
    # 'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'django.contrib.auth.context_processors.auth'
)
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'multydom2015@gmail.com'
EMAIL_HOST_PASSWORD = 'sashailina1'
EMAIL_USE_TLS = True
# отправитель магазин
DEFAULT_FROM_EMAIL = "multydom2015@gmail.com"
# получатель хозяин/менеджер магазина
DEFAULT_TO_EMAIL = 'vlasov_com@mail.ru'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

#CAPTCHA_FONT_SIZE ='30'
CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.math_challenge'
CAPTCHA_LETTER_ROTATION = (-5, 5)
CAPTCHA_BACKGROUND_COLOR = 'white'
CAPTCHA_FOREGROUND_COLOR = '#000'
CAPTCHA_NOISE_FUNCTIONS = ()