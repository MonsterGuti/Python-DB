from django.contrib import admin
from main_app.models import *


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'established_date', 'country', 'rating')
    list_filter = ('rating',)
    search_fields = ('name', 'country')


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth_date', 'country', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'country')
    readonly_fields = ('updated_at',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'summary', 'rating', 'main_author', 'publisher')
    list_filter = ('publication_date', 'is_bestseller', 'genre' )
    search_fields = ('title', 'main_author__name')
    readonly_fields = ('updated_at',)
