import datetime
import os
import django
from django.db.models import Q, Avg, F, When, Value, DecimalField
from sqlparse.sql import Case

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import *


def populate_db():
    publisher1 = Publisher.objects.create(
        name='Martin',
        established_date=datetime.date.today(),
        country='US',
        rating=4.5
    )
    publisher2 = Publisher.objects.create(
        name='Georgi',
        established_date=datetime.date(1997, 5, 4),
        country='UK',
        rating=3.7
    )

    author1 = Author.objects.create(
        name='Neno',
        birth_date=datetime.date(2005, 8, 8),
        country='UK',
        is_active=True,
    )
    author2 = Author.objects.create(
        name='Ivo',
        birth_date=datetime.date(2005, 3, 7),
        country='US',
        is_active=False,
    )

    book1 = Book.objects.create(
        title='Book 1',
        publication_date=datetime.date.today(),
        summary='A book',
        genre='Fiction',
        price=26.00,
        rating=4.2,
        is_bestseller=True,
        publisher=publisher1,
        main_author=author2,
    )
    book1.co_authors.add(author2, author1)
    book2 = Book.objects.create(
        title='Book 2',
        publication_date=datetime.date(2025, 7, 3),
        summary='A book 2',
        genre='Non-Fiction',
        price=23.50,
        rating=4.1,
        is_bestseller=False,
        publisher=publisher2,
        main_author=author1,
    )
    book2.co_authors.add(author2, author1)


def get_publishers(search_string=None):
    if not search_string:
        return "No search criteria."

    publishers = Publisher.objects.filter(
        Q(name__icontains=search_string) | Q(country__icontains=search_string)
    ).order_by('-rating', 'name')

    if not publishers.exists():
        return "No publishers found."

    return '\n'.join(
        f"Publisher: {p.name}, country: {p.country}, rating: {p.rating}"
        for p in publishers
    )


def get_top_publisher():
    top_publisher = Publisher.objects.annotate(
        total_books=Count('books')
    ).order_by('-total_books', 'name').first()

    if not top_publisher:
        return "No publishers found."

    return f"Top Publisher: {top_publisher.name} with {top_publisher.total_books} books."


def get_top_main_author():
    top_main_author = Author.objects.annotate(
        total_books=Count('main_author')
    ).order_by('-total_books', 'name').first()

    if top_main_author is None or top_main_author.total_books == 0:
        return "No results."

    average_rating = Book.objects.filter(main_author=top_main_author).aggregate(
        avg_rating=Avg('rating')
    )['avg_rating']

    author_books = [b.title for b in Book.objects.filter(main_author=top_main_author)]
    books_string = ', '.join(author_books)

    return (
        f"Top Author: {top_main_author.name}, own book titles: {books_string},"
        f" books average rating: {average_rating}"
    )


def get_authors_by_books_count():
    authors = Author.objects.annotate(
        main_count=Count('main_author'),
        co_count=Count('co_authors', distinct=True)
    ).filter(main_count__gt=0).annotate(
        total_books=F('main_count') + F('co_count')
    ).filter(total_books__gt=0).order_by('-total_books', 'name')[:3]

    if not authors:
        return "No results."

    return '\n'.join(
        f"{author.name} authored {author.total_books} books."
        for author in authors
    )


def get_bestseller():
    top_book = Book.objects.annotate(
        total_authors=Count('co_authors', distinct=True),
        composed_index=F('total_authors') + F('rating') + 1
    ).order_by('-composed_index', '-rating', '-total_authors', 'title').first()

    if not top_book:
        return "No results."

    co_authors = top_book.co_authors.all().order_by('name')
    co_authors_string = '/'.join(a.name for a in co_authors) if co_authors else 'N/A'

    return (
        f"Top bestseller: {top_book.title}, index: {top_book.composed_index:.1f}."
        f" Main author: {top_book.main_author.name}."
        f" Co-authors: {co_authors_string}."
    )


def increase_price():
    books_to_update = Book.objects.filter(
        publication_date__year=2025
    ).annotate(
        total_rating=F('rating') + F('publisher__rating')
    ).filter(total_rating__gte=8.0)

    if not books_to_update.exists():
        return "No changes in price."

    updated_books = books_to_update.update(
        price=Case(
            When(price__gt=50.0, then=F('price') * 1.1),
            default=F('price') * 1.2,
            output_field=DecimalField(max_digits=10, decimal_places=2)
        )
    )

    return (
        f"Prices increased for {updated_books} book/s."
    )
