from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.db.models import F
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from books.models import Book
from users.forms import *
from users.models import Basket, StepOrder, WayOrder, BookOrder


# Create your views here.

##register function
# def register(request):
#     if request.method == 'POST':
#         form = RegisterUserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             login(request, form.save())
#             return redirect('home')
#     else:
#         form = RegisterUserForm()
#     context = {'form': form}
#     return TemplateResponse(request, 'users/register.html', context=context)


class RegisterUserView(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('lk')


class LoginUserView(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('home')


#check available all books for order or not
def check_books(basket_obj):
    return basket_obj.filter(book__amount=0).exists()


@login_required
def lk(request):
    if request.method == 'POST':
        form = ProfileUserForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль обновлен')
            return redirect('lk')
    else:
        form = ProfileUserForm(instance=request.user)
    order = Order.objects.filter(user=request.user).select_related('way', 'step').order_by('date_start')
    basket = Basket.objects.filter(user=request.user).select_related('book')
    return TemplateResponse(request, 'users/lk.html', {'form': form, 'basket': basket, 'order': order, 'flag': check_books(basket)})


@login_required
def order(request):
    basket = Basket.objects.filter(user=request.user).select_related('book')
    if request.method == 'POST':
        if check_books(basket) or not basket.exists():
            messages.error(request, 'Невозможно оформить заказ')
        else:
            Order.objects.create(user=request.user, total_sum=basket.total_sum(), way=WayOrder.objects.get(id=request.POST['way']))
            order = Order.objects.filter(user=request.user).latest('date_start')
            for b in basket:
                BookOrder.objects.create(order=order, book=b.book, amount=b.amount)
                Book.objects.filter(id=b.book.id).update(amount=F('amount') - b.amount)
                b.delete()
            messages.success(request, 'Оформление заказа прошло успешно!')
            return redirect('lk')
    form = OrderForm(initial={'user': request.user, 'total_sum': basket.total_sum()})
    return TemplateResponse(request, 'users/orderpage.html', {'form': form, 'basket': basket})


class AboutOrderView(ListView):
    model = BookOrder
    template_name = 'users/about_order.html'
    context_object_name = 'bookorder'
    allow_empty = False

    def get_queryset(self):
        return BookOrder.objects.filter(order=self.kwargs['order_id']).select_related('book')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = Order.objects.get(id=self.kwargs['order_id'])
        return context

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
    return redirect(request.META['HTTP_REFERER'])


@login_required
def delete_basket(request, book_id):
    book = Book.objects.get(id=book_id)
    basket = Basket.objects.get(user=request.user, book=book)
    if basket.amount > 1:
        basket.amount -= 1
        basket.save()
    else:
        basket.delete()
    return redirect(request.META['HTTP_REFERER'])