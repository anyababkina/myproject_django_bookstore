import pytest

from books.models import *


@pytest.fixture(scope='function')
def create_db(db):
    Genre.objects.bulk_create([
        Genre(name='Художественная литература'),
        Genre(name='Нехудожественная литература')])
    SubGenre.objects.bulk_create([
        SubGenre(name='Детективы', genre=Genre.objects.get(id=1)),
        SubGenre(name='История', genre=Genre.objects.get(id=2))])
    Author.objects.bulk_create([
        Author(author_name='Булгаков'),
        Author(author_name='Неизвестно')])
    Book.objects.bulk_create([
        Book(title='Капитанская дочка', price=200, amount=2, subgenre=SubGenre.objects.get(id=1)),
        Book(title='Мастер и Маргарита', price=100, amount=10, subgenre=SubGenre.objects.get(id=1)),
        Book(title='Средневековье', price=120, amount=9, subgenre=SubGenre.objects.get(id=2))])
