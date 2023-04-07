from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from books.models import Book



class User(AbstractUser):
    email = models.EmailField(unique=True)
    date_of_birth = models.DateTimeField(blank=True, null=True)


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
    step = models.ForeignKey(StepOrder, on_delete=models.DO_NOTHING, default=StepOrder.objects.get(name='Оплата'))
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

