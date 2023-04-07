from django.contrib import admin
from .models import *
# Register your models here.


class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'amount', 'subgenre') #это будет отображаться в админ панели при нажатии на модель
    list_display_links = ('id', 'title') #на какие поля можно нажать чтобы перейти на объект
    search_fields = ('id', 'title', 'subgenre') #поиск объекта по этим полям
    fieldsets = ((None, {'fields': ('title', 'author',  'subgenre', 'description', 'img')}), ('Store',
                                                                                              {'fields': ('price', 'amount')}))


class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name') #это будет отображаться в админ панели при нажатии на модель
    list_display_links = ('id', 'name') #на какие поля можно нажать чтобы перейти на объект
    search_fields = ('id', 'name') #поиск объекта по этим полям


class SubGenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'genre') #это будет отображаться в админ панели при нажатии на модель
    list_display_links = ('id', 'name') #на какие поля можно нажать чтобы перейти на объект
    search_fields = ('id', 'name', 'genre') #поиск объекта по этим полям


admin.site.register(Book, BookAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(SubGenre, SubGenreAdmin)
admin.site.register(Author)
