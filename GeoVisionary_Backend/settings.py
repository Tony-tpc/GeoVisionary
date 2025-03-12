import os
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-)i*hj365b8ej!-ryhg(7#2x+k-_4xaa)+tiuw7twb_^a1zqbrz"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost','127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'simpleui',
    'import_export',
    'corsheaders',
    'rest_framework',
    'neo4jDB.apps.Neo4JdbConfig',
    'neo4j',
    'neomodel',
    'django_neomodel',
    'daphne',
    "channels",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'users.apps.UsersConfig',
    'proxy.apps.ProxyConfig',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# CORS_ALLOWED_ORIGINS = [
#      "http://localhost:8080",
#      "http://localhost:5173",
#      "https://ketchhub.cn"
# ]
#
CORS_ALLOW_ALL_ORIGINS = True  # 允许所有域（开发阶段）
CORS_ALLOW_CREDENTIALS = True  # 如果前端需要带cookie，设为True

# 允许的请求方法
CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "DELETE",
    "OPTIONS",
]

ROOT_URLCONF = "GeoVisionary_Backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR/'templates']
        ,
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

WSGI_APPLICATION = "GeoVisionary_Backend.wsgi.application"
# 异步处理
ASGI_APPLICATION = "GeoVisionary_Backend.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}

# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels_redis.core.RedisChannelLayer",
#         "CONFIG": {
#             "hosts": [("127.0.0.1", 6379)],
#         },
#     },
# }

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# 数据库名称以及相关账户
load_dotenv()
USER = os.getenv("MYSQL_USER")
PASSWORD = os.getenv("MYSQL_PASSWORD")
HOST = os.getenv("MYSQL_HOST")
PORT = int(os.getenv("MYSQL_PORT"))

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME":"GeoVisionary",
        "USER": USER,
        "PASSWORD": PASSWORD,
        "HOST": HOST,
        "PORT": PORT,
        "OPTIONS": {
            "charset": "utf8mb4",
        },
    },
}

RUN_SERVER_PORT = 8040
NEOMODEL_NEO4J_BOLT_URL = "bolt://neo4j:123456789@localhost:7687"

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "zh-Hans"

TIME_ZONE = 'Etc/GMT-8'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"

STATICFILES_DIRS = [BASE_DIR/"static"]

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR/"media"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'users.authentication.JWTAuthentication',
    ),
}

SIMPLEUI_CONFIG = {
    'system_keep': True,
    'menu_display': ['学习系统管理', '权限与用户管理','前台访问管理'],
    'dynamic': True,    # 设置是否开启动态菜单, 默认为False. 如果开启, 则会在每次用户登陆时动态展示菜单内容
    'menus': [{
        'name': '学习系统管理',
        'icon':"fa fa-graduation-cap",
        'models':[{
            'name':'用户信息',
            'icon':'fa fa-user',
            'url':'/admin/users/frontenduser/',
        },{
            'name': '试题分类',
            'icon': 'fa fa-folder-open',
            'url': '/admin/users/category/',
        },{
            'name': '题组',
            'icon': 'fa fa-th-large',
            'url': '/admin/users/examset/',
        },{
            'name': '题目',
            'icon': 'fa fa-file-text',
            'url': '/admin/users/problem/',
        },{
            'name': '用户错题记录',
            'icon': 'fa fa-history',
            'url': '/admin/users/userhistory/',
        },{
            'name': '用户对话记录',
            'icon': 'fa fa-comments',
            'url': '/admin/users/userconversation/',
        },{
            'name': 'API 管理',
            'icon': 'fa fa-cogs',
            'url': '/admin/users/apiconfig/',
        }],
    },{
        'name':'权限与用户管理',
        'icon':"fa fa-users-cog",
        'models':[
            {
                'name':'用户',
                'url':'/admin/auth/user/',
                'icon':'fas fa-user'
            },{
                'name': '组',
                'url': '/admin/auth/group/',
                'icon':"fa-solid fa-users-gear"
            }]
    }],
}

SIMPLEUI_HOME_INFO = False

LOCALE_PATHS = [BASE_DIR/"locale",]

JWT_CONFIG = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),  # access_token 过期时间
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),  # refresh_token 过期时间
    "ALGORITHM": "HS256",
}