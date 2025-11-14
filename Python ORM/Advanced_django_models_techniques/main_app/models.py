from wsgiref.validate import validator

from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import PositiveIntegerField

from main_app.validators import validate_menu_categories


class Restaurant(models.Model):
    name = models.CharField(max_length=100,
                            validators=[validators.MinLengthValidator(2, 'Name must be at least 2 characters long.'),
                                        validators.MaxLengthValidator(100, 'Name cannot exceed 100 characters.')])
    location = models.CharField(max_length=200,
                                validators=[
                                    validators.MinLengthValidator(2, 'Location must be at least 2 characters long.'),
                                    validators.MaxLengthValidator(200, 'Location cannot exceed 200 characters."')])
    description = models.TextField(null=True, blank=True)
    rating = models.DecimalField(decimal_places=2, max_digits=3,
                                 validators=[validators.MinValueValidator(0.0, 'Rating must be at least 0.00.'),
                                             validators.MaxValueValidator(5.00, 'Rating cannot exceed 5.00.')])


class Menu(models.Model):
    name = models.CharField(max_length=100, )
    description = models.TextField(validators=[validate_menu_categories])
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)


class ReviewMixin(models.Model):
    rating = PositiveIntegerField(validators=[validators.MaxValueValidator(5)])
    review_content = models.TextField()

    class Meta:
        abstract = True
        ordering = ['-rating']


class RestaurantReview(ReviewMixin):
    class Meta(ReviewMixin.Meta):
        abstract = True
        ordering = ['-rating']
        verbose_name = 'Restaurant Review'
        verbose_name_plural = 'Restaurant Reviews'
        unique_together = ('reviewer_name', 'restaurant')

    reviewer_name = models.CharField(max_length=100)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    review_content = models.TextField()
    rating = PositiveIntegerField(validators=[validators.MaxValueValidator(5)])


class RegularRestaurantReview(RestaurantReview):
    class Meta:
        unique_together = ('reviewer_name', 'restaurant')


class FoodCriticRestaurantReview(RestaurantReview):
    food_critic_cuisine_area = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Food Critic Review'
        verbose_name_plural = 'Food Critic Reviews'
        unique_together = ('reviewer_name', 'restaurant')
        ordering = ['-rating']


class MenuReview(ReviewMixin):
    reviewer_name = models.CharField(max_length=100)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    review_content = models.TextField()
    rating = PositiveIntegerField(validators=[validators.MaxValueValidator(5)])

    class Meta:
        ordering = ['-rating']
        verbose_name = 'Menu Review'
        verbose_name_plural = 'Menu Reviews'
        unique_together = ('reviewer_name', 'menu')
        indexes = [models.Index(fields=['menu'], name='main_app_menu_review_menu_id')]
