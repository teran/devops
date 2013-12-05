import os

DRIVER = 'devops.driver.libvirt.libvirt_driver'
DRIVER_PARAMETERS = {
    'connection_string': os.environ.get('CONNECTION_STRING', 'qemu+tcp://127.0.0.1:16509/system'),
    'storage_pool_name': os.environ.get('STORAGE_POOL_NAME', 'default'),
}

INSTALLED_APPS = ['devops']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        'TEST_CHARSET': 'UTF8'
    }
}

SECRET_KEY = 'dummykey'

