# django-logging-context

## Description
`django-logging-context` is BSD licensed library extending default django 
logging context with following additional values:

- request id,
- request duration,
- remote address,
- response length,
- user id,
- username.

## Quick start

1. install the library:
```bash
pip install django-logging-context -y
```

2. Add `django-logging-context` to your `INSTALLED_APPS` setting like this:
```Python
    INSTALLED_APPS = [
        ...
        'django_logging_context',
    ]
```

3. Add proxy middleware to your `MIDDLEWARE` setting like this:
```Python
MIDDLEWARE = [
    'django_logging_context.middlewares.LoggingContextMiddleware',
    ...
]
```
It's important to place this `LoggingContextMiddleware` at the first place in 
a `MIDDLEWARE` to allow to calculate duration of response more precisely.

4. If you just want to add info about request duration and request id to your 
   log records then you can use `LoggingWSGIMiddleware` in your `wsgi.py` like
   this:
```Python
from django_logging_context.wsgi import LoggingWSGIMiddleware
application = LoggingWSGIMiddleware(get_wsgi_application())
```

5. Use this example of logging setting to set up your loggers correctly

```Python
import os

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
DB_LOG_LEVEL = os.environ.get('DB_LOG_LEVEL', LOG_LEVEL)
REQUESTS_LOG_LEVEL = os.environ.get('REQUESTS_LOG_LEVEL', LOG_LEVEL)
CELERY_LOG_LEVEL = os.environ.get('CELERY_LOG_LEVEL', LOG_LEVEL)
SENTRY_LOG_LEVEL = os.environ.get('SENTRY_LOG_LEVEL', LOG_LEVEL)

LOGGING = {
    'version': 1,
    'loggers': {
        'django': {'level': LOG_LEVEL},
        'django.db': {'level': DB_LOG_LEVEL},
        'urllib3': {'level': REQUESTS_LOG_LEVEL},
        'celery': {'level': CELERY_LOG_LEVEL},
        'sentry': {'level': SENTRY_LOG_LEVEL},
    },
    'root': {
        'level': LOG_LEVEL,
        'handlers': ['console']
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'filters': ['extending_context_filter']
        }
    },
    'filters': {
        'extending_context_filter': {
            '()': 'django_logging_context.logging.ContextExtendingFilter'
        }
    },
    'formatters': {
        'verbose': {
            'format': ('[django] %(levelname)s %(asctime)s'
                       ' %(name)s/%(module)s'
                       ' %(process)d/%(thread)d'
                       ' request_id: %(request_id)s'
                       ' remote_addr: %(remote_addr)s'
                       ' user_id: %(user_id)s'
                       ' username: %(username)s'
                       ' duration: %(response_duration)s'
                       ' uri: %(uri)s'
                       '  %(message)s')
        },
    },
}
```

## Log records example
```log
[django] INFO 2021-04-08 18:12:13,573 django.server/basehttp 47385/123145535799296 request_id: ea9a2dfd-a662-4632-84d0-d0c5151b5422 remote_addr: 127.0.0.1 user_id: 2 username: root duration: 1.548695s uri: http://127.0.0.1:8000/login/?next=/ "GET /admin/ HTTP/1.1" 200 46937
```
