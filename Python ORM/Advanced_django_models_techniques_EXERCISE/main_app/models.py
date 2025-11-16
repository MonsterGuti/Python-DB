from decimal import Decimal
from typing import Any

from django.core.validators import RegexValidator, MinValueValidator, EmailValidator, MinLengthValidator
from django.db import models

from main_app.mixins import RechargeEnergyMixin
from main_app.validators import NameValidator

from django.contrib.postgres.search import SearchVectorField
from django.db import models
from django.contrib.postgres.indexes import GinIndex


class Customer(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[NameValidator('Name can only contain letters and spaces')])
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(18, message='Age must be greater than or equal to 18')])
    email = models.EmailField(validators=[EmailValidator('Enter a valid email address')])
    phone_number = models.CharField(max_length=13,
                                    validators=[
                                        RegexValidator(
                                            regex=r'^\+359\d{9}$',
                                            message="Phone number must start with '+359' followed by 9 digits")])
    website_url = models.URLField(
        error_messages={'invalid': 'Enter a valid URL'}
    )


class BaseMedia(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    genre = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ['-created_at', 'title']


class Book(BaseMedia):
    author = models.CharField(max_length=100,
                              validators=[MinLengthValidator(5, 'Author must be at least 5 characters long')])
    isbn = models.CharField(max_length=20, unique=True,
                            validators=[MinLengthValidator(6, 'ISBN must be at least 6 characters long')])

    class Meta(BaseMedia.Meta):
        verbose_name = 'Model Book'
        verbose_name_plural = 'Models of type - Book'


class Movie(BaseMedia):
    director = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(
                limit_value=8,
                message="Director must be at least 8 characters long",
            )
        ],
    )

    class Meta(BaseMedia.Meta):
        verbose_name = "Model Movie"
        verbose_name_plural = "Models of type - Movie"


class Music(BaseMedia):
    artist = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(
                limit_value=9,
                message="Artist must be at least 9 characters long",
            )
        ]
    )

    class Meta(BaseMedia.Meta):
        verbose_name = "Model Music"
        verbose_name_plural = "Models of type - Music"


class Product(models.Model):
    TAX_PERCENT = Decimal('0.08')
    SHIPPING_MULTIPLIER = Decimal('2.00')
    TYPE_PRODUCT = "Product"

    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def calculate_tax(self):
        return self.price * self.TAX_PERCENT

    def calculate_shipping_cost(self, weight: Decimal):
        return weight * self.SHIPPING_MULTIPLIER

    def format_product_name(self):
        return f"Product: {self.name}"


class DiscountedProduct(Product):
    TAX_PERCENT: Decimal = Decimal('0.05')
    SHIPPING_MULTIPLIER: Decimal = Decimal('1.50')
    TYPE_PRODUCT: str = "Discounted Product"
    PRICE_WITHOUT_DISCOUNT_MULTIPLIER = Decimal('0.20')

    def calculate_price_without_discount(self) -> Decimal:
        return Decimal(str(self.price)) * (1 + self.PRICE_WITHOUT_DISCOUNT_MULTIPLIER)

    def format_product_name(self):
        return f'{self.TYPE_PRODUCT}: {self.name}'

    class Meta:
        proxy = True


class Hero(models.Model, RechargeEnergyMixin):
    ABILITY_ENERGY_CONSUMPTION: int = 0

    name = models.CharField(
        max_length=100,
    )

    hero_title = models.CharField(
        max_length=100,
    )

    energy = models.PositiveIntegerField()

    @property
    def required_energy_message(self) -> str:
        return ""

    @property
    def successful_ability_usage_message(self) -> str:
        return ""

    def use_ability(self) -> str:
        if self.energy < self.ABILITY_ENERGY_CONSUMPTION:
            return self.required_energy_message

        self.energy = max(self.energy - self.ABILITY_ENERGY_CONSUMPTION, 1)

        return self.successful_ability_usage_message


class SpiderHero(Hero):
    ABILITY_ENERGY_CONSUMPTION: int = 80

    def swing_from_buildings(self) -> str:
        return self.use_ability()

    @property
    def required_energy_message(self) -> str:
        return f"{self.name} as Spider Hero is out of web shooter fluid"

    @property
    def successful_ability_usage_message(self) -> str:
        return f"{self.name} as Spider Hero swings from buildings using web shooters"

    class Meta:
        proxy = True


class FlashHero(Hero):
    ABILITY_ENERGY_CONSUMPTION: int = 65

    def run_at_super_speed(self) -> str:
        return self.use_ability()

    @property
    def required_energy_message(self) -> str:
        return f"{self.name} as Flash Hero needs to recharge the speed force"

    @property
    def successful_ability_usage_message(self) -> str:
        return f"{self.name} as Flash Hero runs at lightning speed, saving the day"

    class Meta:
        proxy = True


class Document(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    search_vector = SearchVectorField(null=True)

    class Meta:
        indexes = [
            GinIndex(fields=['search_vector']),
        ]

    def __str__(self):
        return self.title
