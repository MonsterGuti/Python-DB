import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Director, Actor, Movie
import datetime
from decimal import Decimal
from django.db.models import Q, Avg, F, Case, When


def populate_db():
    director1 = Director.objects.create(
        full_name='Director One',
        birth_date=datetime.date(1974, 5, 17),
        nationality='North America',
        years_of_experience=5,
    )

    director2 = Director.objects.create(
        full_name='Director Two',
        birth_date=datetime.date(1969, 2, 21),
        nationality='South America',
        years_of_experience=6,
    )

    # Create Actors
    actor1 = Actor.objects.create(
        full_name='Martin Johnson',
        birth_date=datetime.date(1990, 5, 10),
        nationality='North America',
        is_awarded=True,
    )

    actor2 = Actor.objects.create(
        full_name='Petar Ivanov',
        birth_date=datetime.date(1995, 11, 5),
        nationality='South America',
        is_awarded=False,
    )

    movie1 = Movie.objects.create(
        title='Movie One',
        release_date=datetime.date.today(),
        storyline='A movie description.',
        genre='Action',
        rating=Decimal('5.0'),
        is_classic=True,
        is_awarded=False,
        director=director1,
        starring_actor=actor2,
    )
    movie1.actors.set([actor1, actor2])

    movie2 = Movie.objects.create(
        title='Movie Two',
        release_date=datetime.date(2018, 11, 12),
        storyline='Another movie description.',
        genre='Drama',
        rating=Decimal('3.5'),
        is_classic=False,
        is_awarded=True,
        director=director2,
        starring_actor=actor1,
    )
    movie2.actors.set([actor1, actor2])


def get_directors(search_name=None, search_nationality=None):
    if search_name is None and search_nationality is None:
        return ''

    searched_directors = Director.objects.all()

    if search_name is not None and search_nationality is not None:
        searched_directors = Director.objects.filter(
            full_name__icontains=search_name,
            nationality__icontains=search_nationality,
        )

    elif search_name is not None:
        searched_directors = Director.objects.filter(
            full_name__icontains=search_name,
        )

    elif search_nationality is not None:
        searched_directors = Director.objects.filter(
            nationality__icontains=search_nationality,
        )

    if not searched_directors.exists():
        return ''

    searched_directors = searched_directors.order_by('full_name')

    return '\n'.join(
        f"Director: {d.full_name}, nationality: {d.nationality}, experience: {d.years_of_experience}"
        for d in searched_directors
    )


from django.db.models import Count


def get_top_director():
    top_director = (
        Director.objects
        .annotate(num_of_movies=Count('movies'))
        .order_by('-num_of_movies', 'full_name')
        .first()
    )

    if top_director is None:
        return ""

    return f"Top Director: {top_director.full_name}, movies: {top_director.num_of_movies}."


def get_top_actor():
    top_actor = (
        Actor.objects
        .annotate(num_of_movies=Count('starring_roles'))
        .order_by('-num_of_movies', 'full_name')
        .first()
    )

    if top_actor is None or top_actor.num_of_movies == 0:
        return ""

    movies = Movie.objects.filter(starring_actor=top_actor)
    if not movies.exists():
        return ""

    movie_titles = ', '.join(movies.values_list('title', flat=True))

    avg_rating = movies.aggregate(avg=Avg('rating'))['avg']
    avg_rating = f'{avg_rating:.1f}'

    return (
        f"Top Actor: {top_actor.full_name}, "
        f"starring in movies: {movie_titles}, "
        f"movies average rating: {avg_rating}"
    )


def get_actors_by_movies_count():
    top_actors = Actor.objects.annotate(
        num_of_movies=Count('movies_appeared_in')
    ).order_by('-num_of_movies', 'full_name')[:3]

    if not top_actors:
        return ""

    return '\n'.join(
        f"{a.full_name}, participated in {a.num_of_movies} movies"
        for a in top_actors
    )


def get_top_rated_awarded_movie():
    top_movie = Movie.objects.filter(
        is_awarded=True,
    ).order_by('-rating', 'title').first()

    if not top_movie:
        return ""

    starring_actor_name = top_movie.starring_actor.full_name if top_movie.starring_actor else 'N/A'

    cast = top_movie.actors.all().order_by('full_name')
    cast_string = ', '.join(c.full_name for c in cast)

    return (
        f"Top rated awarded movie: {top_movie.title}, rating: {top_movie.rating:.1f}. "
        f"Starring actor: {starring_actor_name}. "
        f"Cast: {cast_string}"
    )


def increase_rating():
    movies_to_update = Movie.objects.filter(
        is_classic=True,
        rating__lt=10.0
    ).update(
        rating=F('rating') + 0.1
    )

    if movies_to_update == 0:
        return "No ratings increased."

    return f"Rating increased for {movies_to_update} movies."
