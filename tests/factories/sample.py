import factory

from apps.sample.models import Sample

from .base import BaseFactory


class SampleFactory(BaseFactory):
    class Meta:
        model = Sample

    name = factory.Faker("city")
