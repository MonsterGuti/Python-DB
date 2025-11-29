from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Count


class PublisherManager(models.Manager):
    def get_publishers_by_books_count(self):
        return (
            self.annotate(
                total_books=Count('books')
            ).order_by('-total_books', 'name')
        )


class Publisher(models.Model):
    name = models.CharField(
        validators=[MinLengthValidator(3)],
        max_length=100
    )
    established_date = models.DateField(
        default='1800-01-01'
    )
    country = models.CharField(
        validators=[MaxLengthValidator(40)],
        max_length=40,
        default='TBC'
    )
    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        default=0.0
    )
    objects = PublisherManager()


class Author(models.Model):
    name = models.CharField(
        validators=[MinLengthValidator(3)],
        max_length=100
    )
    birth_date = models.DateField(
        null=True,
        blank=True
    )
    country = models.CharField(
        validators=[MaxLengthValidator(40)],
        max_length=40,
        default='TBC'
    )
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)


class Book(models.Model):
    GENRE_CHOICES = (
        ('Fiction', 'Fiction'),
        ('Non-Fiction', 'Non-Fiction'),
        ('Other', 'Other')
    )

    title = models.CharField(
        validators=[MinLengthValidator(2)],
        max_length=200
    )
    publication_date = models.DateField()
    summary = models.TextField(
        null=True,
        blank=True
    )
    genre = models.CharField(
        choices=GENRE_CHOICES,
        validators=[MaxLengthValidator(11)],
        max_length=11,
        default='Other'
    )
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0.01), MaxValueValidator(9999.99)],
        default=0.01
    )
    rating = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        default=0.0
    )
    is_bestseller = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.CASCADE,
        related_name='books',
    )
    main_author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='main_author',
    )
    co_authors = models.ManyToManyField(
        Author,
        related_name='co_authors',
    )
