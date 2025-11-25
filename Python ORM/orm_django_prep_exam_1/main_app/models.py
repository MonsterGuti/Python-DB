from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Count


class TimeStampedModel(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class ProfileManager(models.Manager):
    def get_regular_customers(self):
        return (
            self.annotate(num_of_orders=Count('order'))
            .filter(num_of_orders__gt=2).order_by('-num_of_orders')
        )




class Profile(TimeStampedModel):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name

    objects = ProfileManager()


class Product(TimeStampedModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    in_stock = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Order(TimeStampedModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id}"
