import pytest
from captcha.models import CaptchaStore
from django.contrib.auth import get_user_model
from books.tests.conftest import create_db
from users.models import *


@pytest.fixture()
def user_register_data(db):
    captcha = CaptchaStore.objects.get(hashkey=CaptchaStore.generate_key())
    return {'username': 'anna', 'email': 'anna@yandex.ru', 'password1': 'userpass1',
            'password2': 'userpass1', 'captcha_0': captcha.hashkey, 'captcha_1': captcha.response}


@pytest.fixture()
def user_login_data(db):
    user_model = get_user_model()
    user_model.objects.create(username='anna', email='anna@mail.com', password='userpass1')


@pytest.fixture()
def basket_data(db, user_login_data, create_db):
    user_model = get_user_model()
    Basket.objects.create(user=user_model.objects.get(id=1), book=Book.objects.get(id=1))


@pytest.fixture()
def order_data(db):
    StepOrder.objects.create(name='Оплата')
    WayOrder.objects.create(name='Курьер')
    return {'way': 1}
