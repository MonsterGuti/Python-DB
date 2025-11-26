from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db.models import Count


class PersonBase(models.Model):
    full_name = models.CharField(
        max_length=120,
        validators=[MinLengthValidator(2)]
    )
    birth_date = models.DateField(default='1900-01-01')
    nationality = models.CharField(max_length=50, default='Unknown')

    class Meta:
        abstract = True


class DirectorManager(models.Manager):
    def get_directors_by_movies_count(self):
        return self.annotate(
            movies_count=Count('movies')
        ).order_by('-movies_count', 'full_name')


class Director(PersonBase):
    years_of_experience = models.SmallIntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )
    objects = DirectorManager()


class Actor(PersonBase):
    is_awarded = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)


class Movie(models.Model):
    GENRES = (
        ('Action', 'Action'),
        ('Comedy', 'Comedy'),
        ('Drama', 'Drama'),
        ('Other', 'Other'),
    )

    title = models.CharField(
        max_length=150,
        validators=[MinLengthValidator(5)]
    )
    release_date = models.DateField()
    storyline = models.TextField(null=True, blank=True)

    genre = models.CharField(
        max_length=6,
        choices=GENRES,
        default='Other'
    )

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)]
    )

    is_classic = models.BooleanField(default=False)
    is_awarded = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)

    director = models.ForeignKey(
        Director,
        on_delete=models.CASCADE,
        related_name='movies'
    )

    starring_actor = models.ForeignKey(
        Actor,
        null=True,
        on_delete=models.SET_NULL,
        related_name='starring_roles'
    )

    actors = models.ManyToManyField(
        Actor,
        related_name='movies_appeared_in'
    )
