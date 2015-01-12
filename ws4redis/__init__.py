# -*- coding: utf-8 -*-
__version__ = '0.4.3'

from . import settings
from django.utils.importlib import import_module


def _dynamic_load_module(name):
    comps = str(name).split('.')
    module = import_module('.'.join(comps[:-1]))
    return getattr(module, comps[-1])

Message = _dynamic_load_module(settings.WS4REDIS_MESSAGE)
Subscriber = _dynamic_load_module(settings.WS4REDIS_SUBSCRIBER)
Publisher = _dynamic_load_module(settings.WS4REDIS_PUBLISHER)
Connection = _dynamic_load_module(settings.WS4REDIS_CONNECTION_FACTORY)
from ws4redis.redis_store import SELF


def publish_message(message, **kwargs):
    publisher = Publisher(**kwargs)
    publisher.publish_message(Message(message))
