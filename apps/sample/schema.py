
from ..utils.base_schema import BaseSchema

from .models import Sample


class SampleSchema(BaseSchema):
    class Meta:
        model = Sample
