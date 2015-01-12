# -*- coding: utf-8 -*-
import warnings
from ws4redis import settings
from ws4redis.redis_store import (RedisMessage,
                                  RedisStore, )

from kafka.client import KafkaClient

from kafka.producer import SimpleProducer

def ConnectionFactory(**kwargs):
    print kwargs
    addr = "%s:%d" % (kwargs['host'], kwargs['port'],)
    print "KafkaClient connecting to ", addr
    return KafkaClient(addr)

class KafkaMessage(RedisMessage):
    """
    A class wrapping messages to be send and received through KafkaStore. This class behaves like
    a normal string class, but silently discards heartbeats and converts messages received from
    Kafka.
    """
    pass

class KafkaStore(RedisStore):
    """
    Abstract base class to control publishing and subscription for messages to and from the Redis
    datastore.
    """
    _expire = settings.WS4REDIS_EXPIRE

    def __init__(self, client):
        super(KafkaStore, self).__init__(client)
        self._producer = SimpleProducer(self._connection)


    def publish_message(self, message, expire=None):
        """
        Publish a ``message`` on the subscribed channel on the Redis datastore.
        ``expire`` sets the time in seconds, on how long the message shall additionally of being
        published, also be persisted in the Redis datastore. If unset, it defaults to the
        configuration settings ``WS4REDIS_EXPIRE``.
        """
        print __name__

        expire = expire is None and self._expire or expire
        if not isinstance(message, KafkaMessage):
            raise ValueError('message object is not of type KafkaMessage')
        for channel in self._publishers:
            self._connection.send_messages(channel, message)


    @staticmethod
    def get_prefix():
        return settings.WS4REDIS_PREFIX and '{0}:'.format(settings.WS4REDIS_PREFIX) or ''
