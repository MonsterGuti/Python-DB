import datetime
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models
from django.db.models import Count


class HouseManager(models.Manager):
    def get_houses_by_dragons_count(self):
        return self.annotate(
            total_dragons=Count('dragon'),
        ).order_by('-total_dragons', 'name')


class House(models.Model):
    name = models.CharField(
        max_length=80,
        validators=[MinLengthValidator(5)],
        unique=True,
    )
    motto = models.TextField(
        null=True,
        blank=True,
    )
    is_ruling = models.BooleanField(
        default=False,
    )
    castle = models.CharField(
        max_length=80,
        null=True,
        blank=True,
    )
    wins = models.SmallIntegerField(
        default=0,
    )
    modified_at = models.DateTimeField(
        auto_now=True,
    )

    objects = HouseManager()


class Dragon(models.Model):
    BREATH_CHOICES = (
        ('Fire', 'Fire'),
        ('Ice', 'Ice'),
        ('Lightning', 'Lightning'),
        ('Unknown', 'Unknown'),
    )

    name = models.CharField(
        max_length=80,
        validators=[MinLengthValidator(5)],
        unique=True,
    )
    power = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(1.0), MaxValueValidator(10.0)],
        default=1.0,
    )
    breath = models.CharField(
        max_length=9,
        choices=BREATH_CHOICES,
        default='Unknown',
    )
    is_healthy = models.BooleanField(
        default=True
    )
    birth_date = models.DateField(
        default=datetime.date.today,
    )
    wins = models.SmallIntegerField(
        default=0,
    )
    modified_at = models.DateTimeField(
        auto_now=True,
    )
    house = models.ForeignKey(
        House,
        on_delete=models.CASCADE,
    )


class Quest(models.Model):
    name = models.CharField(
        max_length=80,
        validators=[MinLengthValidator(5)],
        unique=True,
    )
    code = models.CharField(
        max_length=4,
        validators=[
            RegexValidator(regex=r'^[A-Za-z#]{4}$')
        ],
        unique=True,
    )
    reward = models.FloatField(
        default=100.0,
    )
    start_time = models.DateTimeField()
    modified_at = models.DateTimeField(
        auto_now=True,
    )
    dragons = models.ManyToManyField(Dragon)
    host = models.ForeignKey(
        House,
        on_delete=models.CASCADE,
    )
