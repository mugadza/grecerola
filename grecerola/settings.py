import os
import ast
import django_heroku

def get_bool_from_env(name, default_value):
    if name in os.environ:
        value = os.environ[name]
        try:
            return ast.literal_eval(value)
        except ValueError as e:
            raise ValueError("{} is invalid value for {}".format(value, name)) from e
    return default_value

def get_value_from_env(name, default_value):
    if name in os.environ:
        return os.environ[name]
    return default_value

def get_list(txt):
    return [item.strip() for item in txt.split(",")]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = get_bool_from_env("DEBUG", True)

ALLOWED_HOSTS = get_list(os.environ.get("ALLOWED_HOSTS", "localhost, tatendamugadza.herokuapp.com"))

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'grecerola.core',
    'grecerola.account',
    'grecerola.campaign',
    'grecerola.investment',
    'grecerola.wallet',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'grecerola.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'grecerola.context_processors.add_campaign_types_to_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'grecerola.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': get_value_from_env("DBNAME", 'campaign_development'),
        'USER': get_value_from_env("DBUSER", 'db_admin'),
        'PASSWORD': get_value_from_env("DBPASSWORD",'ElephantsFly'),
        'HOST': get_value_from_env("DBHOST",'localhost'),
        'PORT': get_value_from_env("DBPORT",'3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}

AUTH_USER_MODEL = "account.User"

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        "OPTIONS": {"min_length": 8},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEFAULT_CURRENCY = os.environ.get("DEFAULT_CURRENCY", "ZAR")
DEFAULT_DECIMAL_PLACES = 2
DEFAULT_MAX_DIGITS = 12
DEFAULT_CURRENCY_CODE_LENGTH = 3


VERSATILEIMAGEFIELD_RENDITION_KEY_SETS = {
    "campaigns": [
        ("campaign_gallery", "thumbnail__540x540"),
        ("campaign_gallery_2x", "thumbnail__1080x1080"),
        ("campaign_small", "thumbnail__60x60"),
        ("campaign_small_2x", "thumbnail__120x120"),
        ("campaign_list", "thumbnail__255x255"),
        ("campaign_list_2x", "thumbnail__510x510"),
    ],
    "background_images": [("header_image", "thumbnail__1080x440")],
    "user_avatars": [("default", "thumbnail__445x445")],
}

VERSATILEIMAGEFIELD_SETTINGS = {
    # Images should be pre-generated on Production environment
    "create_images_on_demand": get_bool_from_env("CREATE_IMAGES_ON_DEMAND", DEBUG)
}

PLACEHOLDER_IMAGES = {
    60: "images/placeholder60x60.png",
    120: "images/placeholder120x120.png",
    255: "images/placeholder255x255.png",
    540: "images/placeholder540x540.png",
    1080: "images/placeholder1080x1080.png",
}

DEFAULT_PLACEHOLDER = "images/placeholder255x255.png"



SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

ENABLE_SSL = get_bool_from_env("ENABLE_SSL", False)

if ENABLE_SSL:
    SECURE_SSL_REDIRECT = not DEBUG


MEDIA_ROOT = os.path.join(PROJECT_ROOT, "media")
MEDIA_URL = os.environ.get("MEDIA_URL", "/media/")

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

LOGIN_REDIRECT_URL = 'campaign-home'
LOGIN_URL = 'account-login'

django_heroku.settings(locals())