
import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from books.models import Book
from users.models import *


@pytest.mark.django_db
class TestUserRegisterLogin:
    def test_register_user(self, client, user_register_data):
        url = reverse('register')
        response = client.get(url)
        assert response.status_code == 200
        user_model = get_user_model()
        assert user_model.objects.count() == 0
        response_post = client.post(url, user_register_data)
        assert user_model.objects.count() == 1
        assert response_post.status_code == 302
        assert response_post.url == reverse('lk')

    def test_login_user(self, client, user_login_data):
        url = reverse('login')
        response = client.get(url)
        assert response.status_code == 200
        user_model = get_user_model()
        assert user_model.objects.count() == 1
        client.force_login(user_model.objects.get(id=1))
        url_lk = reverse('lk')
        response_login_user = client.get(url_lk)
        assert response_login_user.status_code == 200
        client.logout()
        assert client.login(username='polina', password='1234') == False


@pytest.mark.django_db
class TestBasket:
    def test_add_and_delete_basket(self, client, user_login_data, basket_data):
        user_model = get_user_model().objects.get(id=1)
        client.force_login(user_model)
        basket = Basket.objects.filter(user=user_model, book=Book.objects.get(id=1))
        client.get(reverse('add_basket', kwargs={'book_id': 1}), {}, HTTP_REFERER='lk')
        assert basket.first().amount == 2
        resp = client.get(reverse('add_basket', kwargs={'book_id': 1}), {}, HTTP_REFERER='lk', follow=True)
        messages = list(resp.context['messages'])
        assert str(messages[0]) == 'Книг на складе больше нет!'
        client.get(reverse('delete_basket', kwargs={'book_id': 1}), {}, HTTP_REFERER='lk')
        assert basket.first().amount == 1
        client.get(reverse('delete_basket', kwargs={'book_id': 1}), {}, HTTP_REFERER='lk')
        assert basket.exists() == False


@pytest.mark.django_db
class TestOrder:
    def test_check_books_func(self, basket_data):
        user_model = get_user_model().objects.get(id=1)
        basket = Basket.objects.filter(user=user_model)
        assert basket.filter(book__amount=0).exists() == False

    def test_create_order(self, client, user_login_data, basket_data, order_data):
        user_model = get_user_model().objects.get(id=1)
        client.force_login(user_model)
        basket = Basket.objects.filter(user=user_model)
        basket_count = basket.count()
        url = reverse('order')
        response = client.get(url)
        assert response.status_code == 200
        assert Order.objects.filter(user=user_model).count() == 0
        client.post(url, order_data)
        assert Order.objects.filter(user=user_model).count() == 1
        assert basket.exists() == False
        assert BookOrder.objects.filter(order__id=1).count() == basket_count
        url_order = reverse('about_order', kwargs={'order_id': 1})
        response_order = client.get(url_order)
        assert response_order.status_code == 200













