import os
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

default = 'nophoto.png'


def get_path_img(object, filename):
    if filename == default or object.id is None:
        return f'{filename}'
    return f'{object.id}/{filename}'


class Book(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название') #verbose name - там указать как отображать этот столбец в админ панели
    img = models.ImageField(upload_to=get_path_img, default=default, verbose_name='Изображение')
    description = models.TextField(verbose_name='Аннотация к книге', blank=True, null=True)
    subgenre = models.ForeignKey("SubGenre", on_delete=models.SET_NULL, null=True, verbose_name='Жанр')
    price = models.PositiveIntegerField(verbose_name='Цена')
    amount = models.PositiveIntegerField(verbose_name='Количество')
    author = models.ManyToManyField('Author')

    class Meta:
        ordering = ['id']

    def get_absolute_url(self):
        return reverse('about_book', kwargs={'book_id': self.pk})

    def __str__(self):  #чтобы при показе методами Book.objects выводилось название книги, а не просто номер id
        return self.title


@receiver(post_save, sender=Book)
def update_file_path(instance, created, **kwargs):
    if created:
        if instance.img.path != '/home/annbabkina/PycharmProjects/book-store/bookstore/media/nophoto.png':
            initial_path = instance.img.path
            new_path = f'{instance.id}/{instance.img.name}'
            os.makedirs(os.path.dirname(new_path), exist_ok=True)
            os.rename(initial_path, new_path)
            instance.img = new_path
            instance.save()


class Author(models.Model):
    author_name = models.CharField(max_length=50)

    def __str__(self):
        return self.author_name

    def get_absolute_url(self):
        return reverse('about_author', kwargs={'author_id': self.pk})


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('genres', kwargs={'genre_id': self.pk})


class SubGenre(models.Model):
    name = models.CharField(max_length=100)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('subgenres', kwargs={'subgenre_id': self.pk})





