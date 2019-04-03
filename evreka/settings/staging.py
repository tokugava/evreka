import django_heroku

from .base import *

DEBUG = True

INSTALLED_APPS += ('storages',)

MIDDLEWARE += ('whitenoise.middleware.WhiteNoiseMiddleware',)

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/

#STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

AWS_QUERYSTRING_AUTH = False
AWS_S3_REGION_NAME = os.environ['AWS_REGION']
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = os.environ['S3_BUCKET_NAME']
AWS_DEFAULT_ACL = 'public-read-write'
AWS_BUCKET_ACL = 'public-read-write'
MEDIA_ROOT = 'http://%s.s3.amazonaws.com/test' % AWS_STORAGE_BUCKET_NAME
AWS_S3_ENDPOINT_URL = MEDIA_ROOT
AWS_S3_HOST = 's3.%s.amazonaws.com' % AWS_S3_REGION_NAME

# Activate Django-Heroku.
django_heroku.settings(locals())
