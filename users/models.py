from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from books.models import Book


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users require an email field')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    date_of_birth = models.DateTimeField(blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class BasketQuerySet(models.QuerySet):
    def total_sum(self):
        return sum([b.sum() for b in self])

    def total_amount(self):
        return sum([b.amount for b in self])


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=1)
    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f'Корзина {self.user.username} | Книга {self.book.title}'

    def sum(self):
        return self.book.price * self.amount


class StepOrder(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class WayOrder(models.Model):
    name = models.CharField(max_length=255, verbose_name='Как доставить заказ?')

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    step = models.ForeignKey(StepOrder, on_delete=models.DO_NOTHING, default=1)
    way = models.ForeignKey(WayOrder, on_delete=models.DO_NOTHING, verbose_name='Как доставить заказ?')
    total_sum = models.PositiveIntegerField()
    date_start = models.DateTimeField(auto_now_add=True)
    date_finish = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Заказ {self.pk} для {self.user.username}'

    def get_absolute_url(self):
        return reverse('about_order', kwargs={'order_id': self.pk})


class BookOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()

    def sum(self):
        return self.book.price * self.amount

    # def __str__(self):
    #     return self.book.title

