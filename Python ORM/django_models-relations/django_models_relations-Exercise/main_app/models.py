from datetime import timedelta

from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=40)


class Book(models.Model):
    title = models.CharField(max_length=40)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)


class Song(models.Model):
    title = models.CharField(max_length=100, unique=True)


class Artist(models.Model):
    name = models.CharField(max_length=100, unique=True)
    songs = models.ManyToManyField(Song, related_name='artists')


class Product(models.Model):
    name = models.CharField(max_length=100)


class Review(models.Model):
    description = models.TextField(max_length=200)
    rating = models.PositiveSmallIntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')


class Driver(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)


class DrivingLicense(models.Model):
    license_number = models.CharField(max_length=10)
    issue_date = models.DateField()
    driver = models.OneToOneField(Driver, on_delete=models.CASCADE, related_name='licenses')

    @property
    def get_expiration_date(self):
        return self.issue_date + timedelta(days=365)

    def __str__(self):
        return f"License with number: {self.license_number} expires on {self.get_expiration_date}!"


class Owner(models.Model):
    name = models.CharField(max_length=50)


class Car(models.Model):
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, blank=True, null=True, related_name='cars')


class Registration(models.Model):
    registration_number = models.CharField(max_length=10, unique=True)
    registration_date = models.DateField(blank=True, null=True)
    car = models.OneToOneField(Car, on_delete=models.CASCADE, blank=True, null=True, related_name='registration')


