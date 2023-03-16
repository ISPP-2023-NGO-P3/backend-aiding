# This file is used to override settings for deploy

import environ

env= environ.Env()
environ.env.read_env()

root_password=env('ROOT_PASSWORD')
db_url = env('DATABASE_URL')



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'aiding_db',
        'USER': 'root',
        'PASSWORD': + root_password ,
        'HOST': + db_url ,
        'PORT': '5432',
    }
}