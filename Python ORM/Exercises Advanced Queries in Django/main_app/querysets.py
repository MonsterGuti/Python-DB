from decimal import Decimal

from django.db import models
from django.db.models import QuerySet


class RealEstateListingQuerySet(models.QuerySet):
    def by_property_type(self, property_type: str):
        return self.filter(property_type=property_type)

    def in_price_range(self, min_price: Decimal, max_price: Decimal):
        return self.filter(price__range=[min_price, max_price])

    def with_bedrooms(self, bedrooms_count: int):
        return self.filter(bedrooms=bedrooms_count)


class VideoGameQuerySet(models.QuerySet):
    def games_by_genre(self, genre: str):
        return self.filter(genre=genre)

    def recently_released_games(self, year: int):
        return self.filter(release_year__gte=year)

