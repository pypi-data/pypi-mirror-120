import uuid
from time import time
from threading import current_thread

from django.utils.functional import SimpleLazyObject, empty


_THREAD_STORAGES = {}


USER_KEY = 'user'
REQUEST_ID_KEY = 'request_id'
DJANGO_REQUEST_KEY = 'django_request'
DJANGO_RESPONSE_KEY = 'django_response'
RESPONSE_DURATION_KEY = 'response_duration'
REQUEST_START_TIME = 'request_start_time'


def _get_thread_key():
    return current_thread()


def _get_storage():
    thread_key = _get_thread_key()
    storage = _THREAD_STORAGES.get(thread_key)
    if storage is None:
        _THREAD_STORAGES[thread_key] = storage = {}
    return storage


def _get_user():
    user = _get_storage().get(USER_KEY)
    if user:
        return user
    django_request = get_django_request()
    if django_request and hasattr(django_request, 'user'):
        is_empty = (
            isinstance(django_request.user, SimpleLazyObject)
            and django_request.user._wrapped == empty)
        if not is_empty:
            return django_request.user
    return None


def get_django_request():
    return _get_storage().get(DJANGO_REQUEST_KEY)


def get_django_response():
    return _get_storage().get(DJANGO_RESPONSE_KEY)


def get_user_pk():
    user = _get_user()
    if user:
        return user.pk
    return None


def get_username():
    user = _get_user()
    if user:
        return user.username
    return None


def get_remote_addr():
    request = get_django_request()
    if request:
        return request.META['REMOTE_ADDR']


def set_django_request(value):
    _get_storage()[DJANGO_REQUEST_KEY] = value


def set_django_response(value):
    _get_storage()[DJANGO_RESPONSE_KEY] = value


def set_request_start_time():
    _get_storage()[REQUEST_START_TIME] = time()


def get_request_start_time():
    return _get_storage().get(REQUEST_START_TIME)


def set_response_duration(duration):
    _get_storage()[RESPONSE_DURATION_KEY] = duration


def get_response_duration():
    return _get_storage().get(RESPONSE_DURATION_KEY)


def set_request_id():
    _get_storage()[REQUEST_ID_KEY] = uuid.uuid4()


def get_request_id():
    return _get_storage().get(REQUEST_ID_KEY)


def clear_storage():
    _THREAD_STORAGES.pop(_get_thread_key(), None)
