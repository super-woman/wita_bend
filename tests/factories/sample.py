import factory

from apps.constants.time_zones import timezone
from apps.sample.models import Sample

from .base import BaseFactory


class SampleFactory(BaseFactory):
    class Meta:
        model = Sample

    name = factory.Faker("city")
