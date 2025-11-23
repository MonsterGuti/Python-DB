from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class RangeValidator:
    def __init__(self, min, max, message):
        self.min = min
        self.max = max
        self.message = message

    def __call__(self, value):
        if not (self.min <= value <= self.max):
            raise ValidationError(self.message)


@deconstructible
class ReleaseYearValidator:
    def __init__(self, min_year, max_year, message):
        self.min_year = min_year
        self.max_year = max_year
        self.message = message

    def __call__(self, value):
        if not (self.min_year <= value <= self.max_year):
            raise ValidationError(self.message)
