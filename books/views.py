from django import template
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.views.generic import ListView, DetailView

from users.models import Basket
from .models import *
from .forms import *
from .utils import DataMixin


# Create your views here.
def home(request): #обьект HttpRequest
    return TemplateResponse(request, 'books/home.html')


class StoreListView(DataMixin, ListView):
    template_name = 'books/store.html'

    def get_queryset(self):
        if 'order-by' in self.request.GET and self.request.GET['order-by'] is not "no-order":
            return Book.objects.filter(amount__gt=0).all().order_by(self.request.GET['order-by'])
        return Book.objects.filter(amount__gt=0).all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genre'] = Genre.objects.all()
        return context

# def store(request):
#     data_b = Book.objects.filter(amount__gt=0).all()
#     data_g = Genre.objects.all()
#     return TemplateResponse(request, 'books/store.html', {'book': data_b, 'genre': data_g})


class GenresListView(DataMixin, ListView):

    def get_queryset(self):
        if 'order-by' in self.request.GET and self.request.GET['order-by'] is not "no-order":
            return Book.objects.filter(subgenre__genre__id=self.kwargs['genre_id'], amount__gt=0).order_by(self.request.GET['order-by'])
        return Book.objects.filter(subgenre__genre__id=self.kwargs['genre_id'], amount__gt=0).order_by('id')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genre'] = Genre.objects.get(id=self.kwargs['genre_id'])
        context['subgenre'] = SubGenre.objects.filter(genre__id=self.kwargs['genre_id'])
        return context


class SubGenresListView(DataMixin, ListView):

    def get_queryset(self):
        if 'order-by' in self.request.GET:
            return Book.objects.filter(subgenre__id=self.kwargs['subgenre_id'], amount__gt=0).order_by(self.request.GET['order-by'])
        return Book.objects.filter(subgenre__id=self.kwargs['subgenre_id'], amount__gt=0).order_by('id')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subgenre'] = SubGenre.objects.get(id=self.kwargs['subgenre_id'])
        return context

# def genres(request, genre_id=0, subgenre_id =0):
#     flag = True
#     if subgenre_id:
#         genre = None
#         data_b = Book.objects.filter(subgenre__id=subgenre_id).all() & Book.objects.filter(amount__gt=0).all()
#         data_subg = SubGenre.objects.get(id=subgenre_id)
#         flag = False
#     else:
#         genre = Genre.objects.get(id=genre_id)
#         data_b = Book.objects.filter(subgenre__genre__id=genre_id).all() & Book.objects.filter(amount__gt=0).all()
#         data_subg = SubGenre.objects.filter(genre__id=genre_id).all()
#     return TemplateResponse(request, 'books/genres.html', {'book': data_b, 'subgenre': data_subg, "genre": genre, 'flag': flag})


class SearchBookListView(DataMixin, ListView):
    template_name = 'books/search.html'

    def get_queryset(self):
        query = self.request.GET['search']
        book = Book.objects.filter(Q(title__icontains=query) | Q(author__author_name__icontains=query)).distinct()
        if 'order-by' in self.request.GET and self.request.GET['order-by'] is not "no-order":
            return book.order_by(self.request.GET['order-by'])
        return book

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET['search']
        return context


class AboutBookView(DetailView):
    model = Book
    template_name = 'books/about_book.html'
    context_object_name = 'book'
    pk_url_kwarg = 'book_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['authors'] = Book.objects.get(id=self.kwargs['book_id']).author.all()
        return context

# def about_book(request, book_id):
#     book = Book.objects.get(id=book_id)
#     return TemplateResponse(request, 'books/about_book.html', {'book': book})


class AboutAuthorView(DetailView):
    model = Author
    template_name = 'books/about_author.html'
    context_object_name = 'author'
    pk_url_kwarg = 'author_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = Author.objects.get(id=self.kwargs['author_id']).book_set.all()
        return context


def contact_us(request):
    number_dev = '+79998887766'
    name_dev = 'менеджер Мария'
    address = {'number': '+79995554433', 'street_home': 'Ленинский проспект, д.5', 'city': 'Нижний Новгород'}
    admin = {'number': '+79110002233', 'email': 'mybookstoresupp@email.ru', 'name': 'менеджер Валентина'}
    data = {'number_dev': number_dev, 'name_dev': name_dev, 'address': address, 'admin': admin}
    return TemplateResponse(request, 'books/contact_us.html', data)



@login_required
def add_basket(request, book_id):
    book = Book.objects.get(id=book_id)
    amount = book.amount
    basket = Basket.objects.filter(user=request.user, book=book)
    if not basket.exists():
        Basket.objects.create(user=request.user, book=book, amount=1)
    else:
        basket = basket.first()
        if basket.amount < amount:
            basket.amount += 1
            basket.save()
        else:
            messages.error(request, 'Книг на складе больше нет!')
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def delete_basket(request, book_id):
    book = Book.objects.get(id=book_id)
    basket = Basket.objects.get(user=request.user, book=book)
    if basket.amount > 1:
        basket.amount -= 1
        basket.save()
    else:
        basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

# def search(request):
#     book = []
#     if request.method == "GET":
#         query = request.GET.get('search')
#         if query == '':
#             query = 'None'
#         book = Book.objects.filter(Q(title__icontains=query) | Q(author__author_name__icontains=query)).distinct()
#     return TemplateResponse(request, 'books/search.html', {'query': query, 'book': book})
