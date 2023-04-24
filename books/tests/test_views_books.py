import pytest
from django.db.models import Q
from django.urls import reverse
from books.models import *


@pytest.mark.django_db
@pytest.mark.usefixtures('create_db')
class TestBookStore:
    @pytest.mark.parametrize('urls', ['home', 'contacts', 'store'])
    def test_home_store_and_contact_page(self, client, urls):
        url = reverse(urls)
        response = client.get(url)
        assert response.status_code == 200
        if urls == 'store':
            assert list(response.context['book']) == list(Book.objects.filter(amount__gt=0).all())
            urlparams = reverse(urls) + '?order-by=price'
            responseparams = client.get(urlparams)
            assert responseparams.status_code == 200
            assert list(responseparams.context['book']) == list(Book.objects.filter(amount__gt=0).all().order_by('price'))

    @pytest.mark.parametrize('urls, ids, filters', [('genres', 'genre_id', Book.objects.filter(subgenre__genre__id=1, amount__gt=0)),
                                                    ('subgenres', 'subgenre_id', Book.objects.filter(subgenre__id=1, amount__gt=0))])
    def test_genres_page(self, client, urls, ids, filters):
        url = reverse(urls, kwargs={ids: 1})
        response = client.get(url)
        assert response.status_code == 200
        assert response.context['book'] == list(filters)
        urlparams = reverse(urls, kwargs={ids: 1}) + '?order-by=price'
        responseparams = client.get(urlparams)
        assert responseparams.status_code == 200
        assert responseparams.context['book'] == list(filters.order_by('price'))
        url404 = reverse(urls, kwargs={ids: 10000})
        response404 = client.get(url404)
        assert response404.status_code == 404

    def test_about_book_page(self, client):
        url = reverse('about_book', kwargs={'book_id': 1})
        response = client.get(url)
        assert response.status_code == 200
        assert response.context['book'] == Book.objects.get(id=1)
        url404 = reverse("about_book", kwargs={'book_id': 10000})
        response404 = client.get(url404)
        assert response404.status_code == 404

    def test_about_author_page(self, client):
        url = reverse('about_author', kwargs={'author_id': 1})
        response = client.get(url)
        assert response.status_code == 200
        assert response.context['author'] == Author.objects.get(id=1)
        url404 = reverse("about_author", kwargs={'author_id': 10000})
        response404 = client.get(url404)
        assert response404.status_code == 404

    def test_searching(self, client):
        url = reverse('searching') + '?search=a'
        response = client.get(url)
        assert response.status_code == 200
        book = list(Book.objects.filter(Q(title__icontains='a') | Q(author__author_name__icontains='a', amount__gt=0)).distinct())
        assert list(response.context['book']) == book




