import string

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class NameValidator:
    def __init__(self, message=None):
        self.message = message

    def __call__(self, value):
        for char in value:
            if not char.isalpha() or not char.isspace():
                raise ValidationError(self.message)
