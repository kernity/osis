from django.core.management.base import BaseCommand, CommandError


def create_record(model_class, **kwargs):
    model_class.objects.create(**kwargs)

