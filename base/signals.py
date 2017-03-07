import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from pika.exceptions import ChannelClosed, ConnectionClosed
from osis_common.queue import queue_serializer, queue_sender
from osis_common.models.serializable_model import SerializableModel

LOGGER = logging.getLogger(settings.DEFAULT_LOGGER)

@receiver(post_save)
def send_to_queue_save(sender, instance, **kwargs):
    if issubclass(sender, SerializableModel):
        kwargs['to_delete'] = False
        _send_to_queue(sender, instance, **kwargs)


@receiver(post_delete)
def send_to_queue_delete(sender, instance, **kwargs):
    if issubclass(sender, SerializableModel):
        kwargs['to_delete'] = True
        _send_to_queue(sender, instance,**kwargs)


def _send_to_queue(sender, instance, **kwargs):
    if hasattr(settings, 'QUEUES'):
        try :
            instance_serialized = {'body': queue_serializer.serialize(instance), 'to_delete': kwargs.get('to_delete')}
            queue_sender.send_message(settings.QUEUES.get('QUEUES_NAME').get('MIGRATIONS_TO_PRODUCE'),
                                      instance_serialized)
        except (ChannelClosed, ConnectionClosed):
            LOGGER.exception('QueueServer is not installed or not launched')